from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Game, Guess, Word
from api.serializers import GameSerializer, GuessSerializer, UserSerializer
from rest_framework import permissions
from rest_framework.reverse import reverse
from api.utils import color_word
from rest_framework import authentication
from django.http import HttpRequest

class SubSessionAuthentication(authentication.SessionAuthentication):
    def authenticate(self, request: HttpRequest):
        if request.session.get("username"):
            try:
                user = User.objects.get(username=request.session.get("username"))
                return (user, None)
            except User.DoesNotExist:
                return None
        return None

class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().all()
        serializer = self.get_serializer(queryset, many=True)
        for game_data, game_instance in zip(serializer.data, queryset):
            if game_instance.status == Game.GameStatus.IN_PROGRESS:
                game_data['key'] = '*****'
        return Response(serializer.data)

class GameDetail(generics.RetrieveUpdateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        if instance.status == Game.GameStatus.IN_PROGRESS:
            data['key'] = '*****' 
        return Response(data)
    
class GuessList(generics.ListCreateAPIView):
    queryset = Guess.objects.all()
    serializer_class = GuessSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [SubSessionAuthentication]
    def create(self, request, *args, **kwargs):
        word_value = request.data.get('word')
        if request.session.get("game_id") is None:
            return Response({'error': 'No active game in session.'}, status=400)
        try:
            word = Word.objects.get(value=word_value)
        except Word.DoesNotExist:
            return Response({'error': 'Word does not exist.'}, status=400)
        try:
            game = Game.objects.get(id=request.session["game_id"])
        except Game.DoesNotExist:
            return Response({'error': 'Game not found.'}, status=400)
        if game.status != Game.GameStatus.IN_PROGRESS:
            return Response({'error': 'Game is not in progress.'}, status=400)
        if Guess.objects.filter(game=game, value=word).exists():
            return Response({'error': 'Word has already been guessed.'}, status=400)
        if len(word_value) != len(game.key):
            return Response({'error': 'Word length mismatch.'}, status=400)
        print(word_value, game.key)
        serializer = self.get_serializer(data={'game': game.pk, 'value': word.pk, 'is_correct': word_value == game.key})
        if serializer.is_valid():
            guess_count = Guess.objects.filter(game=game).count()
            if request.user.is_authenticated:
                profile = request.user.userprofile
                if word_value == game.key:
                    profile.games_won += 1
                    profile.current_streak += 1
                    if profile.current_streak > profile.max_streak:
                        profile.max_streak = profile.current_streak
                    profile.guess_distribution[guess_count] += 1
                elif guess_count + 1 >= 6:
                    profile.current_streak = 0
                profile.save()
            serializer.save(game=game, value=word, is_correct=(word_value == game.key))
            ret = color_word(word_value, game.key)
            if word_value == game.key:
                game.status = Game.GameStatus.WON
                game.save()
            elif guess_count >= 5:
                game.status = Game.GameStatus.LOST
                game.save()
            return Response({'result': ret}, status=201)
        return Response(serializer.errors, status=400)

class GuessDetail(generics.RetrieveUpdateAPIView):
    queryset = Guess.objects.all()
    serializer_class = GuessSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GiveUpAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, format=None):
        if request.session.get("game_id") is None:
            return Response({'error': 'No active game in session.'}, status=400)
        try:
            game = Game.objects.get(id=request.session.get("game_id"))
        except Game.DoesNotExist:
            return Response({'error': 'Game not found.'}, status=404)
        if game.status != Game.GameStatus.IN_PROGRESS:
            return Response({'error': 'Game is not in progress.'}, status=400)
        game.status = Game.GameStatus.LOST
        game.save()
        return Response({'message': 'Game marked as lost.', 'key': game.key}, status=200)
    
class ApiRootView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, format=None):
        return Response({
            'games': reverse('game_list', request=request, format=format),
            'guesses': reverse('guess_list', request=request, format=format),
            'users': reverse('user_list', request=request, format=format),
            'giveup': reverse('give_up', request=request, format=format),
        })
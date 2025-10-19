from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Game, Guess, Word
from api.serializers import GameSerializer, GuessSerializer, UserSerializer
from rest_framework import permissions

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
        serializer = self.get_serializer(data={'game': game.pk, 'value': word.pk, 'is_correct': word_value == game.key})
        if serializer.is_valid():
            serializer.save(game=game, value=word, is_correct=(word_value == game.key))
            ret = ''
            m = {}
            for char in game.key:
                m[char] = m.get(char, 0) + 1
            for idx in range(len(game.key)):
                if word_value[idx] == game.key[idx]:
                    ret += 'G'  # Green
                    m[word_value[idx]] -= 1
                elif word_value[idx] in game.key:
                    ret += 'Y'  # Yellow
                    if m[word_value[idx]] > 0:
                        m[word_value[idx]] -= 1
                    else:
                        ret = ret[:-1] + 'B'
                else:
                    ret += 'B'  # Black
            if word_value == game.key:
                game.status = Game.GameStatus.WON
                game.save()
            elif Guess.objects.filter(game=game).count() >= 6:
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
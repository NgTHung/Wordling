import random
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Game, Guess, NightmareGame, NightmareGuess
from api.serializers import GameSerializer, GuessSerializer, NightmareGameSerializer, NightmareGuessSerializer, NightmareGuessSerializer, UserSerializer
from rest_framework import permissions
from rest_framework.reverse import reverse
from api.utils import color_word, nightmare_color_word
from rest_framework import authentication
from django.http import HttpRequest
from api.constants import COLOR_CORRECT, COLOR_BROKEN, COLOR_VAMPIRE_CORRECT, WORD_LENGTH, MAX_GUESSES, COLOR_ABSENT, COLOR_PRESENT
from string import hexdigits

class SubSessionAuthentication(authentication.SessionAuthentication):
    def authenticate(self, request: HttpRequest):
        if request.session.get("username"):
            try:
                user = User.objects.get(username=request.session.get("username"))
                return (user, None)
            except User.DoesNotExist:
                return None
        return None

class GameList(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().all()
        serializer = self.get_serializer(queryset, many=True)
        for game_data, game_instance in zip(serializer.data, queryset):
            if game_instance.status == Game.GameStatus.IN_PROGRESS:
                game_data['pallet'] = '*****'
            else:
                game_data['pallet'] = game_instance.pallet.name
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
            data['pallet'] = '*****'
        else:
            data['pallet'] = instance.pallet.name
            data['colors'] = instance.pallet.colors
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
            game = Game.objects.get(id=request.session["game_id"])
        except Game.DoesNotExist:
            return Response({'error': 'Game not found.'}, status=400)
        if game.status != Game.GameStatus.IN_PROGRESS:
            return Response({'error': 'Game is not in progress.'}, status=400)
        if Guess.objects.filter(game=game, value=word_value).exists():
            return Response({'error': 'Word has already been guessed.'}, status=400)
        if len(word_value) != WORD_LENGTH:
            return Response({'error': 'Word length mismatch.'}, status=400)
        for char in word_value:
            if char not in hexdigits:
                return Response({'error': 'Invalid character in word.'}, status=400)
        word = word_value.upper()
        ret = color_word(word_value, game.pallet.colors)
        c_bitmask = game.correct_bitmask
        for i in ret:
            if i == COLOR_CORRECT*WORD_LENGTH:
                c_bitmask = c_bitmask[:ret.index(i)] + '1' + c_bitmask[ret.index(i)+1:]
        serializer = self.get_serializer(data={'game': game.pk, 'value': word_value})
        if serializer.is_valid():
            guess_count = Guess.objects.filter(game=game).count()
            if request.user.is_authenticated:
                profile = request.user.userprofile
                if c_bitmask == '1' * 4:
                    profile.games_won += 1
                    profile.current_streak += 1
                    if profile.current_streak > profile.max_streak:
                        profile.max_streak = profile.current_streak
                    profile.guess_distribution[guess_count] += 1
                elif guess_count + 1 >= MAX_GUESSES:
                    profile.current_streak = 0
                profile.save()
            serializer.save(game=game, value=word)
            game.correct_bitmask = c_bitmask
            if c_bitmask == '1' * 4:
                game.status = Game.GameStatus.WON
            elif guess_count >= MAX_GUESSES - 1:
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
        return Response({'message': 'Game marked as lost.', 'colors': game.pallet.colors}, status=200)
    
class ApiRootView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, format=None):
        return Response({
            'games': reverse('game_list', request=request, format=format),
            'guesses': reverse('guess_list', request=request, format=format),
            'users': reverse('user_list', request=request, format=format),
            'giveup': reverse('give_up', request=request, format=format),
        })
    
class NightmareGameList(generics.ListAPIView):
    queryset = NightmareGame.objects.all()
    serializer_class = NightmareGameSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NightmareGameDetail(generics.RetrieveUpdateAPIView):
    queryset = NightmareGame.objects.all()
    serializer_class = NightmareGameSerializer
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        if instance.status == NightmareGame.GameStatus.IN_PROGRESS:
            data['pallet'] = '*****'
        else:
            data['pallet'] = instance.pallet.name
            data['colors'] = instance.pallet.colors
        return Response(data)

class NightmareGuessList(generics.ListCreateAPIView):
    queryset = NightmareGuess.objects.all()
    serializer_class = NightmareGuessSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [SubSessionAuthentication]
    def create(self, request, *args, **kwargs):
        word_value = request.data.get('word')
        if request.session.get("nightmare_game_id") is None:
            return Response({'error': 'No active game in session.'}, status=400)
        try:
            game = NightmareGame.objects.get(id=request.session["nightmare_game_id"])
        except NightmareGame.DoesNotExist:
            return Response({'error': 'Game not found.'}, status=400)
        if game.status != NightmareGame.GameStatus.IN_PROGRESS:
            return Response({'error': 'Game is not in progress.'}, status=400)
        if NightmareGuess.objects.filter(game=game, value=word_value).exists():
            return Response({'error': 'Word has already been guessed.'}, status=400)
        if len(word_value) != WORD_LENGTH:
            return Response({'error': 'Word length mismatch.'}, status=400)
        for char in word_value:
            if char not in hexdigits:
                return Response({'error': 'Invalid character in word.'}, status=400)
        word = word_value.upper()
        challenge = game.challenge
        if challenge == 'LIAR':
            if game.challenge_value == '1':
                challenge_value = 0
            else:
                challenge_value = 0
                c = color_word(word_value, game.pallet.colors)
                for i in c:
                    if i == COLOR_CORRECT*WORD_LENGTH:
                        challenge_value = -1
                        break
                if challenge_value != -1:
                    pvalue = {0: 0.0, 1: 0.0, 2: 0.15, 3: 0.25, 4: 0.35, 5: 0.45, 6: 0.55, 7: 0.65, 8: 0.75, 9: 0.80}
                    rand_val = random.random()
                    chance = pvalue.get(NightmareGuess.objects.filter(game=game).count(), 0.5)
                    challenge_value = int(rand_val < chance)
                    if challenge_value == 1:
                        game.challenge_value = '1'
                        game.save()
                else:
                    challenge_value = 0
        elif challenge == 'BROKEN':
            challenge_value = game.challenge_value
        elif challenge == 'AMNESIA':
            challenge_value = ''
        elif challenge == 'GLITCH':
            challenge_value = int(game.challenge_value) if game.challenge_value.isdigit() else 0
        elif challenge == 'VAMPIRE':
            challenge_value = int(game.challenge_value) if game.challenge_value.isdigit() else 0
        ret = nightmare_color_word(word_value, game.pallet.colors, challenge, challenge_value)
        c_bitmask = game.correct_bitmask
        is_any_correct = False
        for i in ret:
            is_all_correct = all(
                char in [COLOR_CORRECT, COLOR_VAMPIRE_CORRECT, COLOR_BROKEN] 
                for char in i
            )
            if is_all_correct:
                c_bitmask = c_bitmask[:ret.index(i)] + '1' + c_bitmask[ret.index(i)+1:]
                is_any_correct = True
        serializer = self.get_serializer(data={'game': game.pk, 'value': word_value, 'color_feedback': ret})
        if serializer.is_valid():
            guess_count = NightmareGuess.objects.filter(game=game).count()
            if request.user.is_authenticated:
                profile = request.user.userprofile
                if c_bitmask == '1' * 4:
                    profile.games_won += 1
                    profile.current_streak += 1
                    if profile.current_streak > profile.max_streak:
                        profile.max_streak = profile.current_streak
                    profile.guess_distribution[guess_count] += 1
                elif guess_count + 1 >= MAX_GUESSES:
                    profile.current_streak = 0
                profile.save()
            serializer.save(game=game, value=word, color_feedback=ret)
            if challenge == 'AMNESIA' and is_any_correct:
                qs = NightmareGuess.objects.filter(game=game)
                for past_guess in qs:
                    new_ret = [COLOR_ABSENT*WORD_LENGTH for _ in range(4)]
                    past_guess.color_feedback = new_ret
                    past_guess.save()
            game.correct_bitmask = c_bitmask
            if c_bitmask == '1' * 4:
                game.status = NightmareGame.GameStatus.WON
            elif guess_count >= MAX_GUESSES - 1:
                game.status = NightmareGame.GameStatus.LOST
            game.save()
            return Response({'result': ret}, status=201)
        return Response(serializer.errors, status=400)

class NightmareGuessDetail(generics.RetrieveUpdateAPIView):
    queryset = NightmareGuess.objects.all()
    serializer_class = NightmareGuessSerializer

class NightmareGiveUpAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, format=None):
        if request.session.get("nightmare_game_id") is None:
            return Response({'error': 'No active game in session.'}, status=400)
        try:
            game = NightmareGame.objects.get(id=request.session.get("nightmare_game_id"))
        except NightmareGame.DoesNotExist:
            return Response({'error': 'Game not found.'}, status=404)
        if game.status != NightmareGame.GameStatus.IN_PROGRESS:
            return Response({'error': 'Game is not in progress.'}, status=400)
        game.status = NightmareGame.GameStatus.LOST
        game.save()
        return Response({'message': 'Game marked as lost.', 'colors': game.pallet.colors}, status=200)
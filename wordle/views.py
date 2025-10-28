from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView
from django.db.models import Max

from accounts.models import UserProfile
from api.models import Game, Guess, Pallet
from api.utils import color_word
from api.constants import LEADERBOARD_PAGE_SIZE

import random
# Create your views here.
class GameView(TemplateView):
    template_name = "game.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game_history'] = []
        context['pallet_colors'] = None
        context['request'] = self.request
        if(self.request.session.get("game_id")):
            try:
                game = Game.objects.get(id=self.request.session["game_id"], is_nightmare=False)
                if game.status != Game.GameStatus.IN_PROGRESS:
                    del self.request.session["game_id"]
                    return context
                history = []
                queryset = Guess.objects.filter(game=game).order_by('created_at').select_related('game__pallet')
                for guess in queryset:
                    word_value = guess.value
                    ret = color_word(word_value, game.pallet.colors)
                    history.append({'word': word_value, 'result': ret})
                context['game_id'] = game.pk
                context['game_history'] = (history)
                context['pallet_colors'] = game.pallet.colors
            except Game.DoesNotExist:
                pass
        return context
    def get(self, request, *args, **kwargs):
        if request.session.get("game_id"):
            try:
                game = Game.objects.get(id=request.session["game_id"], is_nightmare=False)
                if game.status != Game.GameStatus.IN_PROGRESS:
                    del request.session["game_id"]
            except Game.DoesNotExist:
                del request.session["game_id"]
        if not request.session.get("game_id"):
            if request.user.is_authenticated:
                request.session["username"] = request.user.username
                game = Game.objects.filter(user=request.user, status=Game.GameStatus.IN_PROGRESS).first()
                if game:
                    request.session["game_id"] = game.id
                    return super().get(request, *args, **kwargs)
                user = request.user
            else:
                user = None
            max_id = Pallet.objects.aggregate(max_id=Max('id'))['max_id']
            random_id = random.randint(1, max_id)
            pallet = Pallet.objects.filter(id=random_id).first()
            game = Game.objects.create(user=user, pallet=pallet)
            request.session["game_id"] = game.id
        return super().get(request, *args, **kwargs)

class HomeView(TemplateView):
    template_name = 'home.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('game')
        return super().dispatch(request, *args, **kwargs)

class LeaderboardView(ListView):
    model = UserProfile
    template_name = 'leaderboard.html'
    context_object_name = 'profiles'
    
    # Show top LEADERBOARD_PAGE_SIZE players
    paginate_by = LEADERBOARD_PAGE_SIZE

    def get_queryset(self):
        return UserProfile.objects.order_by(
            '-max_streak', 
            '-games_won'
        )
    
class NightmareView(TemplateView):
    template_name = 'nightmare.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game_history'] = []
        context['pallet_colors'] = None
        context['request'] = self.request
        if(self.request.session.get("game_id")):
            try:
                game = Game.objects.get(id=self.request.session["game_id"], is_nightmare=True)
                if game.status != Game.GameStatus.IN_PROGRESS:
                    del self.request.session["game_id"]
                    return context
                history = []
                queryset = Guess.objects.filter(game=game).order_by('created_at').select_related('game__pallet')
                for guess in queryset:
                    word_value = guess.value
                    ret = color_word(word_value, game.pallet.colors)
                    history.append({'word': word_value, 'result': ret})
                context['game_id'] = game.pk
                context['game_history'] = (history)
            except Game.DoesNotExist:
                pass
        return context
    def get(self, request, *args, **kwargs):
        if request.session.get("game_id"):
            try:
                game = Game.objects.get(id=request.session["game_id"], is_nightmare=True)
                if game.status != Game.GameStatus.IN_PROGRESS:
                    del request.session["game_id"]
            except Game.DoesNotExist:
                del request.session["game_id"]
        if not request.session.get("game_id"):
            if request.user.is_authenticated:
                request.session["username"] = request.user.username
                game = Game.objects.filter(user=request.user, status=Game.GameStatus.IN_PROGRESS).first()
                if game:
                    request.session["game_id"] = game.id
                    return super().get(request, *args, **kwargs)
                user = request.user
            else:
                user = None
            max_id = Pallet.objects.aggregate(max_id=Max('id'))['max_id']
            random_id = random.randint(1, max_id)
            pallet = Pallet.objects.filter(id=random_id).first()
            game = Game.objects.create(user=user, pallet=pallet)
            request.session["game_id"] = game.id
        return super().get(request, *args, **kwargs)
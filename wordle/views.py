from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView
from django.db.models import Max

from accounts.models import UserProfile
from api.models import Game, Guess, Word
from api.utils import color_word
from api.constants import LEADERBOARD_PAGE_SIZE

import random
# Create your views here.
class GameView(TemplateView):
    template_name = "game.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game_history'] = []
        context['request'] = self.request
        if(self.request.session.get("game_id")):
            try:
                game = Game.objects.get(id=self.request.session["game_id"])
                if game.status != Game.GameStatus.IN_PROGRESS:
                    del self.request.session["game_id"]
                    return context
                history = []
                queryset = Guess.objects.filter(game=game).order_by('created_at').select_related('value')
                for guess in queryset:
                    word_value = guess.value.value
                    ret = color_word(word_value, game.key)
                    history.append({'word': word_value, 'result': ret})
                context['game_id'] = game.pk
                context['game_history'] = (history)
            except Game.DoesNotExist:
                pass
        return context
    def get(self, request, *args, **kwargs):
        if request.session.get("game_id"):
            try:
                game = Game.objects.get(id=request.session["game_id"])
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
            max_id = Word.objects.aggregate(max_id=Max('id'))['max_id']
            random_id = random.randint(1, max_id)
            word = Word.objects.filter(id=random_id).first()
            game = Game.objects.create(user=user, key=word.value)
            request.session["game_id"] = game.id
        return super().get(request, *args, **kwargs)

class HomeView(TemplateView):
    """
    Serves the main landing page.
    """
    template_name = 'home.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('game')
        return super().dispatch(request, *args, **kwargs)

class LeaderboardView(ListView):
    """
    Displays a ranked list of users based on their game statistics.
    """
    model = UserProfile
    template_name = 'leaderboard.html'
    context_object_name = 'profiles'
    
    # Show top LEADERBOARD_PAGE_SIZE players
    paginate_by = LEADERBOARD_PAGE_SIZE

    def get_queryset(self):
        """
        Order the profiles by the most important stats.
        - The `-` prefix means "descending".
        """
        return UserProfile.objects.order_by(
            '-max_streak', 
            '-games_won'
        )
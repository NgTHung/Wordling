from django.shortcuts import render
from django.views.generic import TemplateView
from api.models import Game, Guess, Word
from django.contrib.auth.models import User
# Create your views here.
class HomeView(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game_history'] = []
        if(self.request.session.get("game_id")):
            try:
                game = Game.objects.get(id=self.request.session["game_id"])
                if game.status != Game.GameStatus.IN_PROGRESS:
                    del self.request.session["game_id"]
                    return context
                history = []
                for guess in Guess.objects.filter(game=game).order_by('created_at'):
                    ret = ''
                    word_value = guess.value.value
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
            word = Word.objects.order_by('?').first()
            if request.user.is_anonymous:
                user = User.objects.get_or_create(username="Annonymous")[0]
            else:
                user = request.user
            game = Game.objects.create(user=user, key=word.value)
            request.session["game_id"] = game.id
        return super().get(request, *args, **kwargs)

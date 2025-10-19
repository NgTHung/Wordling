from django.urls import path

from wordle.views import HomeView, LeaderboardView, GameView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("play/", GameView.as_view(), name="game"),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]
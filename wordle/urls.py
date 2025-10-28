from django.urls import path

from wordle.views import HomeView, LeaderboardView, GameView, NightmareView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("play/", GameView.as_view(), name="game"),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('nightmare/', NightmareView.as_view(), name='nightmare'),
]
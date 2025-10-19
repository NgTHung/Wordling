from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path('games/', views.GameList.as_view(), name='game_list'),
    path('games/<int:pk>/', views.GameDetail.as_view(), name='game_detail'),
    path('guesses/', views.GuessList.as_view(), name='guess_list'),
    path('guesses/<int:pk>/', views.GuessDetail.as_view(), name='guess_detail'),
    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('giveup/', views.GiveUpAPIView.as_view(), name='give_up'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
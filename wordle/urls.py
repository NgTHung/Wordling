from django.urls import path, include

from wordle.views import HomeView

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("", HomeView.as_view(), name="home"),
]
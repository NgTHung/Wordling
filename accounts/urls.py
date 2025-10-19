from django.urls import path

from accounts.views import ProfileView, SignUpView, CustomLoginView, CustomLogoutView
urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", SignUpView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
# your_app/views.py
from django.shortcuts import redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.auth.models import User

from accounts.models import UserProfile
from api.models import Game

class LoggedOutOnlyMixin:
    """
    A mixin that redirects authenticated users to a specified URL.
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in.")
            return redirect('game') 
        return super().dispatch(request, *args, **kwargs)

class CustomLoginView(LoggedOutOnlyMixin, auth_views.LoginView):
    template_name = 'login.html'
    
    def get_success_url(self):
        return reverse_lazy('game')

    def form_valid(self, form):
        if self.request.session.get('game_id') is not None:
            messages.info(self.request, "Resuming your previous game.")
            game_id = self.request.session['game_id']
            usr = User.objects.filter(username=form.cleaned_data.get('username')).first()
            Game.objects.filter(id=game_id).update(user=usr)
        messages.success(self.request, f"Welcome back, {form.cleaned_data.get('username')}!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Adds extra context to the template.
        """
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Login to Quadhexle" 
        return context

class CustomLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        username = request.user.get_username()
        response = super().dispatch(request, *args, **kwargs)
        messages.success(self.request, f"You have been successfully logged out. See you soon, {username}!")
        
        return response

class SignUpView(CreateView):
    form_class = UserCreationForm
    
    success_url = reverse_lazy('game')
    
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('game')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        
        user = self.object
        
        login(self.request, user)
        if self.request.session.get('game_id') is not None:
            messages.info(self.request, "Resuming your previous game.")
            game_id = self.request.session['game_id']
            Game.objects.filter(id=game_id).update(user=user)
        
        return response

class ProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    
    template_name = 'profile.html'
    
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        distribution = profile.guess_distribution
        context['max_dist_value'] = max(distribution) if any(distribution) else 1
        
        return context
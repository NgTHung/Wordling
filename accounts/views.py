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
            return redirect('game') # Or your desired redirect URL
        return super().dispatch(request, *args, **kwargs)

class CustomLoginView(LoggedOutOnlyMixin, auth_views.LoginView):
    """
    Custom login view to add extra functionality.
    """
    template_name = 'login.html'
    
    def get_success_url(self):
        """
        Defines the redirect URL after a successful login.
        """
        # You could add more complex logic here, e.g., redirect staff to an admin page
        return reverse_lazy('game')

    def form_valid(self, form):
        """
        Called after the form is validated. We add a success message here.
        """
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
        context['page_title'] = "Login to Wordle" # Example of extra context
        return context

# ----------------------------------------------
# 2. CUSTOM LOGOUT VIEW
# ----------------------------------------------

class CustomLogoutView(auth_views.LogoutView):
    """
    Custom logout view to add a success message.
    """
    # The URL to redirect to after logging out.
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        """
        We override dispatch to add a message *after* the user is logged out.
        """
        # Get the user's name before they are logged out
        username = request.user.get_username()
        
        # Call the parent's dispatch method to handle the actual logout
        response = super().dispatch(request, *args, **kwargs)

        # Now that the user is logged out, add the message
        messages.success(self.request, f"You have been successfully logged out. See you soon, {username}!")
        
        return response

class SignUpView(CreateView):
    """
    A Class-Based View for handling user registration.
    """
    # The form to use for creating a new user.
    form_class = UserCreationForm
    
    success_url = reverse_lazy('game')
    
    # The template to render for the signup page.
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        """
        Add extra context to the template.
        """
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        return context

    def dispatch(self, request, *args, **kwargs):
        """
        Redirects logged-in users away from the signup page.
        """
        if request.user.is_authenticated:
            return redirect('game')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        This method is called when valid form data has been POSTed.
        It should return an HttpResponse.
        We override it to log the user in after they are created.
        """
        # First, let the CreateView's default behavior save the user
        # and return the proper redirect response.
        response = super().form_valid(form)
        
        # self.object holds the new user object that was just created.
        user = self.object
        
        # Log the new user in.
        login(self.request, user)
        if self.request.session.get('game_id') is not None:
            messages.info(self.request, "Resuming your previous game.")
            game_id = self.request.session['game_id']
            Game.objects.filter(id=game_id).update(user=user)
        
        # Return the response (the redirect to success_url).
        return response

class ProfileView(LoginRequiredMixin, DetailView):
    """
    Displays the profile and statistics for the currently logged-in user.
    """
    # 1. Specify the model this view will display.
    model = UserProfile
    
    # 2. Specify the template to render.
    template_name = 'profile.html'
    
    # 3. Specify the name for the object in the template's context.
    #    This ensures your template can still use `{{ profile }}`.
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        """
        Overrides the default `get_object` to return the UserProfile
        associated with the currently logged-in user, instead of looking
        for a pk or slug in the URL.
        """
        return self.request.user.userprofile

    def get_context_data(self, **kwargs):
        """
        Adds extra context to the template, like the max distribution value
        for scaling the chart bars.
        """
        # First, get the base context from the parent class.
        context = super().get_context_data(**kwargs)
        
        # Get the profile object (which this method gets from get_object).
        profile = self.get_object()
        
        # Calculate the max value for the distribution chart.
        distribution = profile.guess_distribution
        context['max_dist_value'] = max(distribution) if any(distribution) else 1
        
        return context
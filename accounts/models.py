from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from api.constants import MAX_GUESSES, WIN_PERCENTAGE_MULTIPLIER

def get_default_guess_distribution():
    """Create default guess distribution array with MAX_GUESSES slots."""
    return [0] * MAX_GUESSES

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    games_won = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    max_streak = models.IntegerField(default=0)
    
    # Stores the number of wins for each guess count (1 to 6)
    # e.g., [10, 25, 30, 15, 5, 2] means 10 wins on the 1st guess, etc.
    guess_distribution = models.JSONField(default=get_default_guess_distribution)

    def __str__(self):
        return self.user.username

    @property
    def win_percentage(self):
        if self.games_played == 0:
            return 0
        return round((self.games_won / self.games_played) * WIN_PERCENTAGE_MULTIPLIER)
    @property
    def games_played(self):
        return sum(self.guess_distribution)

# This is a Django Signal. It ensures that whenever a new User is created,
# a corresponding UserProfile is automatically created with it.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
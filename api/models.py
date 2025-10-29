from django.db import models
from django.conf import settings
# Create your models here.

class Pallet(models.Model):
    name = models.CharField(max_length=100, unique=True)
    colors = models.JSONField()

    def __str__(self):
        return self.name

class Game(models.Model):
    class GameStatus(models.TextChoices):
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        WON = 'WON', 'Won'
        LOST = 'LOST', 'Lost'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    pallet = models.ForeignKey(Pallet, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=GameStatus.choices, default=GameStatus.IN_PROGRESS, db_index=True)
    correct_bitmask = models.CharField(max_length=4, default='0000')
    class Meta:
        ordering = ['-created_at']
    
class Guess(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    value = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class NightmareGame(models.Model):
    class GameStatus(models.TextChoices):
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        WON = 'WON', 'Won'
        LOST = 'LOST', 'Lost'
    
    class GameChallenge(models.TextChoices):
        LIAR = 'LIAR', 'The Liar'
        BROKEN = 'BROKEN', 'The Broken Keyboard'
        AMNESIA = 'AMNESIA', 'The Amnesiac'
        GLITCH = 'GLITCH', 'The Glitch'
        VAMPIRE = 'VAMPIRE', 'The Vampire'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    pallet = models.ForeignKey(Pallet, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=Game.GameStatus.choices, default=Game.GameStatus.IN_PROGRESS, db_index=True)
    challenge = models.CharField(max_length=20, choices=GameChallenge.choices)
    challenge_value = models.CharField(max_length=100, default='')
    correct_bitmask = models.CharField(max_length=4, default='0000')

    class Meta:
        ordering = ['-created_at']

class NightmareGuess(models.Model):
    game = models.ForeignKey(NightmareGame, on_delete=models.CASCADE)
    value = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    color_feedback = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
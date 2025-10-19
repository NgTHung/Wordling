from django.db import models
from django.conf import settings
# Create your models here.

class Game(models.Model):
    class GameStatus(models.TextChoices):
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        WON = 'WON', 'Won'
        LOST = 'LOST', 'Lost'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    key = models.CharField(max_length=100, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=GameStatus.choices, default=GameStatus.IN_PROGRESS)

    class Meta:
        ordering = ['-created_at']

class Word(models.Model):
    value = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.value
    
class Guess(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    value = models.ForeignKey(Word, on_delete=models.DO_NOTHING)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

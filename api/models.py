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
    is_nightmare = models.BooleanField(default=False)
    class Meta:
        ordering = ['-created_at']
    
class Guess(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    value = models.CharField(max_length=6)
    correct_bitmask = models.CharField(max_length=4, default='0'*4)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

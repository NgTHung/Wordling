from rest_framework import serializers
from api.models import Game, Guess, NightmareGame, NightmareGuess, NightmareGuess
from django.contrib.auth.models import User

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['user', 'pallet', 'status', 'created_at', 'updated_at', 'correct_bitmask']
        read_only_fields = ['user', 'created_at', 'updated_at', 'correct_bitmask']

class GuessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guess
        fields = ['game', 'value']      
        read_only_fields = ['game', 'value', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    games = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Game.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "games"]
        read_only_fields = ['id', 'username', 'games', 'password', 'email']

class NightmareGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = NightmareGame
        fields = ['user', 'pallet', 'status', 'created_at', 'updated_at', 'challenge', 'challenge_value', 'correct_bitmask']
        read_only_fields = ['user', 'created_at', 'updated_at', 'challenge', 'challenge_value', 'correct_bitmask']

class NightmareGuessSerializer(serializers.ModelSerializer):
    class Meta:
        model = NightmareGuess
        fields = ['game', 'value', 'color_feedback']
        read_only_fields = ['game', 'value', 'color_feedback', 'created_at']
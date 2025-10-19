from rest_framework import serializers
from api.models import Game, Guess
from django.contrib.auth.models import User

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['user', 'key', 'status', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

class GuessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guess
        fields = ['game', 'value', 'is_correct']
        read_only_fields = ['game', 'value', 'is_correct', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    games = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Game.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "games"]
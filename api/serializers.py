from rest_framework import serializers
from api.models import Game, Guess
from django.contrib.auth.models import User

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['user', 'pallet', 'status', 'created_at', 'updated_at', 'is_nightmare']
        read_only_fields = ['user', 'created_at', 'updated_at', 'is_nightmare']

class GuessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guess
        fields = ['game', 'value', 'correct_bitmask']
        read_only_fields = ['game', 'value', 'correct_bitmask', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    games = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Game.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "games"]
        read_only_fields = ['id', 'username', 'games', 'password', 'email']
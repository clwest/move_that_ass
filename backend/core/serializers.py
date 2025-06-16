from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, DailyLockout, ShamePost, PaddleLog

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"

class DailyLockoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyLockout
        fields = "__all__"

class ShamePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShamePost
        fields = "__all__"

class PaddleLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaddleLog
        fields = "__all__"

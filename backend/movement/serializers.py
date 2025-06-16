from rest_framework import serializers
from django.contrib.auth.models import User

from .models import MovementChallenge, MovementSession


class MovementChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementChallenge
        fields = "__all__"


class MovementSessionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = MovementSession
        fields = "__all__"

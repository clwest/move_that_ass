from django.contrib.auth import get_user_model
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer as BaseRegisterSerializer


User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "is_verified", "date_joined")
        read_only_fields = ("email", "is_verified", "date_joined")


class CustomRegisterSerializer(BaseRegisterSerializer):
    username = None

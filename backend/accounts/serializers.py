from django.contrib.auth import get_user_model
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer as BaseRegisterSerializer


User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "is_verified", "date_joined")
        read_only_fields = ("username", "email", "is_verified", "date_joined")


from allauth.utils import generate_unique_username


class CustomRegisterSerializer(BaseRegisterSerializer):
    """Generate a username automatically from the email."""

    username = None

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        email = data.get("email")
        data["username"] = generate_unique_username([email]) if email else "user"
        return data

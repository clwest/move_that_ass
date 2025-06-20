from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from allauth.account import app_settings as allauth_account_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.socialaccount.models import EmailAddress
from allauth.utils import get_username_max_length
from dj_rest_auth.registration.serializers import RegisterSerializer as BaseRegisterSerializer


User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "is_verified", "date_joined")
        read_only_fields = ("username", "email", "is_verified", "date_joined")



class CustomRegisterSerializer(BaseRegisterSerializer):

    """Serializer requiring username, email, and passwords."""

    # No overrides needed; BaseRegisterSerializer already handles validation
    pass




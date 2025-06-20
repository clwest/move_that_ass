from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from allauth.account import app_settings as allauth_account_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.socialaccount.models import EmailAddress
from allauth.utils import get_username_max_length


User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "is_verified", "date_joined")
        read_only_fields = ("username", "email", "is_verified", "date_joined")


class CustomRegisterSerializer(serializers.Serializer):
    """Register serializer without deprecated allauth settings."""

    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_account_settings.USERNAME_MIN_LENGTH,
        required=allauth_account_settings.SIGNUP_FIELDS["username"]["required"],
    )
    email = serializers.EmailField(
        required=allauth_account_settings.SIGNUP_FIELDS["email"]["required"]
    )
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_username(self, username: str) -> str:
        return get_adapter().clean_username(username)

    def validate_email(self, email: str) -> str:
        email = get_adapter().clean_email(email)
        if allauth_account_settings.UNIQUE_EMAIL:
            if email and EmailAddress.objects.is_verified(email):
                raise serializers.ValidationError(
                    "A user is already registered with this e-mail address."
                )
        return email

    def validate_password1(self, password: str) -> str:
        return get_adapter().clean_password(password)

    def validate(self, data: dict) -> dict:
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError(
                "The two password fields didn't match."
            )
        return data

    def custom_signup(self, request, user) -> None:  # pragma: no cover - hook
        """Hook for additional signup logic."""
        pass

    def get_cleaned_data(self) -> dict:
        return {
            "username": self.validated_data.get("username", ""),
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data["password1"], user=user)
            except DjangoValidationError as exc:  # pragma: no cover - adapter raises
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
                )
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class VerifyEmailSerializer(serializers.Serializer):
    key = serializers.CharField(write_only=True)


class ResendEmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=allauth_account_settings.SIGNUP_FIELDS["email"]["required"]
    )

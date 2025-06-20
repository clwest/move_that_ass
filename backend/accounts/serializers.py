from django.contrib.auth import get_user_model
from rest_framework import serializers
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.utils import get_username_max_length
from allauth.socialaccount.models import EmailAddress
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError as DjangoValidationError
from dj_rest_auth.serializers import LoginSerializer as BaseLoginSerializer
from allauth.account import app_settings as allauth_account_settings


User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "is_verified", "date_joined")
        read_only_fields = ("username", "email", "is_verified", "date_joined")



class RegisterWithUsernameSerializer(serializers.Serializer):
    """Custom Register serializer avoiding deprecated allauth settings."""

    username = serializers.CharField(
        max_length=get_username_max_length(), required=True
    )
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_username(self, username):
        return get_adapter().clean_username(username)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if EmailAddress.objects.filter(email__iexact=email, verified=True).exists():
            raise serializers.ValidationError(
                _("A user is already registered with this e-mail address."),
            )
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError(
                _("The two password fields didn't match.")
            )
        return data

    def get_cleaned_data(self):
        return {
            "username": self.validated_data.get("username", ""),
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
        }

    def custom_signup(self, request, user):
        pass

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        try:
            adapter.clean_password(self.cleaned_data["password1"], user=user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(detail=serializers.as_serializer_error(exc))
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class NoWarnLoginSerializer(BaseLoginSerializer):
    """Login serializer using new LOGIN_METHODS setting."""

    def get_auth_user_using_allauth(self, username, email, password):
        methods = allauth_account_settings.LOGIN_METHODS
        if (
            allauth_account_settings.LoginMethod.EMAIL in methods
            and allauth_account_settings.LoginMethod.USERNAME not in methods
        ):
            return self._validate_email(email, password)
        if (
            allauth_account_settings.LoginMethod.USERNAME in methods
            and allauth_account_settings.LoginMethod.EMAIL not in methods
        ):
            return self._validate_username(username, password)
        return self._validate_username_email(username, email, password)





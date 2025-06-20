from django.contrib.auth import get_user_model
from .serializers import (
    ProfileSerializer,
    RegisterWithUsernameSerializer,
)
from dj_rest_auth.registration.serializers import (
    VerifyEmailSerializer,
    ResendEmailVerificationSerializer,
)
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import generics, permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import MethodNotAllowed
from allauth.account.views import ConfirmEmailView
from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.models import TokenModel
from dj_rest_auth.utils import jwt_encode
from allauth.account import app_settings as allauth_account_settings
from allauth.account.utils import complete_signup
from allauth.socialaccount.models import EmailAddress
from rest_framework.permissions import AllowAny

User = get_user_model()





class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user



sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters("password1", "password2")
)


class CustomRegisterView(CreateAPIView):
    """Register a new user without triggering deprecation warnings."""

    serializer_class = RegisterWithUsernameSerializer
    permission_classes = api_settings.REGISTER_PERMISSION_CLASSES
    token_model = TokenModel
    throttle_scope = "dj_rest_auth"

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_response_data(self, user):
        if (
            allauth_account_settings.EMAIL_VERIFICATION
            == allauth_account_settings.EmailVerificationMethod.MANDATORY
        ):
            return {"detail": _("Verification e-mail sent.")}

        if api_settings.USE_JWT:
            data = {
                "user": user,
                "access": self.access_token,
                "refresh": self.refresh_token,
            }
            return api_settings.JWT_SERIALIZER(
                data, context=self.get_serializer_context()
            ).data
        elif self.token_model:
            return api_settings.TOKEN_SERIALIZER(
                user.auth_token, context=self.get_serializer_context()
            ).data
        return None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = self.get_response_data(user)
        if data:
            response = Response(
                data, status=status.HTTP_201_CREATED, headers=headers
            )
        else:
            response = Response(status=status.HTTP_204_NO_CONTENT, headers=headers)
        return response

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        if (
            allauth_account_settings.EMAIL_VERIFICATION
            != allauth_account_settings.EmailVerificationMethod.MANDATORY
        ):
            if api_settings.USE_JWT:
                self.access_token, self.refresh_token = jwt_encode(user)
            elif self.token_model:
                api_settings.TOKEN_CREATOR(self.token_model, user, serializer)

        complete_signup(
            self.request._request,
            user,
            allauth_account_settings.EMAIL_VERIFICATION,
            None,
        )
        return user


class VerifyEmailView(APIView, ConfirmEmailView):
    """Verifies the email associated with the provided key."""

    permission_classes = (AllowAny,)
    allowed_methods = ("POST", "OPTIONS", "HEAD")

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)

    def get(self, *args, **kwargs):
        raise MethodNotAllowed("GET")

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs["key"] = serializer.validated_data["key"]
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({"detail": _("ok")}, status=status.HTTP_200_OK)


class ResendEmailVerificationView(CreateAPIView):
    """Resends another email to an unverified email."""

    permission_classes = (AllowAny,)
    serializer_class = ResendEmailVerificationSerializer
    queryset = EmailAddress.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = self.get_queryset().filter(**serializer.validated_data).first()
        if email and not email.verified:
            email.send_confirmation(request)

        return Response({"detail": _("ok")}, status=status.HTTP_200_OK)

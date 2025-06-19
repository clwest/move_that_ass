from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from .serializers import ProfileSerializer
from .serializers import CustomRegisterSerializer
from dj_rest_auth.registration.views import RegisterView as BaseRegisterView

User = get_user_model()





class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class CustomRegisterView(BaseRegisterView):
    serializer_class = CustomRegisterSerializer

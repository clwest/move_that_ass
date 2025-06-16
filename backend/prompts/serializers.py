from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Prompt, PromptResponse


class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = "__all__"


class PromptResponseSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = PromptResponse
        fields = "__all__"

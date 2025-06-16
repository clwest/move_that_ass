from rest_framework import serializers

from .models import GeneratedImage, SocialPost, GeneratedMeme


class GeneratedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedImage
        fields = "__all__"


class SocialPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialPost
        fields = "__all__"


class GeneratedMemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedMeme
        fields = "__all__"

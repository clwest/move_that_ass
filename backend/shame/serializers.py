from rest_framework import serializers
from .models import (
    Badge,
    DailyLockout,
    ShamePost,
    Herd,
    BadgeShoutout,
    DonkeyChallenge,
    HerdPost,
)


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = "__all__"


class DailyLockoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyLockout
        fields = "__all__"
        read_only_fields = ["user", "date"]


class ShamePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShamePost
        fields = "__all__"
        read_only_fields = ["user", "date"]


class HerdSerializer(serializers.ModelSerializer):
    members = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="username"
    )

    class Meta:
        model = Herd
        fields = "__all__"
        read_only_fields = ["created_by", "created_at", "invite_code"]


class BadgeShoutoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = BadgeShoutout
        fields = "__all__"
        read_only_fields = ["user", "created_at"]


class DonkeyChallengeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    issued_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = DonkeyChallenge
        fields = "__all__"
        read_only_fields = ["user", "issued_at"]


class HerdPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = HerdPost
        fields = "__all__"
        read_only_fields = ["user", "created_at"]

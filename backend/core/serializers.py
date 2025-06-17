from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Profile,
    DailyLockout,
    ShamePost,
    PaddleLog,
    VoiceJournal,
    Herd,
    Badge,
    BadgeShoutout,
    WorkoutLog,
    MovementGoal,
    DonkeyChallenge,
    HerdPost,
    DailyGoal,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    badges = BadgeSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"


class DailyLockoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyLockout
        fields = "__all__"


class ShamePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShamePost
        fields = "__all__"


class PaddleLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaddleLog
        fields = "__all__"


class VoiceJournalSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = VoiceJournal
        fields = "__all__"
        read_only_fields = [
            "user",
            "transcript",
            "summary",
            "playback_audio_url",
            "created_at",
        ]


class HerdSerializer(serializers.ModelSerializer):
    members = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="username"
    )

    class Meta:
        model = Herd
        fields = "__all__"


class BadgeShoutoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = BadgeShoutout
        fields = "__all__"


class WorkoutLogSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = WorkoutLog
        fields = "__all__"
        read_only_fields = ["user", "created_at"]


class MovementGoalSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    current_count = serializers.IntegerField(read_only=True)
    is_completed = serializers.BooleanField(read_only=True)
    is_failed = serializers.BooleanField(read_only=True)

    class Meta:
        model = MovementGoal
        fields = "__all__"
        read_only_fields = [
            "user",
            "created_at",
            "current_count",
            "is_completed",
            "is_failed",
        ]


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


class DailyGoalSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    created_at = serializers.DateTimeField(read_only=True)


    class Meta:
        model = DailyGoal
        fields = "__all__"

        read_only_fields = ["user", "created_at"]


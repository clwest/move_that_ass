from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Profile,
    PaddleLog,
    WorkoutLog,
    MovementGoal,
    DailyGoal,
)


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    badges = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ["user"]

    def get_badges(self, obj):
        from shame.serializers import BadgeSerializer

        return BadgeSerializer(obj.badges.all(), many=True).data


class PaddleLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaddleLog
        fields = "__all__"
        read_only_fields = ["user", "date"]


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


class DailyGoalSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = DailyGoal
        fields = "__all__"

        read_only_fields = ["user", "created_at", "date"]

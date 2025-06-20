from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets

User = get_user_model()
import uuid
from datetime import datetime, time, timedelta

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from content.models import GeneratedMeme
from shame.models import DailyLockout, DonkeyChallenge, Herd, ShamePost
from shame.serializers import (BadgeSerializer, BadgeShoutoutSerializer,
                               DailyLockoutSerializer,
                               DonkeyChallengeSerializer, HerdPostSerializer,
                               HerdSerializer, ShamePostSerializer)
from shame.utils.herdmood_engine import evaluate_herd_mood
from shame.utils.shame_engine import check_and_trigger_shame
from voice_journals.models import VoiceJournal
from voice_journals.serializers import VoiceJournalSerializer

from .models import DailyGoal, MovementGoal, PaddleLog, Profile, WorkoutLog
from .serializers import (DailyGoalSerializer, MovementGoalSerializer,
                          PaddleLogSerializer, ProfileSerializer,
                          UserSerializer, WorkoutLogSerializer)
from .utils.mood_avatar import get_mood_avatar
from .utils.mood_engine import evaluate_user_mood


def generate_invite_code():
    return uuid.uuid4().hex[:8]


class UserViewSet(viewsets.ModelViewSet):
    """CRUD operations for Django auth users."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class ProfileViewSet(viewsets.ModelViewSet):
    """Manage Profile objects for users."""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]


class PaddleLogViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for paddle session logs."""

    queryset = PaddleLog.objects.all()
    serializer_class = PaddleLogSerializer
    permission_classes = [IsAuthenticated]


class CurrentProfileView(generics.RetrieveUpdateAPIView):
    """Retrieve or update the authenticated user's profile."""

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def register_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password required"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    user = User.objects.create_user(username=username, password=password)
    Token.objects.create(user=user)
    return Response({"message": "User created"}, status=status.HTTP_201_CREATED)


class CustomAuthToken(ObtainAuthToken):
    """Return an auth token for a given user."""

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data["token"])
        return Response({"token": token.key})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """Delete the auth token for the current user."""
    request.user.auth_token.delete()
    return Response(status=204)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_feed(request):
    """Return a unified activity feed for the dashboard."""

    user = request.user
    mine_only = request.GET.get("mine_only") == "true"
    herd_only = request.GET.get("herd_only") == "true"
    type_filter = request.GET.get("type")

    try:
        limit = int(request.GET.get("limit", 20))
        offset = int(request.GET.get("offset", 0))
    except ValueError:
        limit, offset = 20, 0

    herd = user.herds.first()

    def in_herd(qs):
        if herd_only:
            if not herd:
                return qs.none()
            return qs.filter(user__in=herd.members.all())
        return qs

    def apply_filters(qs):
        qs = qs.order_by("-id")
        if mine_only:
            qs = qs.filter(user=user)
        return in_herd(qs)

    feed_items = []

    if not type_filter or type_filter == "shame":
        for post in apply_filters(ShamePost.objects.all()):
            dt = datetime.combine(post.date, time.min)
            dt = timezone.make_aware(dt, timezone.utc) if timezone.is_naive(dt) else dt
            item = {
                "type": "shame",
                "created_at": dt,
                "content": {
                    "text": post.caption,
                    "image_url": post.image_url,
                },
            }
            if herd and herd.members.filter(id=post.user_id).exists():
                item["content"]["herd"] = herd.name
            feed_items.append(item)

    if not type_filter or type_filter == "meme":
        for meme in apply_filters(GeneratedMeme.objects.all()):
            dt = meme.created_at
            item = {
                "type": "meme",
                "created_at": dt,
                "content": {
                    "caption": meme.caption,
                    "image_url": meme.image_url,
                },
            }
            if herd and herd.members.filter(id=meme.user_id).exists():
                item["content"]["herd"] = herd.name
            feed_items.append(item)

    if not type_filter or type_filter == "voice":
        for journal in apply_filters(VoiceJournal.objects.all()):
            dt = journal.created_at
            item = {
                "type": "voice",
                "created_at": dt,
                "content": {
                    "audio_url": journal.playback_audio_url,
                    "tags": journal.tags or [],
                    "text": journal.summary,
                },
            }
            if herd and herd.members.filter(id=journal.user_id).exists():
                item["content"]["herd"] = herd.name
            feed_items.append(item)

    feed_items.sort(key=lambda x: x["created_at"], reverse=True)

    sliced = feed_items[offset : offset + limit]
    for item in sliced:
        item["created_at"] = item["created_at"].isoformat()

    return Response(sliced)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_mood(request):
    profile = request.user.profile
    mood = evaluate_user_mood(request.user)
    profile.current_mood = mood
    profile.mood_last_updated = timezone.now()
    profile.save()
    return Response({"mood": mood})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_mood_avatar_view(request):
    """Return the user's current mood and corresponding avatar."""
    mood = request.user.profile.current_mood
    avatar = get_mood_avatar(mood)
    return Response({"mood": mood, "avatar": avatar})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_movement_goal(request):
    """Create a MovementGoal for the authenticated user."""

    serializer = MovementGoalSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    goal = serializer.save(user=request.user, is_completed=False)
    return Response(MovementGoalSerializer(goal).data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def daily_goal_view(request):
    """Get or set today's simple goal."""

    today = timezone.now().date()

    if request.method == "POST":
        serializer = DailyGoalSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        obj, _ = DailyGoal.objects.update_or_create(
            user=request.user,
            date=today,
            defaults={
                "goal": serializer.validated_data.get("goal"),
                "target": serializer.validated_data.get("target", 1),
                "goal_type": serializer.validated_data.get("goal_type", "daily"),
            },
        )
    else:
        obj = DailyGoal.objects.filter(user=request.user, date=today).first()
        if not obj:
            return Response({"goal": None})

    return Response(
        {
            "goal": obj.goal,
            "target": obj.target,
            "type": obj.goal_type,
            "date": obj.date.isoformat(),
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def log_workout(request):
    """Create a WorkoutLog entry for the authenticated user."""

    serializer = WorkoutLogSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    workout = serializer.save(user=request.user)

    # Update any goals that match this workout
    matching_goals = MovementGoal.objects.filter(
        user=request.user,
        activity_type=workout.activity_type,
        start_date__lte=workout.created_at.date(),
        end_date__gte=workout.created_at.date(),
        is_completed=False,
        is_failed=False,
    )

    for goal in matching_goals:
        goal.current_count += 1
        if goal.current_count >= goal.target_sessions:
            goal.is_completed = True
        goal.save()

    return Response(WorkoutLogSerializer(workout).data)


from .utils.digest_engine import generate_daily_digest
from .utils.meal_engine import generate_meal_plan as ai_generate_meal_plan
from .utils.plan_engine import \
    generate_workout_plan as ai_generate_workout_plan

try:  # Celery may be optional in some setups
    from .tasks import generate_meal_plan_task, generate_plan_task
except Exception:  # pragma: no cover - missing Celery
    generate_plan_task = None
    generate_meal_plan_task = None


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_workout_plan(request):
    """Return a 7-day workout plan generated by OpenAI."""
    goal = request.data.get("goal", "")
    activity_types = request.data.get("activity_types") or []
    tone = request.data.get("tone", "supportive")

    if not isinstance(activity_types, list):
        activity_types = [str(activity_types)] if activity_types else []

    task = generate_plan_task.delay(goal, activity_types, tone)
    return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_meal_plan_view(request):
    """Return a meal plan generated by OpenAI."""
    goal = request.data.get("goal", "")
    tone = request.data.get("tone", "supportive")
    mood = request.data.get("mood")

    task = generate_meal_plan_task.delay(goal, tone, mood)
    return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)


class TaskStatusView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        from django_celery_results.models import TaskResult

        result = TaskResult.objects.filter(task_id=str(task_id)).first()
        if not result:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response({"state": result.status, "data": result.result})

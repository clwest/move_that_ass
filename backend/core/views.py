from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime, time, timedelta

from .utils.shame_engine import check_and_trigger_shame

from .utils.voice_helpers import (
    transcribe_audio,
    summarize_text,
    generate_tags_from_text,
)
from .utils.tts_helpers import text_to_speech
from .utils.mood_engine import evaluate_user_mood
from .utils.mood_avatar import get_mood_avatar
from .utils.badge_engine import evaluate_badges


from .utils.herdmood_engine import evaluate_herd_mood

import uuid


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
from content.models import GeneratedMeme
from .serializers import (
    ProfileSerializer,
    DailyLockoutSerializer,
    ShamePostSerializer,
    PaddleLogSerializer,
    VoiceJournalSerializer,
    UserSerializer,
    HerdSerializer,
    BadgeSerializer,
    BadgeShoutoutSerializer,
    WorkoutLogSerializer,
    MovementGoalSerializer,
    DonkeyChallengeSerializer,
    HerdPostSerializer,
    DailyGoalSerializer,
)


def generate_invite_code():
    return uuid.uuid4().hex[:8]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]


class DailyLockoutViewSet(viewsets.ModelViewSet):
    queryset = DailyLockout.objects.all()
    serializer_class = DailyLockoutSerializer
    permission_classes = [IsAuthenticated]


class ShamePostViewSet(viewsets.ModelViewSet):
    queryset = ShamePost.objects.all()
    serializer_class = ShamePostSerializer
    permission_classes = [IsAuthenticated]


class PaddleLogViewSet(viewsets.ModelViewSet):
    queryset = PaddleLog.objects.all()
    serializer_class = PaddleLogSerializer
    permission_classes = [IsAuthenticated]


@api_view(["POST"])
@permission_classes([AllowAny])
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
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data["token"])
        return Response({"token": token.key})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_voice_journal(request):
    audio_file = request.FILES.get("audio_file")
    if not audio_file:
        return Response({"error": "audio_file is required"}, status=400)

    journal = VoiceJournal.objects.create(user=request.user, audio_file=audio_file)

    transcript = transcribe_audio(journal.audio_file.path)
    summary = summarize_text(transcript)
    tags = generate_tags_from_text(transcript)

    journal.transcript = transcript
    journal.summary = summary

    filename = f"journal_audio_{uuid.uuid4().hex}.mp3"
    output_path = f"media/voice_playback/{filename}"

    tts_path = text_to_speech(journal.summary, output_path)
    if tts_path:
        journal.playback_audio_url = f"/media/voice_playback/{filename}"

    journal.save()

    serializer = VoiceJournalSerializer(journal)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def trigger_shame_view(request):
    post = check_and_trigger_shame(request.user)
    if not post:
        return Response(
            {"message": "No shame triggered. You're safe... for now."}, status=200
        )
    return Response(
        {
            "message": "Shame post created.",
            "caption": post.caption,
            "image_url": post.image_url,
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_herd(request):
    name = request.data.get("name")
    tone = request.data.get("tone", "mixed")
    invite_code = generate_invite_code()

    # user can only be in one herd at a time
    for herd in request.user.herds.all():
        herd.members.remove(request.user)

    herd = Herd.objects.create(
        name=name, tone=tone, created_by=request.user, invite_code=invite_code
    )
    herd.members.add(request.user)
    return Response(HerdSerializer(herd).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def join_herd(request):
    code = request.data.get("invite_code")
    herd = get_object_or_404(Herd, invite_code=code)

    for h in request.user.herds.all():
        h.members.remove(request.user)

    herd.members.add(request.user)
    return Response({"message": f"Joined herd: {herd.name}"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def leave_herd(request):
    for herd in request.user.herds.all():
        herd.members.remove(request.user)
    return Response({"message": "Left all herds"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_herd(request):
    herd = request.user.herds.first()
    if herd:
        return Response(HerdSerializer(herd).data)
    return Response({"message": "Not in a herd"})


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


@api_view(["GET"])
@permission_classes([IsAuthenticated])

def herd_mood_view(request):
    """Return the overall mood for the user's herd."""
    herd = request.user.herds.first()
    if not herd:
        return Response({"message": "User is not in a herd."})

    mood = evaluate_herd_mood(herd)

    return Response({
        "herd": herd.name,
        "herd_size": herd.members.count(),
        "herd_mood": mood,
    })


@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def check_badges(request):
    """Evaluate badge rules for the current user and return badge list."""
    evaluate_badges(request.user)
    earned_ids = set(request.user.profile.badges.values_list("id", flat=True))
    badges = Badge.objects.filter(is_active=True)
    serialized = [
        {
            "code": b.code,
            "name": b.name,
            "emoji": b.emoji,
            "description": b.description,
            "is_earned": b.id in earned_ids,
        }
        for b in badges
    ]
    return Response(serialized)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_badges(request):
    """Return all badges with earned state for the current user."""
    earned_ids = set(request.user.profile.badges.values_list("id", flat=True))
    badges = Badge.objects.filter(is_active=True)
    serialized = [
        {
            "code": b.code,
            "name": b.name,
            "emoji": b.emoji,
            "description": b.description,
            "is_earned": b.id in earned_ids,
        }
        for b in badges
    ]
    return Response(serialized)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def share_badge(request):
    """Create a badge shoutout for the user's herd."""

    code = request.data.get("badge_code")
    message = request.data.get("message", "")
    if not code:
        return Response({"error": "badge_code is required"}, status=400)

    badge = get_object_or_404(Badge, code=code)
    herd = request.user.herds.first()

    shoutout = BadgeShoutout.objects.create(
        user=request.user, badge=badge, herd=herd, message=message
    )

    if not herd:
        return Response({"message": "Badge saved, no herd to notify."})

    return Response(
        {
            "message": "Badge shared with herd.",
            "herd": herd.name,
            "shoutout": BadgeShoutoutSerializer(shoutout).data,
        }
    )


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


from .utils.plan_engine import generate_workout_plan as ai_generate_workout_plan
from .utils.meal_engine import generate_meal_plan as ai_generate_meal_plan
from .utils.challenge_engine import generate_challenge as ai_generate_challenge
from .utils.digest_engine import generate_daily_digest


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_workout_plan(request):
    """Return a 7-day workout plan generated by OpenAI."""
    goal = request.data.get("goal", "")
    activity_types = request.data.get("activity_types") or []
    tone = request.data.get("tone", "supportive")

    if not isinstance(activity_types, list):
        activity_types = [str(activity_types)] if activity_types else []

    plan = ai_generate_workout_plan(goal=goal, activity_types=activity_types, tone=tone)
    return Response(plan)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_meal_plan_view(request):
    """Return a meal plan generated by OpenAI."""
    goal = request.data.get("goal", "")
    tone = request.data.get("tone", "supportive")
    mood = request.data.get("mood")

    plan = ai_generate_meal_plan(goal=goal, tone=tone, mood=mood)
    return Response(plan)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_donkey_challenge(request):
    """Generate and store a short donkey challenge for the user."""

    tone = request.data.get("tone") or "mixed"
    user = request.user

    today = timezone.now().date()
    last_week = today - timedelta(days=7)

    missed_workouts = DailyLockout.objects.filter(
        user=user, date__gte=last_week, is_unlocked=False
    ).count()
    shame_count = ShamePost.objects.filter(
        user=user, date__gte=today - timedelta(days=3)
    ).count()

    herd = user.herds.first()
    herd_size = herd.members.count() if herd else 0
    mood = user.profile.current_mood

    data = ai_generate_challenge(
        mood=mood,
        missed_workouts=missed_workouts,
        shame_streak=shame_count,
        herd_size=herd_size,
        tone=tone,
    )

    challenge_text = data.get("challenge_text", "")
    days = int(data.get("days", 7))
    expires_at = timezone.now() + timedelta(days=days)

    challenge = DonkeyChallenge.objects.create(
        user=user,
        challenge_text=challenge_text,
        expires_at=expires_at,
        tone=data.get("tone", tone),
    )

    return Response(
        {
            "challenge_text": challenge.challenge_text,
            "expires_at": challenge.expires_at.isoformat(),
            "tone": challenge.tone,
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_today_dashboard(request):
    """Return combined data for the user's Today dashboard."""

    user = request.user

    # Mood + avatar
    mood = user.profile.current_mood
    avatar = get_mood_avatar(mood)

    # Active donkey challenge
    challenge_obj = (
        DonkeyChallenge.objects.filter(
            user=user,
            is_completed=False,
            is_failed=False,
            expires_at__gt=timezone.now(),
        )
        .order_by("-issued_at")
        .first()
    )
    challenge = (
        {
            "text": challenge_obj.challenge_text,
            "expires_at": challenge_obj.expires_at.isoformat(),
        }
        if challenge_obj
        else None
    )

    # Workout and meal plans
    try:
        workout_data = ai_generate_workout_plan(goal="", activity_types=None, tone="supportive")
        workout_plan = workout_data.get("plan")
    except Exception:  # pragma: no cover - network errors
        workout_plan = None

    try:
        meal_plan = ai_generate_meal_plan(goal="", tone="supportive", mood=mood)
    except Exception:  # pragma: no cover - network errors
        meal_plan = None

    # Recap string
    recap = generate_daily_digest(user)

    return Response(
        {
            "mood": mood,
            "mood_avatar": avatar,
            "challenge": challenge,
            "workout_plan": workout_plan,
            "meal_plan": meal_plan,
            "azz_recap": recap,
        }
    )


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """Return or update the authenticated user's profile."""

    profile = request.user.profile
    if request.method == "PUT":
        display_name = request.data.get("display_name")
        if display_name:
            profile.display_name = display_name
            profile.save()

    herd = request.user.herds.first()
    herd_name = herd.name if herd else None
    herd_size = herd.members.count() if herd else 0

    mood = profile.current_mood
    avatar = get_mood_avatar(mood)

    return Response(
        {
            "username": request.user.username,
            "display_name": profile.display_name,
            "mood": mood,
            "mood_avatar": avatar,
            "herd_name": herd_name,
            "herd_size": herd_size,
            "badges": profile.badges.count(),
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def share_to_herd(request):
    """Create a HerdPost record for the user's herd."""

    post_type = request.data.get("type")
    if post_type not in {"meme", "badge"}:
        return Response({"error": "Invalid type"}, status=400)

    HerdPost.objects.create(
        user=request.user,
        type=post_type,
        caption=request.data.get("caption", ""),
        image_url=request.data.get("image_url"),
        emoji=request.data.get("emoji", ""),
        badge_name=request.data.get("badge_name", ""),
    )

    return Response({"message": "Shared to herd"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def herd_feed(request):
    """Return latest HerdPost entries for the user's herd."""

    herd = request.user.herds.first()
    if not herd:
        return Response([])

    posts = HerdPost.objects.filter(user__in=herd.members.all()).order_by(
        "-created_at"
    )[:50]

    serialized = [
        {
            "type": p.type,
            "user": p.user.username,
            "content": {
                "caption": p.caption,
                "image_url": p.image_url,
                "emoji": p.emoji,
                "name": p.badge_name,
            },
            "created_at": p.created_at.isoformat(),
        }
        for p in posts
    ]
    return Response(serialized)

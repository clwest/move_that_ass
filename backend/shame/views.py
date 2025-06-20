import uuid
from datetime import timedelta

from django.contrib.auth import get_user_model

User = get_user_model()
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (Badge, BadgeShoutout, DailyLockout, DonkeyChallenge, Herd,
                     HerdPost, ShamePost)
from .serializers import (
    BadgeShoutoutSerializer,
    DailyLockoutSerializer,
    HerdPostSerializer,
    HerdSerializer,
    ShamePostSerializer,
)
from .utils.badge_engine import evaluate_badges
from .utils.challenge_engine import generate_challenge as ai_generate_challenge
from .utils.herdmood_engine import evaluate_herd_mood
from .utils.shame_engine import check_and_trigger_shame


class DailyLockoutViewSet(viewsets.ModelViewSet):
    queryset = DailyLockout.objects.all()
    serializer_class = DailyLockoutSerializer
    permission_classes = [IsAuthenticated]


class ShamePostViewSet(viewsets.ModelViewSet):
    queryset = ShamePost.objects.all()
    serializer_class = ShamePostSerializer
    permission_classes = [IsAuthenticated]


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def trigger_shame_view(request):
    post = check_and_trigger_shame(request.user)
    if not post:
        return Response(
            {"message": "No shame triggered. You're safe... for now."},
            status=200,
        )
    return Response(
        {
            "message": "Shame post created.",
            "caption": post.caption,
            "image_url": post.image_url,
        }
    )


def generate_invite_code():
    return uuid.uuid4().hex[:8]


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_herd(request):
    name = request.data.get("name")
    tone = request.data.get("tone", "mixed")
    invite_code = generate_invite_code()

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


@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def check_badges(request):
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
        return Response({"message": "Badge saved, no herd to notify."}, status=201)

    return Response(
        {
            "message": "Badge shared with herd.",
            "herd": herd.name,
            "shoutout": BadgeShoutoutSerializer(shoutout).data,
        },
        status=201,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def share_to_herd(request):
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
    herd = request.user.herds.first()
    if not herd:
        return Response({"results": []})

    posts = HerdPost.objects.filter(user__in=herd.members.all()).order_by("-created_at")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    serializer = HerdPostSerializer(
        page_obj.object_list, many=True, context={"request": request}
    )
    return Response({"results": serializer.data, "count": paginator.count})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_like(request, pk):
    post = get_object_or_404(HerdPost, pk=pk)
    user = request.user
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
    return Response({"like_count": post.likes.count(), "liked_by_me": liked})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def herd_mood_view(request):
    herd = request.user.herds.first()
    if not herd:
        return Response({"message": "User is not in a herd."})

    mood = evaluate_herd_mood(herd)

    return Response(
        {
            "herd": herd.name,
            "herd_size": herd.members.count(),
            "herd_mood": mood,
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_donkey_challenge(request):
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

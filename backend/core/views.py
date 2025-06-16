from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .utils.shame_engine import check_and_trigger_shame

from .utils.voice_helpers import (
    transcribe_audio,
    summarize_text,
    generate_tags_from_text,
)
from .utils.tts_helpers import text_to_speech
import uuid


from .models import (
    Profile,
    DailyLockout,
    ShamePost,
    PaddleLog,
    VoiceJournal,
    Herd,
)
from .serializers import (
    ProfileSerializer,
    DailyLockoutSerializer,
    ShamePostSerializer,
    PaddleLogSerializer,
    VoiceJournalSerializer,
    UserSerializer,
    HerdSerializer,
)


def generate_invite_code():
    return uuid.uuid4().hex[:8]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class DailyLockoutViewSet(viewsets.ModelViewSet):
    queryset = DailyLockout.objects.all()
    serializer_class = DailyLockoutSerializer


class ShamePostViewSet(viewsets.ModelViewSet):
    queryset = ShamePost.objects.all()
    serializer_class = ShamePostSerializer


class PaddleLogViewSet(viewsets.ModelViewSet):
    queryset = PaddleLog.objects.all()
    serializer_class = PaddleLogSerializer


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

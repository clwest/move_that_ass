import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from shame.models import ShamePost, Herd
from content.models import GeneratedMeme
from voice_journals.models import VoiceJournal


@pytest.mark.django_db
def test_dashboard_feed_query_count(django_assert_num_queries):
    User = get_user_model()
    user = User.objects.create_user(
        username="dash", email="d@d.com", password="pass", is_verified=True
    )
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    herd = Herd.objects.create(
        name="H", created_by=user, tone="mixed", invite_code="abc123"
    )
    herd.members.add(user)

    today = timezone.now().date()
    for i in range(4):
        ShamePost.objects.create(
            user=user, date=today, image_url=f"http://img{i}", caption="c"
        )
        GeneratedMeme.objects.create(
            user=user, image_url=f"http://m{i}", caption="c"
        )
        VoiceJournal.objects.create(
            user=user,
            audio_file=SimpleUploadedFile(f"f{i}.wav", b"a"),
            summary="s",
            playback_audio_url=f"http://a{i}",
        )

    with django_assert_num_queries(8, exact=False):
        res = client.get("/api/core/dashboard/?limit=10")

    assert res.status_code == 200
    assert len(res.data) == 10

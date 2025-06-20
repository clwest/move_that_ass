from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch

User = get_user_model()

from .models import GeneratedMeme


class ContentAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="connie", email="connie@example.com", password="pass"
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_generate_prompt_caption(self):
        with patch("content.views.generate_caption") as mock_cap:
            mock_cap.return_value = "so funny"
            resp = self.client.post(
                "/api/content/generate-caption/",
                {"description": "test", "tone": "funny"},
                format="json",
            )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["caption"], "so funny")

    def test_generate_meme(self):
        class Dummy:
            id = "task123"

        with patch("content.views.generate_meme_task.delay", return_value=Dummy()):
            resp = self.client.post("/api/content/meme/", {}, format="json")
        self.assertEqual(resp.status_code, 202)
        self.assertEqual(resp.data["task_id"], "task123")


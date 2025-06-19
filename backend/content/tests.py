from django.contrib.auth import get_user_model

User = get_user_model()
from rest_framework.test import APITestCase
from unittest.mock import patch
import unittest

from .models import GeneratedMeme


@unittest.skip("legacy tests")
class ContentAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="connie@example.com", password="pass")
        self.client.login(email="connie@example.com", password="pass")

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
        with patch("content.views.generate_meme_task", None), patch(
            "content.views.fetch_donkey_gif"
        ) as gif_mock, patch("content.views.generate_meme_caption") as caption_mock:
            gif_mock.return_value = "http://gif"
            caption_mock.return_value = "roast"
            resp = self.client.post("/api/content/generate-meme/", {}, format="json")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["image_url"], "http://gif")
        self.assertEqual(resp.data["caption"], "roast")
        self.assertEqual(GeneratedMeme.objects.count(), 1)


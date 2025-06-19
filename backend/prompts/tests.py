from django.contrib.auth import get_user_model

User = get_user_model()
from rest_framework.test import APITestCase
import unittest


@unittest.skip("legacy tests")
class PromptsAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="pro@example.com", password="pass")
        self.client.login(email="pro@example.com", password="pass")

    def test_prompt_and_response(self):
        p_resp = self.client.post(
            "/api/prompts/prompts/",
            {"text": "Do it", "category": "test"},
            format="json",
        )
        self.assertEqual(p_resp.status_code, 201)
        pid = p_resp.data["id"]

        r_resp = self.client.post(
            "/api/prompts/responses/",
            {
                "prompt": pid,
                "user": self.user.id,
                "image_url": "http://example.com/img.png",
                "caption": "cap",
            },
            format="json",
        )
        self.assertEqual(r_resp.status_code, 201)
        self.assertEqual(r_resp.data["prompt"], pid)
        self.assertEqual(r_resp.data["user"], self.user.id)


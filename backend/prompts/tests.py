from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class PromptsAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="pro", password="pass")
        self.client.login(username="pro", password="pass")

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


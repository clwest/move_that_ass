from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class PromptsAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="pro", email="pro@example.com", password="pass"
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

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


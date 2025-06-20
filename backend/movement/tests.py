from django.contrib.auth import get_user_model

User = get_user_model()
from django.utils import timezone
from rest_framework.test import APITestCase


class MovementAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="mover", email="mover@example.com", password="pass", is_verified=True
        )
        from rest_framework_simplejwt.tokens import RefreshToken

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_create_challenge_and_session(self):
        chal_resp = self.client.post(
            "/api/movement/challenges/",
            {"title": "Run", "description": "fast", "duration_minutes": 5},
            format="json",
        )
        self.assertEqual(chal_resp.status_code, 201)
        challenge_id = chal_resp.data["id"]

        sess_payload = {
            "user": self.user.id,
            "challenge": challenge_id,
            "duration": 5,
            "start_time": timezone.now().isoformat(),
            "end_time": (timezone.now() + timezone.timedelta(minutes=5)).isoformat(),
            "is_complete": True,
        }

        sess_resp = self.client.post(
            "/api/movement/sessions/", sess_payload, format="json"
        )
        self.assertEqual(sess_resp.status_code, 201)
        self.assertEqual(sess_resp.data["challenge"], challenge_id)
        self.assertEqual(sess_resp.data["user"], self.user.id)


from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.test import APITestCase

User = get_user_model()


class AuthThrottleTest(APITestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(
            username="ratelimit",
            email="ratelimit@example.com",
            password="StrongPass123",
        )

    def test_login_rate_limit(self):
        for _ in range(3):
            res = self.client.post(
                "/api/auth/login/",
                {"username": "ratelimit", "password": "wrong"},
                format="json",
            )
            self.assertEqual(res.status_code, 400)
        res = self.client.post(
            "/api/auth/login/",
            {"username": "ratelimit", "password": "wrong"},
            format="json",
        )
        self.assertEqual(res.status_code, 429)


    def test_registration_rate_limit(self):
        for i in range(3):
            res = self.client.post(
                "/api/auth/registration/",
                {

                    "username": f"rl{i}",

                    "email": f"rl{i}@example.com",
                    "password1": "StrongPass123",
                    "password2": "StrongPass123",
                },
                format="json",
            )
            self.assertEqual(res.status_code, 201)
        res = self.client.post(
            "/api/auth/registration/",
            {

                "username": "rl4",

                "email": "rl4@example.com",
                "password1": "StrongPass123",
                "password2": "StrongPass123",
            },
            format="json",
        )
        self.assertEqual(res.status_code, 429)

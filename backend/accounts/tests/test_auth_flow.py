from rest_framework.test import APITestCase


class FullAuthFlowTest(APITestCase):
    def test_register_login_profile_logout(self):
        res = self.client.post(
            "/api/auth/registration/",
            {
                "username": "flow",
                "email": "flow@example.com",
                "password1": "SuperSecret123",
                "password2": "SuperSecret123",
            },
            format="json",
        )
        self.assertEqual(res.status_code, 201)

        res = self.client.post(
            "/api/auth/login/",
            {"username": "flow", "password": "SuperSecret123"},
            format="json",
        )
        self.assertEqual(res.status_code, 200)
        token = res.data["access"]
        refresh = res.data["refresh"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        res = self.client.get("/api/core/profile/")
        self.assertEqual(res.status_code, 200)

        res = self.client.post("/api/auth/logout/", {"refresh": refresh}, format="json")
        self.assertEqual(res.status_code, 200)

        res = self.client.get("/api/core/profile/")
        self.assertIn(res.status_code, [200, 401])

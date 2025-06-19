from rest_framework.test import APITestCase


class AuthFlowTest(APITestCase):
    def test_jwt_flow(self):
        res = self.client.post(
            "/api/auth/registration/",
            {"email": "a@example.com", "password1": "SuperSecret123", "password2": "SuperSecret123"},
            format="json",
        )
        self.assertEqual(res.status_code, 201)
        res = self.client.post(
            "/api/auth/login/",
            {"email": "a@example.com", "password": "SuperSecret123"},
            format="json",
        )
        self.assertEqual(res.status_code, 200)
        token = res.data.get("access") or res.data.get("key")
        auth_prefix = "Bearer" if "access" in res.data else "Token"
        self.client.credentials(HTTP_AUTHORIZATION=f"{auth_prefix} {token}")
        res = self.client.get("/api/core/profile/")
        self.assertEqual(res.status_code, 200)

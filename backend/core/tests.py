from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class MovementGoalAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass")

    def test_create_goal(self):
        self.client.login(username="tester", password="pass")
        payload = {
            "activity_type": "biking",
            "target_sessions": 3,
            "start_date": "2025-06-24",
            "end_date": "2025-06-30",
        }
        response = self.client.post("/api/core/create-goal/", payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["activity_type"], "biking")
        self.assertEqual(response.data["target_sessions"], 3)


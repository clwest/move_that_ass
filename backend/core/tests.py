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


class WorkoutPlanAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="planner", password="pass")

    def test_generate_plan(self):
        self.client.login(username="planner", password="pass")
        payload = {
            "goal": "weight loss",
            "activity_types": ["walking"],
            "tone": "supportive",
        }

        from unittest.mock import patch

        with patch("core.views.ai_generate_workout_plan") as mock_gen:
            mock_gen.return_value = {"plan": ["Day 1: test"]}
            response = self.client.post(
                "/api/core/generate-workout-plan/",
                payload,
                format="json",
            )

        self.assertEqual(response.status_code, 200)
        self.assertIn("plan", response.data)
        self.assertEqual(response.data["plan"], ["Day 1: test"])


class MealPlanAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="eater", password="pass")

    def test_generate_meal_plan(self):
        self.client.login(username="eater", password="pass")
        payload = {"goal": "bulk", "tone": "donkey", "mood": "ashamed"}

        from unittest.mock import patch

        with patch("core.views.ai_generate_meal_plan") as mock_gen:
            mock_gen.return_value = {"breakfast": "oats", "lunch": "salad", "dinner": "steak", "snacks": ["nuts"]}
            response = self.client.post(
                "/api/core/generate-meal-plan/",
                payload,
                format="json",
            )

        self.assertEqual(response.status_code, 200)
        self.assertIn("breakfast", response.data)
        self.assertIn("lunch", response.data)
        self.assertIn("dinner", response.data)
        self.assertIn("snacks", response.data)


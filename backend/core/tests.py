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


class DonkeyChallengeAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="challenger", password="pass")
        from core.models import Profile
        Profile.objects.create(user=self.user, display_name="Challenger")

    def test_generate_challenge(self):
        from django.utils import timezone
        from core.models import DailyLockout, ShamePost, DonkeyChallenge

        today = timezone.now().date()
        DailyLockout.objects.create(user=self.user, date=today, is_unlocked=False)
        ShamePost.objects.create(
            user=self.user,
            date=today,
            image_url="http://x",
            caption="fail",
            posted_to=[],
            was_triggered=True,
        )

        self.client.login(username="challenger", password="pass")

        from unittest.mock import patch

        with patch("core.views.ai_generate_challenge") as mock_gen:
            mock_gen.return_value = {"challenge_text": "walk", "days": 3, "tone": "savage"}
            response = self.client.post(
                "/api/core/generate-challenge/",
                {"tone": "savage"},
                format="json",
            )

        self.assertEqual(response.status_code, 200)
        self.assertIn("challenge_text", response.data)

        challenge = DonkeyChallenge.objects.filter(user=self.user).first()
        self.assertIsNotNone(challenge)
        self.assertEqual(challenge.challenge_text, "walk")
        self.assertEqual(challenge.tone, "savage")


class DashboardTodayAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="dasher", password="pass")
        from core.models import Profile
        Profile.objects.create(user=self.user, display_name="Dasher")

    def test_today_dashboard(self):
        from django.utils import timezone
        from django.core.files.uploadedfile import SimpleUploadedFile
        from core.models import (
            DailyLockout,
            ShamePost,
            VoiceJournal,
            WorkoutLog,
            DonkeyChallenge,
        )

        today = timezone.now().date()
        DailyLockout.objects.create(user=self.user, date=today, is_unlocked=True)
        ShamePost.objects.create(
            user=self.user,
            date=today,
            image_url="http://x",
            caption="fail",
            posted_to=[],
            was_triggered=True,
        )
        WorkoutLog.objects.create(
            user=self.user,
            activity_type="walk",
            duration_minutes=30,
        )
        VoiceJournal.objects.create(
            user=self.user,
            audio_file=SimpleUploadedFile("test.mp3", b"abc"),
        )
        DonkeyChallenge.objects.create(
            user=self.user,
            challenge_text="Walk daily",
            expires_at=timezone.now() + timezone.timedelta(days=1),
        )

        self.client.login(username="dasher", password="pass")

        from unittest.mock import patch

        with patch("core.views.generate_daily_digest") as digest_mock, patch(
            "core.views.ai_generate_workout_plan"
        ) as plan_mock, patch("core.views.ai_generate_meal_plan") as meal_mock:
            digest_mock.return_value = "recap"
            plan_mock.return_value = {"plan": ["Day 1: move"]}
            meal_mock.return_value = {
                "breakfast": "eggs",
                "lunch": "salad",
                "dinner": "fish",
                "snacks": ["nuts"],
            }

            response = self.client.get("/api/core/dashboard-today/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("mood", response.data)
        self.assertIn("mood_avatar", response.data)
        self.assertIn("workout_plan", response.data)
        self.assertEqual(response.data["workout_plan"], ["Day 1: move"])
        self.assertIn("meal_plan", response.data)
        self.assertEqual(response.data["meal_plan"]["breakfast"], "eggs")
        self.assertIn("challenge", response.data)
        self.assertIn("azz_recap", response.data)


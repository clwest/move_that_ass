from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class AuthAPITest(APITestCase):
    def test_register_and_login(self):
        # Register new user
        response = self.client.post(
            "/api/core/register/",
            {"username": "newbie", "password": "pass"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)

        # Login and get token
        response = self.client.post(
            "/api/core/login/",
            {"username": "newbie", "password": "pass"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)
        token = response.data["token"]
        self.assertTrue(Token.objects.filter(key=token).exists())

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


class DailyGoalAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="goalie", password="pass")

    def test_set_daily_goal(self):
        self.client.login(username="goalie", password="pass")
        payload = {"goal": "journal", "target": 1, "goal_type": "daily"}
        response = self.client.post("/api/core/daily-goal/", payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["goal"], "journal")
        self.assertEqual(response.data["target"], 1)


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
        self.user.profile.display_name = "Challenger"
        self.user.profile.save()

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
        self.user.profile.display_name = "Dasher"
        self.user.profile.save()

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


class BadgeListAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="badger", password="pass")
        from core.models import Badge
        self.user.profile.display_name = "Badger"
        self.user.profile.save()
        self.badge1 = Badge.objects.create(
            code="test1", name="Test One", emoji="1", description="d"
        )
        self.badge2 = Badge.objects.create(
            code="test2", name="Test Two", emoji="2", description="d"
        )
        self.user.profile.badges.add(self.badge1)

    def test_list_badges(self):
        self.client.login(username="badger", password="pass")
        response = self.client.get("/api/core/badges/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        codes = {b["code"] for b in response.data}
        self.assertIn("test1", codes)
        self.assertIn("test2", codes)
        earned_map = {b["code"]: b["is_earned"] for b in response.data}
        self.assertTrue(earned_map["test1"])  # earned
        self.assertFalse(earned_map["test2"])  # not earned


class ProfileAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="profilr", password="pass")
        from core.models import Badge, Herd

        self.user.profile.display_name = "Donk"
        self.user.profile.save()
        self.badge = Badge.objects.create(code="b", name="B", emoji="d", description="d")
        self.user.profile.badges.add(self.badge)
        herd = Herd.objects.create(
            name="Donk Dynasty",
            created_by=self.user,
            tone="mixed",
            invite_code="abc123",
        )
        herd.members.add(self.user)

    def test_get_profile(self):
        self.client.login(username="profilr", password="pass")
        response = self.client.get("/api/core/profile/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "profilr")
        self.assertEqual(response.data["display_name"], "Donk")
        self.assertEqual(response.data["herd_name"], "Donk Dynasty")
        self.assertEqual(response.data["herd_size"], 1)
        self.assertEqual(response.data["badges"], 1)
        self.assertIn("mood_avatar", response.data)

    def test_update_display_name(self):
        self.client.login(username="profilr", password="pass")
        response = self.client.put("/api/core/profile/", {"display_name": "New"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.display_name, "New")


class HerdPostAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="herder", password="pass")
        from core.models import Herd

        self.user.profile.display_name = "Herder"
        self.user.profile.save()
        herd = Herd.objects.create(
            name="Herd One", created_by=self.user, tone="mixed", invite_code="code"
        )
        herd.members.add(self.user)

    def test_share_and_feed(self):
        self.client.login(username="herder", password="pass")

        payload = {
            "type": "meme",
            "caption": "funny",
            "image_url": "http://x.com/meme.png",
        }
        response = self.client.post("/api/core/share-to-herd/", payload, format="json")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/api/core/herd-feed/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["type"], "meme")


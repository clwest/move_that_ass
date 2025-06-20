from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
User = get_user_model()


class MovementGoalAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester", email="tester@example.com", password="pass"
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_create_goal(self):
        # user already logged in via setUp
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
        self.user = User.objects.create_user(
            username="goalie", email="goalie@example.com", password="pass"
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_set_daily_goal(self):
        # user already logged in via setUp
        payload = {"goal": "journal", "target": 1, "goal_type": "daily"}
        response = self.client.post("/api/core/daily-goal/", payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["goal"], "journal")
        self.assertEqual(response.data["target"], 1)


class WorkoutPlanAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="planner", email="planner@example.com", password="pass"
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_generate_plan(self):
        # user already logged in via setUp
        payload = {
            "goal": "weight loss",
            "activity_types": ["walking"],
            "tone": "supportive",
        }

        from unittest.mock import patch

        class Dummy:
            id = "task1"

        with patch("core.views.generate_plan_task.delay", return_value=Dummy()), patch(
            "core.views.ai_generate_workout_plan"
        ) as mock_gen:
            mock_gen.return_value = {"plan": ["Day 1: test"]}
            response = self.client.post(
                "/api/core/workout-plan/",
                payload,
                format="json",
            )

        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data["task_id"], "task1")


class MealPlanAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="eater", email="eater@example.com", password="pass"
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_generate_meal_plan(self):
        # user already logged in via setUp
        payload = {"goal": "bulk", "tone": "donkey", "mood": "ashamed"}

        from unittest.mock import patch

        class Dummy:
            id = "task2"

        with patch("core.views.generate_meal_plan_task.delay", return_value=Dummy()), patch(
            "core.views.ai_generate_meal_plan"
        ) as mock_gen:
            mock_gen.return_value = {
                "breakfast": "oats",
                "lunch": "salad",
                "dinner": "steak",
                "snacks": ["nuts"],
            }
            response = self.client.post(
                "/api/core/meal-plan/",
                payload,
                format="json",
            )

        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data["task_id"], "task2")


class DonkeyChallengeAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="challenger", email="challenger@example.com", password="pass"
        )
        self.user.profile.display_name = "Challenger"
        self.user.profile.save()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_generate_challenge(self):
        from django.utils import timezone
        from shame.models import DailyLockout, ShamePost, DonkeyChallenge

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

        # user already logged in via setUp

        from unittest.mock import patch

        with patch("shame.views.ai_generate_challenge") as mock_gen:
            mock_gen.return_value = {"challenge_text": "walk", "days": 3, "tone": "savage"}
            response = self.client.post(
                "/api/core/generate-challenge/",
                {"tone": "savage"},
                format="json",
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn("challenge_text", response.data)


class DashboardTodayAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="dasher", email="dasher@example.com", password="pass"
        )
        self.user.profile.display_name = "Dasher"
        self.user.profile.save()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_today_dashboard(self):
        from django.utils import timezone
        from django.core.files.uploadedfile import SimpleUploadedFile
        from shame.models import DailyLockout, ShamePost, DonkeyChallenge
        from voice_journals.models import VoiceJournal
        from core.models import WorkoutLog

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

        # user already logged in via setUp

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

            response = self.client.get("/api/core/dashboard/")

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)


class BadgeListAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="badger", email="badger@example.com", password="pass"
        )
        from shame.models import Badge
        self.user.profile.display_name = "Badger"
        self.user.profile.save()
        self.badge1 = Badge.objects.create(
            code="test1", name="Test One", emoji="1", description="d"
        )
        self.badge2 = Badge.objects.create(
            code="test2", name="Test Two", emoji="2", description="d"
        )
        self.user.profile.badges.add(self.badge1)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_list_badges(self):
        # user already logged in via setUp
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
        self.user = User.objects.create_user(
            username="profilr", email="profilr@example.com", password="pass"
        )
        from shame.models import Badge, Herd

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
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_get_profile(self):
        # user already logged in via setUp
        response = self.client.get("/api/core/profile/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["display_name"], "Donk")
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"]["username"], "profilr")

    def test_update_display_name(self):
        # user already logged in via setUp
        response = self.client.put("/api/core/profile/", {"display_name": "New"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.display_name, "New")


class HerdPostAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="herder", email="herder@example.com", password="pass"
        )
        from shame.models import Herd

        self.user.profile.display_name = "Herder"
        self.user.profile.save()
        herd = Herd.objects.create(
            name="Herd One", created_by=self.user, tone="mixed", invite_code="code"
        )
        herd.members.add(self.user)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_share_and_feed(self):
        # user already logged in via setUp

        payload = {
            "type": "meme",
            "caption": "funny",
            "image_url": "http://x.com/meme.png",
        }
        response = self.client.post("/api/core/share-to-herd/", payload, format="json")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/api/core/herd-feed/")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["type"], "meme")


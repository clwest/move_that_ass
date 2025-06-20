import json
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django_celery_results.models import TaskResult
from rest_framework.test import APITestCase

User = get_user_model()


class AsyncEndpointsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="asyncuser",
            email="async@example.com",
            password="pass",
            is_verified=True,
        )
        from rest_framework_simplejwt.tokens import RefreshToken

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def _mock_success(self, task_id, payload):
        TaskResult.objects.update_or_create(
            task_id=task_id,
            defaults={"status": "SUCCESS", "result": json.dumps(payload)},
        )

    def _check_status(self, task_id, payload):
        self._mock_success(task_id, payload)
        res = self.client.get(f"/api/core/tasks/{task_id}/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["state"], "SUCCESS")
        self.assertEqual(res.data["data"], json.dumps(payload))

    def test_workout_plan_kickoff(self):
        with patch("core.views.generate_plan_task.delay") as mock_delay:
            mock_delay.return_value.id = "11111111-1111-1111-1111-111111111111"
            res = self.client.post(
                "/api/core/workout-plan/", {"goal": "fit"}, format="json"
            )
        self.assertEqual(res.status_code, 202)
        tid = res.data["task_id"]
        self.assertEqual(tid, "11111111-1111-1111-1111-111111111111")
        self._check_status(tid, {"plan": []})

    def test_meal_plan_kickoff(self):
        with patch("core.views.generate_meal_plan_task.delay") as mock_delay:
            mock_delay.return_value.id = "22222222-2222-2222-2222-222222222222"
            res = self.client.post(
                "/api/core/meal-plan/", {"goal": "fit"}, format="json"
            )
        self.assertEqual(res.status_code, 202)
        tid = res.data["task_id"]
        self.assertEqual(tid, "22222222-2222-2222-2222-222222222222")
        self._check_status(tid, {"meal": []})

    def test_meme_kickoff(self):
        with patch("content.views.generate_meme_task.delay") as mock_delay:
            mock_delay.return_value.id = "33333333-3333-3333-3333-333333333333"
            res = self.client.post(
                "/api/content/meme/", {"tone": "funny"}, format="json"
            )
        self.assertEqual(res.status_code, 202)
        tid = res.data["task_id"]
        self.assertEqual(tid, "33333333-3333-3333-3333-333333333333")
        self._check_status(tid, {"caption": "ok"})

    def test_voice_transcribe_kickoff(self):
        audio = SimpleUploadedFile("t.wav", b"hi")
        with patch(
            "voice_journals.views.process_voice_journal_task.delay"
        ) as mock_delay:
            mock_delay.return_value.id = "44444444-4444-4444-4444-444444444444"
            res = self.client.post("/api/voice/transcribe/", {"audio_file": audio})
        self.assertEqual(res.status_code, 202)
        tid = res.data["task_id"]
        self.assertEqual(tid, "44444444-4444-4444-4444-444444444444")
        self._check_status(tid, {"voice": "done"})

    def test_celery_ping(self):
        self.client.credentials()  # drop auth
        res = self.client.get("/api/core/celery-ping/")
        self.assertEqual(res.status_code, 401)

        with patch("core.views.celery_app.control.ping") as mock_ping:
            mock_ping.return_value = ["pong"]
            for _ in range(10):
                res = self.client.get("/api/core/celery-ping/")
                self.assertEqual(res.status_code, 200)
            res = self.client.get("/api/core/celery-ping/")
        self.assertEqual(res.status_code, 429)

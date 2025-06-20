import json
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache
from django_celery_results.models import TaskResult
from rest_framework.test import APITestCase
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from unittest.mock import patch
from django.core.cache import cache


User = get_user_model()


class VisionIdentifyTest(APITestCase):
    def setUp(self):

        cache.clear()
        self.user = User.objects.create_user(
            username="visionuser",
            email="vision@example.com",
            password="pass",
            is_verified=True,
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

    def _mock_success(self, task_id, payload):
        TaskResult.objects.update_or_create(
            task_id=task_id,
            defaults={"status": "SUCCESS", "result": json.dumps(payload)},
        )

    def test_authentication_required(self):
        img = SimpleUploadedFile("t.jpg", b"hi", content_type="image/jpeg")
        self.client.credentials()  # remove auth
        res = self.client.post("/api/vision/identify/", {"file": img})
        self.assertEqual(res.status_code, 401)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )
        with patch("vision.views.identify_image_task.delay") as mock_delay:
            mock_delay.return_value.id = "2"
            res = self.client.post("/api/vision/identify/", {"file": img})
        self.assertEqual(res.status_code, 202)

    def test_identify_kickoff_and_result(self):
        img = SimpleUploadedFile("t.jpg", b"hi", content_type="image/jpeg")
        with patch("vision.views.identify_image_task.delay") as mock_delay:
            mock_delay.return_value.id = "55555555-5555-5555-5555-555555555555"
            res = self.client.post("/api/vision/identify/", {"file": img})
        self.assertEqual(res.status_code, 202)
        tid = res.data["task_id"]
        self.assertEqual(tid, "55555555-5555-5555-5555-555555555555")
        payload = {
            "label": "oak leaf",
            "is_dangerous": False,
            "wiki_url": "http://wiki",
        }
        self._mock_success(tid, payload)
        res = self.client.get(f"/api/core/tasks/{tid}/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["state"], "SUCCESS")
        self.assertEqual(json.loads(res.data["data"]), payload)

    def test_rate_limit(self):
        from django.core.cache import cache
        cache.clear()
        with patch("vision.views.identify_image_task.delay") as mock_delay:
            mock_delay.return_value.id = "1"
            for _ in range(5):
                img = SimpleUploadedFile("t.jpg", b"hi", content_type="image/jpeg")
                res = self.client.post("/api/vision/identify/", {"file": img})
                self.assertEqual(res.status_code, 202)
            img = SimpleUploadedFile("t.jpg", b"hi", content_type="image/jpeg")
            res = self.client.post("/api/vision/identify/", {"file": img})
            self.assertEqual(res.status_code, 403)

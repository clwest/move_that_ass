import json
from django.core.files.uploadedfile import SimpleUploadedFile
from django_celery_results.models import TaskResult
from rest_framework.test import APITestCase
from unittest.mock import patch


class VisionIdentifyTest(APITestCase):
    def _mock_success(self, task_id, payload):
        TaskResult.objects.update_or_create(
            task_id=task_id, defaults={"status": "SUCCESS", "result": json.dumps(payload)}
        )

    def test_identify_kickoff_and_result(self):
        img = SimpleUploadedFile("t.jpg", b"hi", content_type="image/jpeg")
        with patch("vision.views.identify_image_task.delay") as mock_delay:
            mock_delay.return_value.id = "55555555-5555-5555-5555-555555555555"
            res = self.client.post("/api/vision/identify/", {"file": img})
        self.assertEqual(res.status_code, 202)
        tid = res.data["task_id"]
        self.assertEqual(tid, "55555555-5555-5555-5555-555555555555")
        payload = {"label": "oak leaf", "is_dangerous": False, "wiki_url": "http://wiki"}
        self._mock_success(tid, payload)
        res = self.client.get(f"/api/core/tasks/{tid}/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["state"], "SUCCESS")
        self.assertEqual(json.loads(res.data["data"]), payload)

    def test_rate_limit(self):
        with patch("vision.views.identify_image_task.delay") as mock_delay:
            mock_delay.return_value.id = "1"
            for _ in range(10):
                img = SimpleUploadedFile("t.jpg", b"hi", content_type="image/jpeg")
                res = self.client.post("/api/vision/identify/", {"file": img})
                self.assertEqual(res.status_code, 202)
            img = SimpleUploadedFile("t.jpg", b"hi", content_type="image/jpeg")
            res = self.client.post("/api/vision/identify/", {"file": img})
            self.assertEqual(res.status_code, 429)

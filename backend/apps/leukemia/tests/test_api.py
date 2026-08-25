from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from apps.analyses.models import Analysis
from apps.leukemia.inference import LeukemiaPrediction


@override_settings(MEDIA_ROOT="/tmp/limci-test-media")
class LeukemiaApiTests(TestCase):
    @patch("apps.leukemia.api.predict_leukemia")
    def test_predict_endpoint_returns_and_persists_result(self, mocked_predict):
        mocked_predict.return_value = LeukemiaPrediction(
            predicted_class="malignant",
            malignant_score=0.8,
            normal_score=0.2,
            threshold=0.5,
            inference_time_ms=12.5,
            original_width=224,
            original_height=224,
        )
        image = SimpleUploadedFile(
            "cell.png",
            b"fake-image-content",
            content_type="image/png",
        )

        response = self.client.post(
            "/api/v1/modules/leukemia/predict",
            {"file": image},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["predicted_class"], "malignant")
        self.assertEqual(response.json()["threshold"], 0.5)
        self.assertEqual(Analysis.objects.count(), 1)

    def test_predict_endpoint_requires_file(self):
        response = self.client.post("/api/v1/modules/leukemia/predict", {})

        self.assertEqual(response.status_code, 422)

    @override_settings(MAX_IMAGE_UPLOAD_BYTES=4)
    def test_predict_endpoint_rejects_large_file(self):
        image = SimpleUploadedFile(
            "cell.png",
            b"12345",
            content_type="image/png",
        )

        response = self.client.post(
            "/api/v1/modules/leukemia/predict",
            {"file": image},
        )

        self.assertEqual(response.status_code, 413)

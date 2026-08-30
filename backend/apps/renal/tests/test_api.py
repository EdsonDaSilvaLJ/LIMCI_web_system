from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from apps.renal.inference import RenalSegmentation
from apps.renal.models import RenalAnalysis


class RenalApiTests(TestCase):
    def setUp(self):
        self.media_directory = TemporaryDirectory()
        self.settings_override = override_settings(MEDIA_ROOT=self.media_directory.name)
        self.settings_override.enable()

    def tearDown(self):
        self.settings_override.disable()
        self.media_directory.cleanup()

    @patch("apps.renal.api.segment_renal_image")
    def test_segment_endpoint_returns_and_persists_result(self, mocked_segment):
        mocked_segment.return_value = RenalSegmentation(
            probability_mean=0.42,
            mask_coverage=0.25,
            threshold=0.5,
            fold=1,
            inference_time_ms=25.0,
            original_width=291,
            original_height=203,
            mask_png=b"mask-png",
            overlay_png=b"overlay-png",
        )
        image = SimpleUploadedFile("renal.jpg", b"image-content", content_type="image/jpeg")

        response = self.client.post("/api/v1/modules/renal/segment", {"file": image})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["fold"], 1)
        self.assertEqual(payload["threshold"], 0.5)
        self.assertTrue(payload["mask_url"].endswith("-mask.png"))
        self.assertTrue(payload["overlay_url"].endswith("-overlay.png"))
        self.assertEqual(RenalAnalysis.objects.count(), 1)

    def test_segment_endpoint_requires_file(self):
        response = self.client.post("/api/v1/modules/renal/segment", {})
        self.assertEqual(response.status_code, 422)

    @override_settings(MAX_IMAGE_UPLOAD_BYTES=4)
    def test_segment_endpoint_rejects_large_file(self):
        image = SimpleUploadedFile("renal.png", b"12345", content_type="image/png")
        response = self.client.post("/api/v1/modules/renal/segment", {"file": image})
        self.assertEqual(response.status_code, 413)

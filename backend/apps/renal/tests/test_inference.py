from io import BytesIO
from unittest.mock import Mock, patch

import numpy as np
from django.test import SimpleTestCase, override_settings
from PIL import Image

from apps.renal.exceptions import InvalidModelOutputError
from apps.renal.inference import segment_renal_image


class RenalInferenceTests(SimpleTestCase):
    @staticmethod
    def create_image_bytes():
        image = Image.new("RGB", (32, 24), color=(220, 180, 190))
        image_buffer = BytesIO()
        image.save(image_buffer, format="PNG")
        return image_buffer.getvalue()

    @override_settings(RENAL_THRESHOLD=0.5, RENAL_MODEL_FOLD=1)
    @patch("apps.renal.inference.get_renal_model")
    def test_generates_binary_mask_and_overlay(self, mocked_loader):
        probability_mask = np.zeros((1, 224, 224, 1), dtype=np.float32)
        probability_mask[:, :112, :, :] = 0.8
        model = Mock()
        model.predict.return_value = probability_mask
        mocked_loader.return_value = model

        result = segment_renal_image(self.create_image_bytes())

        self.assertAlmostEqual(result.mask_coverage, 0.5)
        self.assertAlmostEqual(result.probability_mean, 0.4, places=5)
        self.assertEqual(result.fold, 1)
        self.assertEqual(Image.open(BytesIO(result.mask_png)).mode, "L")
        self.assertEqual(Image.open(BytesIO(result.overlay_png)).mode, "RGB")

    @patch("apps.renal.inference.get_renal_model")
    def test_rejects_unexpected_output_shape(self, mocked_loader):
        model = Mock()
        model.predict.return_value = np.zeros((1, 1), dtype=np.float32)
        mocked_loader.return_value = model

        with self.assertRaises(InvalidModelOutputError):
            segment_renal_image(self.create_image_bytes())

from io import BytesIO
from unittest.mock import Mock, patch

import numpy as np
from django.test import SimpleTestCase
from PIL import Image

from apps.leukemia.inference import predict_leukemia


class InferenceTests(SimpleTestCase):
    @staticmethod
    def create_image_bytes():
        image = Image.new("RGB", (32, 32), color="white")
        image_buffer = BytesIO()
        image.save(image_buffer, format="PNG")
        return image_buffer.getvalue()

    @patch("apps.leukemia.inference.get_leukemia_model")
    @patch("apps.leukemia.inference.get_inference_config")
    def test_predicts_malignant_using_configured_threshold(
        self,
        mocked_config,
        mocked_model_loader,
    ):
        mocked_config.return_value = {
            "image_size": [224, 224],
            "decision_threshold": 0.5,
        }
        model = Mock()
        model.predict.return_value = np.array([[0.8]], dtype=np.float32)
        mocked_model_loader.return_value = model

        result = predict_leukemia(self.create_image_bytes())

        self.assertEqual(result.predicted_class, "malignant")
        self.assertAlmostEqual(result.malignant_score, 0.8, places=6)
        self.assertAlmostEqual(result.normal_score, 0.2, places=6)
        model.predict.assert_called_once()


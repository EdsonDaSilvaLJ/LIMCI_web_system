from io import BytesIO

import numpy as np
from django.test import SimpleTestCase
from PIL import Image

from apps.renal.exceptions import InvalidImageError
from apps.renal.preprocessing import preprocess_image


class RenalPreprocessingTests(SimpleTestCase):
    def test_resizes_rgb_and_normalizes_to_zero_one(self):
        image = Image.new("RGB", (40, 30), color=(12, 100, 240))
        image_buffer = BytesIO()
        image.save(image_buffer, format="PNG")

        result = preprocess_image(image_buffer.getvalue())

        self.assertEqual(result.batch.shape, (1, 224, 224, 3))
        self.assertEqual(result.batch.dtype, np.float32)
        self.assertEqual(result.resized_rgb.dtype, np.uint8)
        self.assertEqual((result.original_width, result.original_height), (40, 30))
        self.assertGreaterEqual(float(result.batch.min()), 0.0)
        self.assertLessEqual(float(result.batch.max()), 1.0)

    def test_rejects_invalid_file(self):
        with self.assertRaises(InvalidImageError):
            preprocess_image(b"not-an-image")

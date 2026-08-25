from io import BytesIO

import numpy as np
from django.test import SimpleTestCase
from PIL import Image

from apps.leukemia.exceptions import InvalidImageError
from apps.leukemia.preprocessing import preprocess_image


class PreprocessingTests(SimpleTestCase):
    def test_prepares_rgb_batch_without_external_normalization(self):
        image = Image.new("RGB", (40, 30), color=(12, 100, 240))
        image_buffer = BytesIO()
        image.save(image_buffer, format="PNG")

        result = preprocess_image(image_buffer.getvalue())

        self.assertEqual(result.batch.shape, (1, 224, 224, 3))
        self.assertEqual(result.batch.dtype, np.float32)
        self.assertEqual(result.original_width, 40)
        self.assertEqual(result.original_height, 30)
        self.assertGreater(float(result.batch.max()), 1.0)

    def test_rejects_invalid_file(self):
        with self.assertRaises(InvalidImageError):
            preprocess_image(b"not-an-image")


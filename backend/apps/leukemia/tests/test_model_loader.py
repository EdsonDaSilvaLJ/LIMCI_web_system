from pathlib import Path
from tempfile import TemporaryDirectory

from django.test import SimpleTestCase, override_settings

from apps.leukemia.exceptions import ModelNotAvailableError
from apps.leukemia.model_loader import (
    clear_model_caches,
    get_inference_config,
    get_leukemia_model,
)


class ModelLoaderTests(SimpleTestCase):
    def tearDown(self):
        clear_model_caches()

    def test_reports_missing_inference_config(self):
        with TemporaryDirectory() as temporary_directory:
            missing_path = Path(temporary_directory) / "missing.json"

            with override_settings(
                LEUKEMIA_INFERENCE_CONFIG_PATH=missing_path,
            ):
                clear_model_caches()

                with self.assertRaises(ModelNotAvailableError):
                    get_inference_config()

    def test_reports_missing_model_before_importing_tensorflow(self):
        with TemporaryDirectory() as temporary_directory:
            missing_path = Path(temporary_directory) / "missing.keras"

            with override_settings(LEUKEMIA_MODEL_PATH=missing_path):
                clear_model_caches()

                with self.assertRaises(ModelNotAvailableError):
                    get_leukemia_model()

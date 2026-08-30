from pathlib import Path
from tempfile import TemporaryDirectory

from django.test import SimpleTestCase, override_settings

from apps.renal.exceptions import ModelNotAvailableError
from apps.renal.model_loader import clear_model_cache, get_renal_model


class RenalModelLoaderTests(SimpleTestCase):
    def tearDown(self):
        clear_model_cache()

    def test_reports_missing_weights_before_building_model(self):
        with TemporaryDirectory() as temporary_directory:
            missing_path = Path(temporary_directory) / "missing.h5"
            with override_settings(RENAL_MODEL_PATH=missing_path):
                clear_model_cache()
                with self.assertRaises(ModelNotAvailableError):
                    get_renal_model()

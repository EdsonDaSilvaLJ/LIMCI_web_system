from functools import lru_cache
from pathlib import Path

from django.conf import settings

from .exceptions import ModelNotAvailableError
from .model_architecture import build_renal_model


@lru_cache(maxsize=1)
def get_renal_model():
    model_path = Path(settings.RENAL_MODEL_PATH)

    if not model_path.is_file():
        raise ModelNotAvailableError(
            f"Pesos do modelo renal não encontrados: {model_path}"
        )

    try:
        model = build_renal_model(input_shape=(224, 224, 3))
        model.load_weights(str(model_path))
        return model
    except Exception as error:
        raise ModelNotAvailableError(
            "Não foi possível reconstruir ou carregar o modelo renal."
        ) from error


def clear_model_cache():
    get_renal_model.cache_clear()

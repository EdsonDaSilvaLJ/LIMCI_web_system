import json
from functools import lru_cache
from pathlib import Path

from django.conf import settings

from .exceptions import ModelNotAvailableError


@lru_cache(maxsize=1)
def get_inference_config():
    config_path = Path(settings.LEUKEMIA_INFERENCE_CONFIG_PATH)

    if not config_path.is_file():
        raise ModelNotAvailableError(
            f"Configuração de inferência não encontrada: {config_path}"
        )

    try:
        with config_path.open(encoding="utf-8") as config_file:
            inference_config = json.load(config_file)
    except (OSError, json.JSONDecodeError) as error:
        raise ModelNotAvailableError(
            "Não foi possível ler a configuração de inferência."
        ) from error

    threshold = inference_config.get("decision_threshold")
    image_size = inference_config.get("image_size")

    if not isinstance(threshold, (int, float)) or not 0 <= threshold <= 1:
        raise ModelNotAvailableError("Threshold de inferência inválido.")

    if image_size != [224, 224]:
        raise ModelNotAvailableError("Tamanho de entrada incompatível.")

    return inference_config


@lru_cache(maxsize=1)
def get_leukemia_model():
    model_path = Path(settings.LEUKEMIA_MODEL_PATH)

    if not model_path.is_file():
        raise ModelNotAvailableError(
            f"Modelo de leucemia não encontrado: {model_path}"
        )

    try:
        from tensorflow import keras

        return keras.models.load_model(model_path, compile=False)
    except Exception as error:
        raise ModelNotAvailableError(
            "Não foi possível carregar o modelo de leucemia."
        ) from error


def clear_model_caches():
    get_inference_config.cache_clear()
    get_leukemia_model.cache_clear()


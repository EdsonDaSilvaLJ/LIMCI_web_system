from dataclasses import dataclass
from io import BytesIO
from time import perf_counter

import numpy as np
from django.conf import settings
from PIL import Image

from .exceptions import InvalidModelOutputError
from .model_loader import get_renal_model
from .preprocessing import preprocess_image


@dataclass(frozen=True)
class RenalSegmentation:
    probability_mean: float
    mask_coverage: float
    threshold: float
    fold: int
    inference_time_ms: float
    original_width: int
    original_height: int
    mask_png: bytes
    overlay_png: bytes


def _encode_png(array, mode):
    buffer = BytesIO()
    Image.fromarray(array, mode=mode).save(buffer, format="PNG")
    return buffer.getvalue()


def segment_renal_image(image_bytes):
    threshold = float(settings.RENAL_THRESHOLD)
    if not 0 <= threshold <= 1:
        raise InvalidModelOutputError("O threshold renal deve estar entre 0 e 1.")

    preprocessed = preprocess_image(image_bytes)
    model = get_renal_model()

    started_at = perf_counter()
    raw_prediction = model.predict(preprocessed.batch, verbose=0)
    inference_time_ms = (perf_counter() - started_at) * 1000
    probability_mask = np.asarray(raw_prediction, dtype=np.float32)

    if probability_mask.shape != (1, 224, 224, 1):
        raise InvalidModelOutputError(
            "O modelo renal retornou uma máscara com formato inválido."
        )

    probability_mask = probability_mask[0, :, :, 0]
    if not np.isfinite(probability_mask).all():
        raise InvalidModelOutputError("A máscara contém valores não finitos.")
    if probability_mask.min() < 0 or probability_mask.max() > 1:
        raise InvalidModelOutputError("A máscara contém valores fora do intervalo [0, 1].")

    binary_mask = probability_mask >= threshold
    mask_image = binary_mask.astype(np.uint8) * 255

    overlay = preprocessed.resized_rgb.astype(np.float32)
    red = np.zeros_like(overlay)
    red[..., 0] = 255.0
    alpha = np.expand_dims(binary_mask.astype(np.float32) * 0.45, axis=-1)
    overlay = np.clip(overlay * (1.0 - alpha) + red * alpha, 0, 255).astype(np.uint8)

    return RenalSegmentation(
        probability_mean=float(probability_mask.mean()),
        mask_coverage=float(binary_mask.mean()),
        threshold=threshold,
        fold=int(settings.RENAL_MODEL_FOLD),
        inference_time_ms=inference_time_ms,
        original_width=preprocessed.original_width,
        original_height=preprocessed.original_height,
        mask_png=_encode_png(mask_image, "L"),
        overlay_png=_encode_png(overlay, "RGB"),
    )

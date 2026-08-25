from dataclasses import dataclass
from time import perf_counter

import numpy as np

from .exceptions import InvalidModelOutputError
from .model_loader import get_inference_config, get_leukemia_model
from .preprocessing import preprocess_image


@dataclass(frozen=True)
class LeukemiaPrediction:
    predicted_class: str
    malignant_score: float
    normal_score: float
    threshold: float
    inference_time_ms: float
    original_width: int
    original_height: int


def predict_leukemia(image_bytes):
    inference_config = get_inference_config()
    image_size = tuple(inference_config["image_size"])
    threshold = float(inference_config["decision_threshold"])
    preprocessed = preprocess_image(image_bytes, image_size=image_size)
    model = get_leukemia_model()

    started_at = perf_counter()
    raw_prediction = model.predict(preprocessed.batch, verbose=0)
    inference_time_ms = (perf_counter() - started_at) * 1000

    scores = np.asarray(raw_prediction, dtype=np.float32).reshape(-1)

    if scores.size != 1 or not np.isfinite(scores[0]):
        raise InvalidModelOutputError("O modelo retornou uma saída inválida.")

    malignant_score = float(scores[0])

    if not 0 <= malignant_score <= 1:
        raise InvalidModelOutputError("O score retornado está fora do intervalo esperado.")

    normal_score = 1.0 - malignant_score
    predicted_class = (
        "malignant" if malignant_score >= threshold else "normal"
    )

    return LeukemiaPrediction(
        predicted_class=predicted_class,
        malignant_score=malignant_score,
        normal_score=normal_score,
        threshold=threshold,
        inference_time_ms=inference_time_ms,
        original_width=preprocessed.original_width,
        original_height=preprocessed.original_height,
    )


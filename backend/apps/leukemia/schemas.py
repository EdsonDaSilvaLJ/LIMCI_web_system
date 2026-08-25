from typing import Literal
from uuid import UUID

from ninja import Schema


class LeukemiaPredictionResponse(Schema):
    analysis_id: UUID
    predicted_class: Literal["normal", "malignant"]
    malignant_score: float
    normal_score: float
    threshold: float
    inference_time_ms: float
    experimental: bool


class ErrorResponse(Schema):
    detail: str


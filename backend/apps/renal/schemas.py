from uuid import UUID

from ninja import Schema


class RenalSegmentationResponse(Schema):
    analysis_id: UUID
    mask_url: str
    overlay_url: str
    mask_mean: float
    mask_coverage: float
    threshold: float
    fold: int
    inference_time_ms: float
    experimental: bool


class ErrorResponse(Schema):
    detail: str

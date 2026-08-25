from django.conf import settings
from django.core.files.base import ContentFile
from ninja import File, Router
from ninja.files import UploadedFile

from .exceptions import (
    InvalidImageError,
    InvalidModelOutputError,
    ModelNotAvailableError,
)
from .inference import predict_leukemia
from .models import LeukemiaAnalysis
from .schemas import ErrorResponse, LeukemiaPredictionResponse


router = Router(tags=["leukemia"])


@router.post(
    "/predict",
    response={
        200: LeukemiaPredictionResponse,
        400: ErrorResponse,
        413: ErrorResponse,
        503: ErrorResponse,
    },
    summary="Classificar imagem celular",
)
def predict(request, file: File[UploadedFile]):
    if file.size and file.size > settings.MAX_IMAGE_UPLOAD_BYTES:
        return 413, {"detail": "A imagem excede o limite permitido."}

    image_bytes = file.read()

    try:
        prediction = predict_leukemia(image_bytes)
    except InvalidImageError as error:
        return 400, {"detail": str(error)}
    except (ModelNotAvailableError, InvalidModelOutputError) as error:
        return 503, {"detail": str(error)}

    analysis = LeukemiaAnalysis(
        status=LeukemiaAnalysis.Status.COMPLETED,
        predicted_class=prediction.predicted_class,
        malignant_score=prediction.malignant_score,
        normal_score=prediction.normal_score,
        decision_threshold=prediction.threshold,
        inference_time_ms=prediction.inference_time_ms,
        original_width=prediction.original_width,
        original_height=prediction.original_height,
    )
    analysis.input_image.save(
        file.name or "uploaded-image",
        ContentFile(image_bytes),
        save=False,
    )
    analysis.save()

    return {
        "analysis_id": analysis.id,
        "predicted_class": prediction.predicted_class,
        "malignant_score": prediction.malignant_score,
        "normal_score": prediction.normal_score,
        "threshold": prediction.threshold,
        "inference_time_ms": prediction.inference_time_ms,
        "experimental": True,
    }

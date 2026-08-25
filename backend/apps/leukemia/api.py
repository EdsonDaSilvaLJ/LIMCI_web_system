from django.conf import settings
from django.core.files.base import ContentFile
from ninja import File, Router
from ninja.files import UploadedFile

from apps.analyses.models import Analysis

from .exceptions import (
    InvalidImageError,
    InvalidModelOutputError,
    ModelNotAvailableError,
)
from .inference import predict_leukemia
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

    result_data = {
        "predicted_class": prediction.predicted_class,
        "malignant_score": prediction.malignant_score,
        "normal_score": prediction.normal_score,
        "threshold": prediction.threshold,
        "original_size": {
            "width": prediction.original_width,
            "height": prediction.original_height,
        },
        "experimental": True,
    }

    analysis = Analysis.objects.create(
        module=Analysis.Module.LEUKEMIA,
        status=Analysis.Status.COMPLETED,
        result_data=result_data,
        inference_time_ms=prediction.inference_time_ms,
    )
    analysis.input_image.save(
        file.name or "uploaded-image",
        ContentFile(image_bytes),
        save=True,
    )

    return {
        "analysis_id": analysis.id,
        "predicted_class": prediction.predicted_class,
        "malignant_score": prediction.malignant_score,
        "normal_score": prediction.normal_score,
        "threshold": prediction.threshold,
        "inference_time_ms": prediction.inference_time_ms,
        "experimental": True,
    }


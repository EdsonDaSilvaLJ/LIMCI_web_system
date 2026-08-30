from django.conf import settings
from ninja import File, Router
from ninja.files import UploadedFile

from .exceptions import InvalidImageError, InvalidModelOutputError, ModelNotAvailableError
from .inference import segment_renal_image
from .schemas import ErrorResponse, RenalSegmentationResponse
from .services import save_renal_analysis


router = Router(tags=["renal"])


@router.post(
    "/segment",
    response={
        200: RenalSegmentationResponse,
        400: ErrorResponse,
        413: ErrorResponse,
        503: ErrorResponse,
    },
    summary="Segmentar região glomerular",
)
def segment(request, file: File[UploadedFile]):
    if file.size and file.size > settings.MAX_IMAGE_UPLOAD_BYTES:
        return 413, {"detail": "A imagem excede o limite permitido."}

    image_bytes = file.read()
    try:
        result = segment_renal_image(image_bytes)
    except InvalidImageError as error:
        return 400, {"detail": str(error)}
    except (ModelNotAvailableError, InvalidModelOutputError) as error:
        return 503, {"detail": str(error)}

    analysis = save_renal_analysis(
        uploaded_name=file.name,
        image_bytes=image_bytes,
        segmentation=result,
    )

    return {
        "analysis_id": analysis.id,
        "mask_url": analysis.mask_image.url,
        "overlay_url": analysis.overlay_image.url,
        "mask_mean": result.probability_mean,
        "mask_coverage": result.mask_coverage,
        "threshold": result.threshold,
        "fold": result.fold,
        "inference_time_ms": result.inference_time_ms,
        "experimental": True,
    }

from pathlib import Path

from django.core.files.base import ContentFile

from .models import RenalAnalysis


def save_renal_analysis(*, uploaded_name, image_bytes, segmentation):
    base_name = Path(uploaded_name or "renal-image").stem
    analysis = RenalAnalysis(
        fold=segmentation.fold,
        threshold=segmentation.threshold,
        mask_mean=segmentation.probability_mean,
        mask_coverage=segmentation.mask_coverage,
        inference_time_ms=segmentation.inference_time_ms,
        original_width=segmentation.original_width,
        original_height=segmentation.original_height,
    )
    analysis.input_image.save(
        uploaded_name or "renal-image.png",
        ContentFile(image_bytes),
        save=False,
    )
    analysis.mask_image.save(
        f"{base_name}-mask.png",
        ContentFile(segmentation.mask_png),
        save=False,
    )
    analysis.overlay_image.save(
        f"{base_name}-overlay.png",
        ContentFile(segmentation.overlay_png),
        save=False,
    )
    analysis.save()
    return analysis

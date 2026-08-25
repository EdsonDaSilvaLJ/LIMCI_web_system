from pathlib import Path

from django.conf import settings
from ninja import Router

from .schemas import HealthResponse, ModuleResponse


router = Router(tags=["system"])


@router.get("/health", response=HealthResponse, summary="Verificar a API")
def health(request):
    return {
        "status": "ok",
        "service": "limci-web-system-api",
        "version": "1.0.0",
    }


@router.get(
    "/modules",
    response=list[ModuleResponse],
    summary="Listar módulos da aplicação",
)
def list_modules(request):
    return [
        {
            "slug": "renal",
            "name": "Segmentação renal",
            "task": "segmentation",
            "status": "integration_pending",
            "input_scope": "Imagem histológica renal ou região de interesse",
        },
        {
            "slug": "leukemia",
            "name": "Classificação de LLA-B",
            "task": "classification",
            "status": (
                "available"
                if Path(settings.LEUKEMIA_MODEL_PATH).is_file()
                else "integration_pending"
            ),
            "input_scope": "Imagem recortada de uma célula sanguínea",
        },
    ]

from ninja import NinjaAPI

from apps.core.api import router as core_router


api = NinjaAPI(
    title="LIMCI Web System API",
    version="1.0.0",
    description="API experimental da Iniciação Tecnológica.",
    urls_namespace="api-v1",
)

api.add_router("", core_router)

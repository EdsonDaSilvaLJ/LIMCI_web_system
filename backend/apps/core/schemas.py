from typing import Literal

from ninja import Schema


class HealthResponse(Schema):
    status: Literal["ok"]
    service: str
    version: str


class ModuleResponse(Schema):
    slug: str
    name: str
    task: Literal["segmentation", "classification"]
    status: Literal["integration_pending", "available"]
    input_scope: str

import uuid

from django.db import models


class Analysis(models.Model):
    class Module(models.TextChoices):
        RENAL = "renal", "Renal"
        LEUKEMIA = "leukemia", "Leucemia"

    class Status(models.TextChoices):
        COMPLETED = "completed", "Concluída"
        FAILED = "failed", "Falhou"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    module = models.CharField(max_length=20, choices=Module.choices)
    status = models.CharField(max_length=20, choices=Status.choices)
    input_image = models.ImageField(
        upload_to="analyses/%Y/%m/%d/",
        blank=True,
    )
    result_data = models.JSONField(default=dict, blank=True)
    inference_time_ms = models.FloatField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.module}:{self.id}"


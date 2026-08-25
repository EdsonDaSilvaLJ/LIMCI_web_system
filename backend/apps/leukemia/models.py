import uuid

from django.db import models


class LeukemiaAnalysis(models.Model):
    class Status(models.TextChoices):
        COMPLETED = "completed", "Concluída"
        FAILED = "failed", "Falhou"

    class PredictedClass(models.TextChoices):
        NORMAL = "normal", "Normal"
        MALIGNANT = "malignant", "Maligna"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    input_image = models.ImageField(
        upload_to="leukemia/analyses/%Y/%m/%d/",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.COMPLETED,
    )
    predicted_class = models.CharField(
        max_length=20,
        choices=PredictedClass.choices,
    )
    malignant_score = models.FloatField()
    normal_score = models.FloatField()
    decision_threshold = models.FloatField()
    inference_time_ms = models.FloatField()
    original_width = models.PositiveIntegerField()
    original_height = models.PositiveIntegerField()
    experimental = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"leukemia:{self.id}:{self.predicted_class}"

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="RenalAnalysis",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("input_image", models.ImageField(upload_to="renal/inputs/%Y/%m/%d/")),
                ("mask_image", models.ImageField(upload_to="renal/masks/%Y/%m/%d/")),
                ("overlay_image", models.ImageField(upload_to="renal/overlays/%Y/%m/%d/")),
                ("fold", models.PositiveSmallIntegerField()),
                ("threshold", models.FloatField()),
                ("mask_mean", models.FloatField()),
                ("mask_coverage", models.FloatField()),
                ("inference_time_ms", models.FloatField()),
                ("original_width", models.PositiveIntegerField()),
                ("original_height", models.PositiveIntegerField()),
                ("experimental", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]

from dataclasses import dataclass
from io import BytesIO

import numpy as np
from PIL import Image, UnidentifiedImageError

from .exceptions import InvalidImageError


@dataclass(frozen=True)
class PreprocessedImage:
    batch: np.ndarray
    resized_rgb: np.ndarray
    original_width: int
    original_height: int


def preprocess_image(image_bytes, image_size=(224, 224)):
    if not image_bytes:
        raise InvalidImageError("O arquivo de imagem está vazio.")

    try:
        with Image.open(BytesIO(image_bytes)) as image:
            image.load()
            original_width, original_height = image.size
            resized = image.convert("RGB").resize(
                image_size,
                Image.Resampling.BILINEAR,
            )
            resized_rgb = np.asarray(resized, dtype=np.uint8)
    except (UnidentifiedImageError, OSError, ValueError) as error:
        raise InvalidImageError("O arquivo enviado não é uma imagem válida.") from error

    expected_shape = (image_size[1], image_size[0], 3)
    if resized_rgb.shape != expected_shape:
        raise InvalidImageError("A imagem possui dimensões inválidas.")

    normalized = resized_rgb.astype(np.float32) / 255.0
    return PreprocessedImage(
        batch=np.expand_dims(normalized, axis=0),
        resized_rgb=resized_rgb,
        original_width=original_width,
        original_height=original_height,
    )

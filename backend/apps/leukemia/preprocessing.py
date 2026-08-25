from dataclasses import dataclass
from io import BytesIO

import numpy as np
from PIL import Image, UnidentifiedImageError

from .exceptions import InvalidImageError


@dataclass(frozen=True)
class PreprocessedImage:
    batch: np.ndarray
    original_width: int
    original_height: int


def preprocess_image(image_bytes, image_size=(224, 224)):
    if not image_bytes:
        raise InvalidImageError("O arquivo de imagem está vazio.")

    try:
        with Image.open(BytesIO(image_bytes)) as image:
            image.load()
            original_width, original_height = image.size
            image = image.convert("RGB")
            image = image.resize(image_size, Image.Resampling.BILINEAR)
            image_array = np.asarray(image, dtype=np.float32)
    except (UnidentifiedImageError, OSError, ValueError) as error:
        raise InvalidImageError("O arquivo enviado não é uma imagem válida.") from error

    if image_array.shape != (image_size[1], image_size[0], 3):
        raise InvalidImageError("A imagem possui dimensões inválidas.")

    return PreprocessedImage(
        batch=np.expand_dims(image_array, axis=0),
        original_width=original_width,
        original_height=original_height,
    )


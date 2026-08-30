class InvalidImageError(ValueError):
    """Raised when an uploaded file cannot be decoded as an image."""


class ModelNotAvailableError(RuntimeError):
    """Raised when the renal model cannot be loaded."""


class InvalidModelOutputError(RuntimeError):
    """Raised when the segmentation model returns an invalid mask."""

class InvalidImageError(ValueError):
    """Raised when an uploaded file cannot be processed as an image."""


class ModelNotAvailableError(RuntimeError):
    """Raised when model artifacts cannot be loaded."""


class InvalidModelOutputError(RuntimeError):
    """Raised when the model returns an unexpected prediction."""


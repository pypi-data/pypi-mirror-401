"""
RedenLab ML SDK

Python SDK for RedenLab's ML inference service.
"""

__version__ = "0.2.0"

from .client import (
    BaseInferenceClient,
    InferenceClient,
    IntelligibilityClient,
    TranscribeClient,
)
from .exceptions import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    InferenceError,
    RedenLabMLError,
    TimeoutError,
    UploadError,
    ValidationError,
)

__all__ = [
    # Client classes
    "InferenceClient",  # Backward compatibility (alias for BaseInferenceClient)
    "BaseInferenceClient",
    "TranscribeClient",
    "IntelligibilityClient",
    # Exceptions
    "RedenLabMLError",
    "AuthenticationError",
    "InferenceError",
    "TimeoutError",
    "APIError",
    "UploadError",
    "ValidationError",
    "ConfigurationError",
]

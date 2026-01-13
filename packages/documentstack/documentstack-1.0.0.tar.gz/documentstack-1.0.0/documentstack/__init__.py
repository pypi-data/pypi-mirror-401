"""DocumentStack SDK for Python."""
from .client import DocumentStack
from .errors import (
    APIError,
    AuthenticationError,
    DocumentStackError,
    ForbiddenError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TimeoutError,
    ValidationError,
)
from .types import (
    APIErrorResponse,
    DocumentStackConfig,
    GenerateOptions,
    GenerateRequest,
    GenerateResponse,
)

__version__ = "1.0.0"
__all__ = [
    # Client
    "DocumentStack",
    # Types
    "DocumentStackConfig",
    "GenerateOptions",
    "GenerateRequest",
    "GenerateResponse",
    "APIErrorResponse",
    # Errors
    "DocumentStackError",
    "APIError",
    "ValidationError",
    "AuthenticationError",
    "ForbiddenError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "TimeoutError",
    "NetworkError",
]

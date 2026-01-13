"""Custom exceptions for DocumentStack SDK."""
from typing import Any, Optional


class DocumentStackError(Exception):
    """Base error class for all DocumentStack SDK errors."""

    pass


class APIError(DocumentStackError):
    """Error thrown when API request fails with a specific HTTP status."""

    def __init__(
        self,
        status_code: int,
        error: str,
        message: str,
        details: Optional[Any] = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error
        self.message = message
        self.details = details

    def __str__(self) -> str:
        return f"{self.error_code}: {self.message}"


class ValidationError(APIError):
    """Error thrown when request validation fails (400)."""

    def __init__(
        self, error: str, message: str, details: Optional[Any] = None
    ) -> None:
        super().__init__(400, error, message, details)


class AuthenticationError(APIError):
    """Error thrown when authentication fails (401)."""

    def __init__(
        self, error: str, message: str, details: Optional[Any] = None
    ) -> None:
        super().__init__(401, error, message, details)


class ForbiddenError(APIError):
    """Error thrown when access is forbidden (403)."""

    def __init__(
        self, error: str, message: str, details: Optional[Any] = None
    ) -> None:
        super().__init__(403, error, message, details)


class NotFoundError(APIError):
    """Error thrown when template is not found (404)."""

    def __init__(
        self, error: str, message: str, details: Optional[Any] = None
    ) -> None:
        super().__init__(404, error, message, details)


class RateLimitError(APIError):
    """Error thrown when rate limit is exceeded (429)."""

    def __init__(
        self,
        error: str,
        message: str,
        details: Optional[Any] = None,
        retry_after: Optional[int] = None,
    ) -> None:
        super().__init__(429, error, message, details)
        self.retry_after = retry_after


class ServerError(APIError):
    """Error thrown when server encounters an error (500)."""

    def __init__(
        self, error: str, message: str, details: Optional[Any] = None
    ) -> None:
        super().__init__(500, error, message, details)


class TimeoutError(DocumentStackError):
    """Error thrown when request times out."""

    def __init__(self, timeout: float) -> None:
        super().__init__(f"Request timed out after {timeout} seconds")
        self.timeout = timeout


class NetworkError(DocumentStackError):
    """Error thrown when network request fails."""

    def __init__(self, message: str, cause: Optional[Exception] = None) -> None:
        super().__init__(message)
        self.cause = cause

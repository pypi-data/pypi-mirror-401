"""Type definitions for DocumentStack SDK."""
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class DocumentStackConfig:
    """Configuration options for the DocumentStack client."""

    api_key: str
    """API key for authentication (Bearer token)."""

    base_url: str = "https://api.documentstack.dev"
    """Base URL of the DocumentStack API."""

    timeout: float = 30.0
    """Request timeout in seconds."""

    headers: dict[str, str] = field(default_factory=dict)
    """Custom headers to include in all requests."""

    debug: bool = False
    """Enable debug logging."""


@dataclass
class GenerateOptions:
    """Options for PDF generation."""

    filename: Optional[str] = None
    """Custom filename for the generated PDF (without .pdf extension)."""


@dataclass
class GenerateRequest:
    """Request payload for PDF generation."""

    data: Optional[dict[str, Any]] = None
    """Template data for variable substitution."""

    options: Optional[GenerateOptions] = None
    """Generation options."""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result: dict[str, Any] = {}
        if self.data is not None:
            result["data"] = self.data
        if self.options is not None and self.options.filename:
            result["options"] = {"filename": self.options.filename}
        return result


@dataclass
class GenerateResponse:
    """Response from PDF generation."""

    pdf: bytes
    """PDF binary data."""

    filename: str
    """Filename from Content-Disposition header."""

    generation_time_ms: int
    """Generation time in milliseconds."""

    content_length: int
    """Content length in bytes."""


@dataclass
class APIErrorResponse:
    """Error response from the API."""

    error: str
    message: str
    details: Optional[Any] = None

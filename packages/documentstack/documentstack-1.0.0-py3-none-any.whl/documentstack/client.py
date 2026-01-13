"""DocumentStack API client for PDF generation."""
import logging
import re
from typing import Any, Optional
from urllib.parse import quote

import httpx

from .errors import (
    APIError,
    AuthenticationError,
    ForbiddenError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TimeoutError as SDKTimeoutError,
    ValidationError,
)
from .types import (
    DocumentStackConfig,
    GenerateOptions,
    GenerateRequest,
    GenerateResponse,
)


logger = logging.getLogger("documentstack")


class DocumentStack:
    """
    DocumentStack API client for PDF generation.

    Example:
        ```python
        from documentstack import DocumentStack

        client = DocumentStack(api_key="your-api-key")

        result = client.generate(
            template_id="template-id",
            data={"name": "John Doe", "amount": 100},
            filename="invoice"
        )

        # Save to file
        with open("invoice.pdf", "wb") as f:
            f.write(result.pdf)
        ```
    """

    DEFAULT_BASE_URL = "https://api.documentstack.dev"
    DEFAULT_TIMEOUT = 30.0

    def __init__(
        self,
        api_key: str,
        *,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        headers: Optional[dict[str, str]] = None,
        debug: bool = False,
    ) -> None:
        """
        Initialize the DocumentStack client.

        Args:
            api_key: API key for authentication (Bearer token).
            base_url: Base URL of the DocumentStack API.
            timeout: Request timeout in seconds.
            headers: Custom headers to include in all requests.
            debug: Enable debug logging.
        """
        if not api_key:
            raise ValueError("API key is required")

        self._config = DocumentStackConfig(
            api_key=api_key,
            base_url=(base_url or self.DEFAULT_BASE_URL).rstrip("/"),
            timeout=timeout or self.DEFAULT_TIMEOUT,
            headers=headers or {},
            debug=debug,
        )

        if debug:
            logging.basicConfig(level=logging.DEBUG)

    def generate(
        self,
        template_id: str,
        *,
        data: Optional[dict[str, Any]] = None,
        filename: Optional[str] = None,
    ) -> GenerateResponse:
        """
        Generate a PDF from a template.

        Args:
            template_id: The ID of the template to use.
            data: Template data for variable substitution.
            filename: Custom filename for the generated PDF.

        Returns:
            GenerateResponse containing the PDF and metadata.

        Raises:
            ValidationError: When request body is invalid.
            AuthenticationError: When API key is invalid.
            ForbiddenError: When access to template is forbidden.
            NotFoundError: When template is not found.
            RateLimitError: When rate limit is exceeded.
            ServerError: When server encounters an error.
            TimeoutError: When request times out.
            NetworkError: When network request fails.
        """
        if not template_id:
            raise ValidationError("Bad Request", "Template ID is required")

        url = f"{self._config.base_url}/api/v1/generate/{quote(template_id, safe='')}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._config.api_key}",
            **self._config.headers,
        }

        request = GenerateRequest(
            data=data,
            options=GenerateOptions(filename=filename) if filename else None,
        )

        if self._config.debug:
            logger.debug(f"Request: POST {url}")
            logger.debug(f"Body: {request.to_dict()}")

        try:
            with httpx.Client(timeout=self._config.timeout) as client:
                response = client.post(url, headers=headers, json=request.to_dict())
        except httpx.TimeoutException:
            raise SDKTimeoutError(self._config.timeout)
        except httpx.RequestError as e:
            raise NetworkError(f"Network request failed: {e!s}", e)

        if response.status_code != 200:
            self._raise_api_error(response)

        # Extract metadata from headers
        content_disposition = response.headers.get("Content-Disposition", "")
        generation_time_ms = int(response.headers.get("X-Generation-Time-Ms", "0"))
        content_length = int(response.headers.get("Content-Length", "0"))

        # Parse filename from Content-Disposition
        filename_match = re.search(r'filename="?([^";\n]+)"?', content_disposition)
        extracted_filename = filename_match.group(1) if filename_match else "document.pdf"

        if self._config.debug:
            logger.debug(
                f"Response: filename={extracted_filename}, time={generation_time_ms}ms"
            )

        return GenerateResponse(
            pdf=response.content,
            filename=extracted_filename,
            generation_time_ms=generation_time_ms,
            content_length=content_length or len(response.content),
        )

    def _raise_api_error(self, response: httpx.Response) -> None:
        """Parse error response and raise appropriate exception."""
        try:
            error_body = response.json()
            error = error_body.get("error", "Unknown Error")
            message = error_body.get("message", response.reason_phrase)
            details = error_body.get("details")
        except Exception:
            error = "Unknown Error"
            message = response.reason_phrase or "Request failed"
            details = None

        status_code = response.status_code
        retry_after = response.headers.get("Retry-After")

        if status_code == 400:
            raise ValidationError(error, message, details)
        elif status_code == 401:
            raise AuthenticationError(error, message, details)
        elif status_code == 403:
            raise ForbiddenError(error, message, details)
        elif status_code == 404:
            raise NotFoundError(error, message, details)
        elif status_code == 429:
            raise RateLimitError(
                error,
                message,
                details,
                retry_after=int(retry_after) if retry_after else None,
            )
        elif status_code >= 500:
            raise ServerError(error, message, details)
        else:
            raise APIError(status_code, error, message, details)

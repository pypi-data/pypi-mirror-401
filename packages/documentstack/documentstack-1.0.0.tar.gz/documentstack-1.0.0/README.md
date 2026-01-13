# documentstack

Official Python SDK for the DocumentStack PDF generation API.

## Installation

```bash
pip install documentstack
```

## Quick Start

```python
from documentstack import DocumentStack

# Initialize the client
client = DocumentStack(api_key="your-api-key")

# Generate a PDF
result = client.generate(
    template_id="template-id",
    data={
        "name": "John Doe",
        "amount": 1500,
    },
    filename="invoice",
)

# Save to file
with open(result.filename, "wb") as f:
    f.write(result.pdf)

print(f"PDF generated in {result.generation_time_ms}ms")
```

## Configuration

```python
client = DocumentStack(
    # Required: Your API key
    api_key="your-api-key",

    # Optional: Custom base URL (default: https://api.documentstack.dev)
    base_url="https://api.documentstack.dev",

    # Optional: Request timeout in seconds (default: 30.0)
    timeout=30.0,

    # Optional: Custom headers for all requests
    headers={
        "X-Custom-Header": "value",
    },

    # Optional: Enable debug logging (default: False)
    debug=False,
)
```

## API Reference

### `client.generate(template_id, *, data=None, filename=None)`

Generate a PDF from a template.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `template_id` | `str` | Yes | The ID of the template to use |
| `data` | `dict[str, Any]` | No | Template data for variable substitution |
| `filename` | `str` | No | Custom filename (without .pdf extension) |

**Returns:** `GenerateResponse`

```python
@dataclass
class GenerateResponse:
    pdf: bytes              # PDF binary data
    filename: str           # Filename from response
    generation_time_ms: int # Generation time in ms
    content_length: int     # File size in bytes
```

## Error Handling

The SDK provides typed exceptions for different failure scenarios:

```python
from documentstack import (
    DocumentStack,
    ValidationError,
    AuthenticationError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TimeoutError,
    NetworkError,
)

try:
    result = client.generate("template-id", data={})
except ValidationError as e:
    # 400: Invalid request
    print(f"Validation failed: {e.message}")
except AuthenticationError as e:
    # 401: Invalid API key
    print(f"Authentication failed: {e.message}")
except ForbiddenError as e:
    # 403: No access to template
    print(f"Access forbidden: {e.message}")
except NotFoundError as e:
    # 404: Template not found
    print(f"Template not found: {e.message}")
except RateLimitError as e:
    # 429: Rate limit exceeded
    print(f"Rate limited. Retry after {e.retry_after} seconds")
except ServerError as e:
    # 500: Server error
    print(f"Server error: {e.message}")
except TimeoutError as e:
    # Request timed out
    print("Request timed out")
except NetworkError as e:
    # Network failure
    print(f"Network error: {e}")
```

## Type Hints

This SDK is fully typed with Python type hints and supports static type checking with mypy.

```python
from documentstack import (
    DocumentStackConfig,
    GenerateRequest,
    GenerateResponse,
    GenerateOptions,
)
```

## Requirements

- Python 3.10 or higher
- httpx >= 0.24.0

## License

MIT

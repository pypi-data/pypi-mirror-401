# Infilake OpenAPI Auth SDK

Authorization SDK for generating HMAC-SHA256 signed headers.

## Installation

### Using pip

```bash
pip install infilake-openapi-auth
```

### Using uv

```bash
# Install uv (if not already installed)
# Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
# macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install
uv venv
uv pip install .

# Or install in development mode
uv pip install -e .
```

### Install from source

```bash
pip install .
```

## Development Setup with uv

```bash
# Create virtual environment with specific Python version
uv venv --python 3.11

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install with dev dependencies
uv pip install -e ".[dev]"

# Or use uv sync (reads pyproject.toml)
uv sync

# Run tests
uv run pytest
```

## Usage

```python
from infilake_openapi_auth import AuthSDK

# Initialize with your secret key
sdk = AuthSDK("your-secret-key")

# Generate headers for a request
headers = sdk.get_headers("/api/v1/resource", "POST")
print(headers)
# {'X-Timestamp': '20260116T104530Z', 'X-Authorization': 'base64...'}

# Use with requests library
import requests

url = "https://api.example.com/api/v1/resource"
auth_headers = sdk.get_headers("/api/v1/resource", "GET")
response = requests.get(url, headers=auth_headers)
```

## API

### AuthSDK(hmac_secret: str)

Initialize the SDK with your HMAC secret key.

### sdk.sign(sign_url: str, request_action: str = "GET") -> AuthResult

Generate authorization signature. Returns an `AuthResult` object with:
- `x_timestamp`: The timestamp used for signing
- `x_authorization`: The Base64-encoded HMAC-SHA256 signature

### sdk.get_headers(sign_url: str, request_action: str = "GET") -> dict

Generate headers dict ready for HTTP requests. Returns:
```python
{
    "X-Timestamp": "...",
    "X-Authorization": "..."
}
```

## License

MIT

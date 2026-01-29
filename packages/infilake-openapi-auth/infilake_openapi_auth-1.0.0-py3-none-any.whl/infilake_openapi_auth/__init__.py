"""
Infilake OpenAPI Auth SDK
Authorization SDK for generating HMAC-SHA256 signed headers
"""
import hmac
import hashlib
import base64
from datetime import datetime, timezone
from dataclasses import dataclass


__version__ = "1.0.0"
__all__ = ["AuthSDK", "AuthResult"]


@dataclass
class AuthResult:
    """Authorization result containing timestamp and signature"""
    x_timestamp: str
    x_authorization: str


class AuthSDK:
    """SDK for generating HMAC-SHA256 authorization headers"""

    def __init__(self, hmac_secret: str):
        """
        Initialize AuthSDK with HMAC secret

        Args:
            hmac_secret: The HMAC secret key
        """
        if not hmac_secret:
            raise ValueError("hmac_secret is required")
        self.hmac_secret = hmac_secret

    @staticmethod
    def generate_timestamp() -> str:
        """
        Generate timestamp in format: YYYYMMDDTHHMMSSZ

        Returns:
            Formatted timestamp string
        """
        now = datetime.now(timezone.utc)
        return now.strftime("%Y%m%dT%H%M%SZ")

    def sign(self, sign_url: str, request_action: str = "GET") -> AuthResult:
        """
        Generate authorization signature

        Args:
            sign_url: The URL to sign
            request_action: HTTP method (default: GET)

        Returns:
            AuthResult with timestamp and authorization
        """
        if not sign_url:
            raise ValueError("sign_url is required")

        timestamp = self.generate_timestamp()
        string_to_sign = f"{request_action}\n{sign_url}\n{timestamp}\n"

        signature = hmac.new(
            self.hmac_secret.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            hashlib.sha256
        ).digest()

        authorization = base64.b64encode(signature).decode('utf-8')

        return AuthResult(
            x_timestamp=timestamp,
            x_authorization=authorization
        )

    def get_headers(self, sign_url: str, request_action: str = "GET") -> dict:
        """
        Generate headers dict ready for HTTP request

        Args:
            sign_url: The URL to sign
            request_action: HTTP method (default: GET)

        Returns:
            Dict with X-Timestamp and X-Authorization headers
        """
        result = self.sign(sign_url, request_action)
        return {
            "X-Timestamp": result.x_timestamp,
            "X-Authorization": result.x_authorization
        }

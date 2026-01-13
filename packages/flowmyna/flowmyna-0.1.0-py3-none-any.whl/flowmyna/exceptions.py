"""FlowMyna SDK Exceptions.

This module defines all exception classes used by the FlowMyna SDK.
"""

from typing import Optional


class FlowMynaError(Exception):
    """Base exception for all FlowMyna SDK errors."""

    def __init__(self, message: str, status_code: Optional[int] = None) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)

    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class AuthenticationError(FlowMynaError):
    """Raised when authentication fails (401).

    This occurs when:
    - API key is missing
    - API key is invalid
    - API key has been revoked
    - API key has expired
    """

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message, status_code=401)


class ValidationError(FlowMynaError):
    """Raised when request validation fails (422).

    This occurs when:
    - Required fields are missing
    - Field values are invalid (wrong type, out of range, etc.)
    - Request body is malformed
    """

    def __init__(self, message: str = "Validation error") -> None:
        super().__init__(message, status_code=422)


class RateLimitError(FlowMynaError):
    """Raised when rate limit is exceeded (429).

    Attributes:
        retry_after: Number of seconds to wait before retrying, if provided by the server.
    """

    def __init__(
        self, message: str = "Rate limit exceeded", retry_after: Optional[int] = None
    ) -> None:
        super().__init__(message, status_code=429)
        self.retry_after = retry_after

    def __str__(self) -> str:
        base = super().__str__()
        if self.retry_after:
            return f"{base} (retry after {self.retry_after}s)"
        return base


class ServerError(FlowMynaError):
    """Raised when the server returns a 5xx error.

    This indicates a problem on the server side. The request can typically
    be retried after a short delay.
    """

    def __init__(
        self, message: str = "Server error", status_code: int = 500
    ) -> None:
        super().__init__(message, status_code=status_code)


class NetworkError(FlowMynaError):
    """Raised when a network error occurs.

    This includes connection errors, timeouts, and other transport-level failures.
    """

    def __init__(self, message: str = "Network error") -> None:
        super().__init__(message)

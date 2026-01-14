"""
Callbotics SDK Exceptions.

Custom exception classes for handling API errors.
"""

from typing import Any, Dict, Optional


class CallboticsError(Exception):
    """Base exception for all Callbotics SDK errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}

    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class AuthenticationError(CallboticsError):
    """Raised when authentication fails (401)."""

    pass


class AuthorizationError(CallboticsError):
    """Raised when access is forbidden (403)."""

    pass


class NotFoundError(CallboticsError):
    """Raised when a resource is not found (404)."""

    pass


class ValidationError(CallboticsError):
    """Raised when request validation fails (400, 422)."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        errors: Optional[list] = None,
    ):
        super().__init__(message, status_code, response_data)
        self.errors = errors or []


class ConflictError(CallboticsError):
    """Raised when there's a resource conflict (409)."""

    pass


class RateLimitError(CallboticsError):
    """Raised when rate limit is exceeded (429)."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        retry_after: Optional[int] = None,
    ):
        super().__init__(message, status_code, response_data)
        self.retry_after = retry_after


class ServerError(CallboticsError):
    """Raised when server returns 5xx error."""

    pass


class ConnectionError(CallboticsError):
    """Raised when connection to the API fails."""

    pass


class TimeoutError(CallboticsError):
    """Raised when request times out."""

    pass


class WebSocketError(CallboticsError):
    """Raised when WebSocket connection fails."""

    pass

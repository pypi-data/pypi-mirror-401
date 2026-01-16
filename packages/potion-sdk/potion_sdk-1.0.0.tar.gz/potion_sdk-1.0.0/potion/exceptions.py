"""
Potion SDK Exceptions

Exception classes for API errors.
"""

from typing import Optional, Dict, Any


class PotionError(Exception):
    """Base exception for all Potion API errors."""

    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        status_code: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        self.request_id = request_id

    def __str__(self):
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message


class AuthenticationError(PotionError):
    """Raised when authentication fails (401)."""

    pass


class AuthorizationError(PotionError):
    """Raised when authorization fails (403)."""

    pass


class RateLimitError(PotionError):
    """Raised when rate limit is exceeded (429)."""

    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        retry_after: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(message, code, 429, **kwargs)
        self.retry_after = retry_after


class ValidationError(PotionError):
    """Raised when request validation fails (400)."""

    pass


class NotFoundError(PotionError):
    """Raised when a resource is not found (404)."""

    pass


class ConflictError(PotionError):
    """Raised on version conflicts (409)."""

    pass


class ServerError(PotionError):
    """Raised on server errors (5xx)."""

    pass


def raise_for_status(response) -> None:
    """Raise appropriate exception based on response status."""
    if response.status_code < 400:
        return

    try:
        data = response.json()
        error = data.get("error", {})
        code = error.get("code", "UNKNOWN_ERROR")
        message = error.get("message", "An unknown error occurred")
        details = error.get("details", {})
        request_id = data.get("meta", {}).get("request_id")
    except Exception:
        code = "UNKNOWN_ERROR"
        message = response.text or "An unknown error occurred"
        details = {}
        request_id = None

    status = response.status_code

    if status == 401:
        raise AuthenticationError(message, code, status, details, request_id)
    elif status == 403:
        raise AuthorizationError(message, code, status, details, request_id)
    elif status == 404:
        raise NotFoundError(message, code, status, details, request_id)
    elif status == 409:
        raise ConflictError(message, code, status, details, request_id)
    elif status == 429:
        retry_after = details.get("retry_after_seconds")
        raise RateLimitError(message, code, retry_after, details=details, request_id=request_id)
    elif status >= 500:
        raise ServerError(message, code, status, details, request_id)
    elif status >= 400:
        raise ValidationError(message, code, status, details, request_id)
    else:
        raise PotionError(message, code, status, details, request_id)

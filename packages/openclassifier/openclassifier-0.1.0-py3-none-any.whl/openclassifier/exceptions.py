from __future__ import annotations

from typing import Any


class OpenClassifierError(Exception):
    """Base exception for OpenClassifier SDK."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class APIError(OpenClassifierError):
    """Error returned by the OpenClassifier API."""

    def __init__(
        self,
        message: str,
        code: str,
        status_code: int,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        self.code = code
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(message)

    def __repr__(self) -> str:
        return f"APIError(code={self.code!r}, status={self.status_code}, msg={self.message!r})"


class AuthenticationError(APIError):
    """Invalid or missing API key."""

    pass


class InvalidRequestError(APIError):
    """Request validation failed."""

    pass


class RateLimitError(APIError):
    """Rate limit exceeded."""

    pass


class InsufficientBalanceError(APIError):
    """Wallet balance too low."""

    pass


class ClassificationError(APIError):
    """Classification failed."""

    pass


class ConnectionError(OpenClassifierError):
    """Network connection error."""

    pass


class TimeoutError(OpenClassifierError):
    """Request timed out."""

    pass


ERROR_CODE_MAP = {
    "UNAUTHORIZED": AuthenticationError,
    "INVALID_REQUEST": InvalidRequestError,
    "INVALID_JSON": InvalidRequestError,
    "INVALID_CONTENT_TYPE": InvalidRequestError,
    "RATE_LIMIT_EXCEEDED": RateLimitError,
    "INSUFFICIENT_BALANCE": InsufficientBalanceError,
    "CLASSIFICATION_FAILED": ClassificationError,
    "PDF_FETCH_ERROR": InvalidRequestError,
    "INVALID_PDF": InvalidRequestError,
    "PDF_TOO_LARGE": InvalidRequestError,
}


def raise_for_error(status_code: int, response_body: dict[str, Any]) -> None:
    """Raise appropriate exception based on API error response."""
    if response_body.get("success") is True:
        return

    error = response_body.get("error", {})
    code = error.get("code", "UNKNOWN_ERROR")
    message = error.get("message", "An unknown error occurred")

    exception_class = ERROR_CODE_MAP.get(code, APIError)
    raise exception_class(
        message=message,
        code=code,
        status_code=status_code,
        response_body=response_body,
    )

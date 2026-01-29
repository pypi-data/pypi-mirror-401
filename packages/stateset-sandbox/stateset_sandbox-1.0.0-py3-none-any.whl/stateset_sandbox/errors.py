"""Custom exceptions for StateSet Sandbox SDK."""

from typing import Any, Dict, Optional


class SandboxError(Exception):
    """Base exception for sandbox errors."""

    def __init__(
        self,
        message: str,
        request_id: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.request_id = request_id


class SandboxApiError(SandboxError):
    """Exception for API errors."""

    def __init__(
        self,
        message: str,
        code: str,
        status_code: int,
        request_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, request_id)
        self.code = code
        self.status_code = status_code
        self.details = details or {}

    @classmethod
    def from_response(
        cls,
        response_body: Dict[str, Any],
        status_code: int,
        request_id: Optional[str] = None,
    ) -> "SandboxApiError":
        """Create an error from an API response."""
        error = response_body.get("error", {})

        if isinstance(error, str):
            return cls(
                message=error,
                code="UNKNOWN_ERROR",
                status_code=status_code,
                request_id=request_id,
            )

        return cls(
            message=error.get("message", "Unknown error"),
            code=error.get("code", "UNKNOWN_ERROR"),
            status_code=status_code,
            request_id=error.get("request_id") or request_id,
            details=error.get("details"),
        )

    def __str__(self) -> str:
        parts = [f"[{self.code}] {self.message}"]
        if self.request_id:
            parts.append(f"(request_id: {self.request_id})")
        return " ".join(parts)


class SandboxTimeoutError(SandboxError):
    """Exception for request timeouts."""

    def __init__(
        self,
        message: str,
        timeout_ms: int,
        request_id: Optional[str] = None,
    ) -> None:
        super().__init__(message, request_id)
        self.timeout_ms = timeout_ms


class SandboxNetworkError(SandboxError):
    """Exception for network errors."""

    def __init__(
        self,
        message: str,
        original_error: Optional[Exception] = None,
        request_id: Optional[str] = None,
    ) -> None:
        super().__init__(message, request_id)
        self.original_error = original_error


class SandboxValidationError(SandboxError):
    """Exception for validation errors."""

    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        request_id: Optional[str] = None,
    ) -> None:
        super().__init__(message, request_id)
        self.field = field


class SandboxNotFoundError(SandboxApiError):
    """Exception when a sandbox is not found."""

    def __init__(
        self,
        sandbox_id: str,
        request_id: Optional[str] = None,
    ) -> None:
        super().__init__(
            message=f"Sandbox '{sandbox_id}' not found",
            code="SANDBOX_NOT_FOUND",
            status_code=404,
            request_id=request_id,
        )
        self.sandbox_id = sandbox_id


class SandboxAuthenticationError(SandboxApiError):
    """Exception for authentication errors."""

    def __init__(
        self,
        message: str = "Authentication failed",
        request_id: Optional[str] = None,
    ) -> None:
        super().__init__(
            message=message,
            code="UNAUTHORIZED",
            status_code=401,
            request_id=request_id,
        )


class SandboxRateLimitError(SandboxApiError):
    """Exception for rate limit errors."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
        request_id: Optional[str] = None,
    ) -> None:
        super().__init__(
            message=message,
            code="RATE_LIMITED",
            status_code=429,
            request_id=request_id,
        )
        self.retry_after = retry_after

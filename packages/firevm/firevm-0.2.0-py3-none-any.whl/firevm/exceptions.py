"""
FireVM SDK Exceptions
Custom exception classes for error handling
"""

from typing import Optional, Dict, Any


class FireVMError(Exception):
    """Base exception for all FireVM SDK errors"""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class AuthenticationError(FireVMError):
    """Raised when authentication fails (401)"""

    def __init__(self, message: str = "Authentication failed", **kwargs):
        super().__init__(message, status_code=401, **kwargs)


class PermissionDeniedError(FireVMError):
    """Raised when user lacks permission for an action (403)"""

    def __init__(self, message: str = "Permission denied", **kwargs):
        super().__init__(message, status_code=403, **kwargs)


class VMNotFoundError(FireVMError):
    """Raised when a VM is not found (404)"""

    def __init__(self, message: str = "VM not found", **kwargs):
        super().__init__(message, status_code=404, **kwargs)


class ResourceNotFoundError(FireVMError):
    """Raised when any resource is not found (404)"""

    def __init__(self, message: str = "Resource not found", **kwargs):
        super().__init__(message, status_code=404, **kwargs)


class QuotaExceededError(FireVMError):
    """Raised when user exceeds their quota limits (429)"""

    def __init__(self, message: str = "Quota exceeded", **kwargs):
        super().__init__(message, status_code=429, **kwargs)


class RateLimitError(FireVMError):
    """Raised when rate limit is exceeded (429)"""

    def __init__(self, message: str = "Rate limit exceeded", **kwargs):
        super().__init__(message, status_code=429, **kwargs)


class ValidationError(FireVMError):
    """Raised when request validation fails (422)"""

    def __init__(self, message: str = "Validation error", **kwargs):
        super().__init__(message, status_code=422, **kwargs)


class ServerError(FireVMError):
    """Raised when server encounters an error (500+)"""

    def __init__(self, message: str = "Internal server error", **kwargs):
        super().__init__(message, status_code=kwargs.get("status_code", 500), **kwargs)


class NetworkError(FireVMError):
    """Raised when network/connection errors occur"""

    def __init__(self, message: str = "Network error", **kwargs):
        super().__init__(message, **kwargs)


class TimeoutError(FireVMError):
    """Raised when request times out"""

    def __init__(self, message: str = "Request timeout", **kwargs):
        super().__init__(message, **kwargs)


def error_from_response(status_code: int, message: str, data: Optional[Dict] = None) -> FireVMError:
    """
    Create appropriate exception based on HTTP status code
    
    Args:
        status_code: HTTP status code
        message: Error message
        data: Optional response data
    
    Returns:
        Appropriate FireVMError subclass
    """
    error_map = {
        401: AuthenticationError,
        403: PermissionDeniedError,
        404: ResourceNotFoundError,
        422: ValidationError,
        429: QuotaExceededError,
    }

    error_class = error_map.get(status_code)
    if error_class:
        return error_class(message, response_data=data)

    if status_code >= 500:
        return ServerError(message, status_code=status_code, response_data=data)

    return FireVMError(message, status_code=status_code, response_data=data)

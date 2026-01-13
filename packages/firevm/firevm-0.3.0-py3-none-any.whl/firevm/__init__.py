"""
FireVM Python SDK
Official client library for FireVM - MicroVM Management Platform
"""

from firevm.client import FireVM
from firevm.async_client import AsyncFireVM
from firevm.exceptions import (
    FireVMError,
    AuthenticationError,
    PermissionDeniedError,
    VMNotFoundError,
    QuotaExceededError,
    RateLimitError,
    ValidationError,
    ServerError,
)
from firevm.models import VM, APIKey, PaginatedResponse

__version__ = "0.1.0"
__all__ = [
    "FireVM",
    "AsyncFireVM",
    "FireVMError",
    "AuthenticationError",
    "PermissionDeniedError",
    "VMNotFoundError",
    "QuotaExceededError",
    "RateLimitError",
    "ValidationError",
    "ServerError",
    "VM",
    "APIKey",
    "PaginatedResponse",
]

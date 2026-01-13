"""
FireVM SDK Models
Pydantic models for API request/response data
"""

from datetime import datetime
from typing import Optional, List, Dict, Any, TypeVar, Generic
from pydantic import BaseModel, Field, ConfigDict


T = TypeVar("T")


class VM(BaseModel):
    """Represents a FireVM microVM instance"""

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id")
    name: str
    user_id: str
    tier: str  # "small" | "medium" | "large"
    image: str
    state: str  # "creating" | "running" | "stopped" | "paused" | "terminated"
    worker_id: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def __repr__(self) -> str:
        return f"VM(id='{self.id}', name='{self.name}', state='{self.state}')"


class VMCreate(BaseModel):
    """Request model for creating a new VM"""

    name: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")
    tier: str = Field(..., pattern=r"^(small|medium|large)$")
    image: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class VMStatus(BaseModel):
    """VM status information"""

    id: str
    name: str
    state: str
    uptime: Optional[float] = None  # seconds
    cpu_usage: Optional[float] = None  # percentage
    memory_usage: Optional[int] = None  # bytes


class APIKey(BaseModel):
    """Represents an API key"""

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id")
    user_id: str
    name: str
    key_hash: str
    key: Optional[str] = None  # Only present when creating
    scopes: List[str] = Field(default_factory=list)
    last_used_at: Optional[datetime] = None
    created_at: datetime
    revoked: bool = False

    def __repr__(self) -> str:
        return f"APIKey(id='{self.id}', name='{self.name}', revoked={self.revoked})"


class APIKeyCreate(BaseModel):
    """Request model for creating a new API key"""

    name: str = Field(..., min_length=3, max_length=100)
    scopes: List[str] = Field(default_factory=lambda: ["vms:read", "vms:write"])


class User(BaseModel):
    """Represents a user"""

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id")
    email: str
    name: Optional[str] = None
    picture: Optional[str] = None
    tier: str = "free"  # "free" | "pro" | "enterprise"
    google_id: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response"""

    data: List[T]
    page: int
    limit: int
    total: int
    total_pages: int

    def __repr__(self) -> str:
        return f"PaginatedResponse(page={self.page}/{self.total_pages}, items={len(self.data)}/{self.total})"


class ErrorResponse(BaseModel):
    """API error response"""

    detail: str
    status_code: int
    error_type: Optional[str] = None
    fields: Optional[Dict[str, Any]] = None

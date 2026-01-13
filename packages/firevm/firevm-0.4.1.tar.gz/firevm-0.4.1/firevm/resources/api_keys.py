"""
API Key Resource - API key management operations
"""

from typing import List, TYPE_CHECKING

from firevm.models import APIKey, APIKeyCreate

if TYPE_CHECKING:
    from firevm.http_client import HTTPClient


class APIKeyResource:
    """API key management operations"""

    def __init__(self, client: "HTTPClient"):
        """
        Initialize API key resource
        
        Args:
            client: HTTP client instance
        """
        self._client = client

    def create(self, name: str, scopes: List[str] = None) -> APIKey:
        """
        Create a new API key
        
        Args:
            name: Key name for identification
            scopes: List of permission scopes (e.g., ["vms:read", "vms:write"])
            
        Returns:
            APIKey object with plaintext key (save it - it won't be shown again!)
            
        Example:
            >>> key = client.api_keys.create(
            ...     name="production-key",
            ...     scopes=["vms:read", "vms:write"]
            ... )
            >>> print(f"API Key: {key.key}")  # Save this!
        """
        if scopes is None:
            scopes = ["vms:read", "vms:write"]

        key_data = APIKeyCreate(name=name, scopes=scopes)
        response = self._client.post("/api/v1/api-keys/", json=key_data.model_dump())
        return APIKey(**response)

    def list(self) -> List[APIKey]:
        """
        List all API keys for the authenticated user
        
        Note: Plaintext keys are not returned, only metadata
        
        Returns:
            List of APIKey objects
            
        Example:
            >>> keys = client.api_keys.list()
            >>> for key in keys:
            ...     print(f"{key.name}: {key.scopes}")
        """
        response = self._client.get("/api/v1/api-keys/")
        return [APIKey(**key_data) for key_data in response]

    def get(self, key_id: str) -> APIKey:
        """
        Get details of a specific API key
        
        Args:
            key_id: API key identifier
            
        Returns:
            APIKey object (without plaintext key)
            
        Example:
            >>> key = client.api_keys.get("key_abc123")
            >>> print(f"Last used: {key.last_used_at}")
        """
        response = self._client.get(f"/api/v1/api-keys/{key_id}")
        return APIKey(**response)

    def revoke(self, key_id: str) -> APIKey:
        """
        Revoke an API key (cannot be undone)
        
        Args:
            key_id: API key identifier
            
        Returns:
            Updated APIKey object with revoked=True
            
        Example:
            >>> key = client.api_keys.revoke("key_abc123")
            >>> print(f"Revoked: {key.revoked}")
        """
        response = self._client.delete(f"/api/v1/api-keys/{key_id}")
        return APIKey(**response)

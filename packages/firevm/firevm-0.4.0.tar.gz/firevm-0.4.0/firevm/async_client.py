"""
FireVM SDK Async Client
Asynchronous client for interacting with FireVM API
"""

from typing import Optional, Dict, Any, List

try:
    import aiohttp
except ImportError:
    raise ImportError(
        "Async support requires aiohttp. Install it with: pip install firevm[async]"
    )

from firevm.models import VM, VMCreate, APIKey, APIKeyCreate, PaginatedResponse
from firevm.exceptions import error_from_response, NetworkError, TimeoutError as FireVMTimeoutError


class AsyncFireVM:
    """
    Async client for FireVM API
    
    Example:
        >>> import asyncio
        >>> from firevm import AsyncFireVM
        >>> 
        >>> async def main():
        ...     async with AsyncFireVM(api_key="fvm_live_...") as client:
        ...         vm = await client.vms.create(
        ...             name="async-vm",
        ...             tier="small",
        ...             image="ubuntu-22.04"
        ...         )
        ...         print(f"Created: {vm.id}")
        >>> 
        >>> asyncio.run(main())
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        token: Optional[str] = None,
        base_url: str = "https://firevm.cloud",
        timeout: int = 30,
    ):
        """
        Initialize async FireVM client
        
        Args:
            api_key: Your FireVM API key (starts with fvm_live_)
            token: JWT token from OAuth authentication
            base_url: API base URL (defaults to production)
            timeout: Request timeout in seconds
        """
        if not api_key and not token:
            raise ValueError("Either api_key or token must be provided")

        if api_key and token:
            raise ValueError("Provide either api_key or token, not both")

        self.base_url = base_url.rstrip("/")
        self.timeout = aiohttp.ClientTimeout(total=timeout)

        # Prepare headers
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "firevm-python/0.1.0",
        }

        if api_key:
            self.headers["X-API-Key"] = api_key
        elif token:
            self.headers["Authorization"] = f"Bearer {token}"

        self._session: Optional[aiohttp.ClientSession] = None
        self.vms = AsyncVMResource(self)
        self.api_keys = AsyncAPIKeyResource(self)

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers=self.headers,
                timeout=self.timeout,
            )
        return self._session

    async def _request(
        self,
        method: str,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make async HTTP request"""
        session = await self._get_session()
        url = f"{self.base_url}{path}"

        try:
            async with session.request(method, url, json=json, params=params) as response:
                # Handle error responses
                if response.status >= 400:
                    try:
                        error_data = await response.json()
                        message = error_data.get("detail", await response.text())
                    except Exception:
                        message = await response.text() or response.reason

                    raise error_from_response(
                        status_code=response.status,
                        message=message,
                        data=error_data if "error_data" in locals() else None,
                    )

                # Parse successful response
                if response.status == 204:
                    return {}

                return await response.json()

        except aiohttp.ClientTimeout as e:
            raise FireVMTimeoutError(f"Request timeout") from e
        except aiohttp.ClientError as e:
            raise NetworkError(f"Network error: {str(e)}") from e

    async def close(self):
        """Close the client session"""
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()


class AsyncVMResource:
    """Async VM operations"""

    def __init__(self, client: AsyncFireVM):
        self._client = client

    async def create(
        self,
        name: str,
        tier: str,
        image: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> VM:
        """Create a new VM"""
        vm_data = VMCreate(
            name=name,
            tier=tier,
            image=image,
            metadata=metadata or {},
        )
        response = await self._client._request("POST", "/api/v1/vms/", json=vm_data.model_dump())
        return VM(**response)

    async def list(
        self,
        state: Optional[str] = None,
        tier: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
    ) -> PaginatedResponse[VM]:
        """List all VMs"""
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if state:
            params["state"] = state
        if tier:
            params["tier"] = tier

        response = await self._client._request("GET", "/api/v1/vms/", params=params)
        vms = [VM(**vm_data) for vm_data in response["data"]]

        return PaginatedResponse[VM](
            data=vms,
            page=response["page"],
            limit=response["limit"],
            total=response["total"],
            total_pages=response["total_pages"],
        )

    async def get(self, vm_id: str) -> VM:
        """Get VM details"""
        response = await self._client._request("GET", f"/api/v1/vms/{vm_id}")
        return VM(**response)

    async def start(self, vm_id: str) -> VM:
        """Start a VM"""
        response = await self._client._request("POST", f"/api/v1/vms/{vm_id}/start")
        return VM(**response)

    async def stop(self, vm_id: str) -> VM:
        """Stop a VM"""
        response = await self._client._request("POST", f"/api/v1/vms/{vm_id}/stop")
        return VM(**response)

    async def restart(self, vm_id: str) -> VM:
        """Restart a VM"""
        response = await self._client._request("POST", f"/api/v1/vms/{vm_id}/restart")
        return VM(**response)

    async def pause(self, vm_id: str) -> VM:
        """Pause a VM"""
        response = await self._client._request("POST", f"/api/v1/vms/{vm_id}/pause")
        return VM(**response)

    async def resume(self, vm_id: str) -> VM:
        """Resume a VM"""
        response = await self._client._request("POST", f"/api/v1/vms/{vm_id}/resume")
        return VM(**response)

    async def kill(self, vm_id: str) -> VM:
        """Kill a VM"""
        response = await self._client._request("POST", f"/api/v1/vms/{vm_id}/kill")
        return VM(**response)

    async def status(self, vm_id: str) -> Dict[str, Any]:
        """Get VM status"""
        return await self._client._request("GET", f"/api/v1/vms/{vm_id}/status")

    async def logs(self, vm_id: str, lines: int = 100) -> str:
        """Get VM logs"""
        response = await self._client._request("GET", f"/api/v1/vms/{vm_id}/logs", params={"lines": lines})
        return response.get("logs", "")
    
    async def run_code(
        self,
        vm_id: str,
        code: str,
        language: str = "python",
        timeout: int = 30
    ) -> Dict[str, Any]:
        """
        Execute code in a running VM and get the output (async version)
        
        Args:
            vm_id: VM identifier
            code: Code to execute
            language: Programming language (python, bash, node). Default: python
            timeout: Execution timeout in seconds (1-300). Default: 30
            
        Returns:
            Dictionary containing:
                - stdout: Standard output from the code execution
                - stderr: Standard error from the code execution
                - exit_code: Exit code (0 = success)
                - execution_time: Time taken to execute in seconds
            
        Example:
            >>> # Execute Python code asynchronously
            >>> result = await client.vms.run_code(
            ...     vm_id="vm_abc123",
            ...     code="print('Hello from async!')",
            ...     language="python"
            ... )
            >>> print(result["stdout"])
            Hello from async!
        """
        return await self._client._request(
            "POST",
            f"/api/v1/vms/{vm_id}/execute",
            params={
                "code": code,
                "language": language,
                "timeout": timeout
            }
        )


class AsyncAPIKeyResource:
    """Async API key operations"""

    def __init__(self, client: AsyncFireVM):
        self._client = client

    async def create(self, name: str, scopes: List[str] = None) -> APIKey:
        """Create a new API key"""
        if scopes is None:
            scopes = ["vms:read", "vms:write"]

        key_data = APIKeyCreate(name=name, scopes=scopes)
        response = await self._client._request("POST", "/api/v1/api-keys/", json=key_data.model_dump())
        return APIKey(**response)

    async def list(self) -> List[APIKey]:
        """List all API keys"""
        response = await self._client._request("GET", "/api/v1/api-keys/")
        return [APIKey(**key_data) for key_data in response]

    async def get(self, key_id: str) -> APIKey:
        """Get API key details"""
        response = await self._client._request("GET", f"/api/v1/api-keys/{key_id}")
        return APIKey(**response)

    async def revoke(self, key_id: str) -> APIKey:
        """Revoke an API key"""
        response = await self._client._request("DELETE", f"/api/v1/api-keys/{key_id}")
        return APIKey(**response)

"""
FireVM SDK Main Client
Synchronous client for interacting with FireVM API
"""

from typing import Optional

from firevm.http_client import HTTPClient
from firevm.resources.vms import VMResource
from firevm.resources.api_keys import APIKeyResource


class FireVM:
    """
    Main client for FireVM API (synchronous)
    
    Example:
        >>> from firevm import FireVM
        >>> 
        >>> # Using API key
        >>> client = FireVM(api_key="fvm_live_your_key_here")
        >>> 
        >>> # Using JWT token
        >>> client = FireVM(token="your_jwt_token")
        >>> 
        >>> # Create a VM
        >>> vm = client.vms.create(name="test-vm", tier="small", image="ubuntu-22.04")
        >>> 
        >>> # List VMs
        >>> vms = client.vms.list()
        >>> 
        >>> # Close client when done
        >>> client.close()
        >>> 
        >>> # Or use context manager
        >>> with FireVM(api_key="fvm_live_...") as client:
        ...     vm = client.vms.create(name="test", tier="small", image="ubuntu-22.04")
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        token: Optional[str] = None,
        base_url: str = "https://firevm.cloud",
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """
        Initialize FireVM client
        
        Args:
            api_key: Your FireVM API key (starts with fvm_live_)
            token: JWT token from OAuth authentication
            base_url: API base URL (defaults to production)
            timeout: Request timeout in seconds
            max_retries: Number of retry attempts for failed requests
            retry_delay: Delay between retries in seconds
            
        Raises:
            ValueError: If neither api_key nor token is provided
            
        Note:
            You must provide either api_key or token, but not both.
        """
        if not api_key and not token:
            raise ValueError("Either api_key or token must be provided")

        if api_key and token:
            raise ValueError("Provide either api_key or token, not both")

        # Initialize HTTP client
        self._http_client = HTTPClient(
            base_url=base_url,
            api_key=api_key,
            token=token,
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
        )

        # Initialize resource clients
        self.vms = VMResource(self._http_client)
        self.api_keys = APIKeyResource(self._http_client)

    def close(self):
        """Close the HTTP client session"""
        self._http_client.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

    def __repr__(self) -> str:
        """String representation"""
        return f"FireVM(base_url='{self._http_client.base_url}')"

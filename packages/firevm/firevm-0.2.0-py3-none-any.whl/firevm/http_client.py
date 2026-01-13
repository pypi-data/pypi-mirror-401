"""
HTTP client wrapper with retry logic and error handling
"""

import time
from typing import Optional, Dict, Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from firevm.exceptions import error_from_response, NetworkError, TimeoutError as FireVMTimeoutError


class HTTPClient:
    """HTTP client with automatic retries and error handling"""

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        token: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """
        Initialize HTTP client
        
        Args:
            base_url: API base URL
            api_key: FireVM API key (starts with fvm_live_)
            token: JWT token from OAuth
            timeout: Request timeout in seconds
            max_retries: Number of retry attempts
            retry_delay: Delay between retries in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # Create session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=retry_delay,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Set authentication headers
        if api_key:
            self.session.headers["X-API-Key"] = api_key
        elif token:
            self.session.headers["Authorization"] = f"Bearer {token}"
        else:
            raise ValueError("Either api_key or token must be provided")

        self.session.headers["Content-Type"] = "application/json"
        self.session.headers["User-Agent"] = "firevm-python/0.1.0"

    def request(
        self,
        method: str,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make HTTP request with error handling
        
        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path
            json: JSON request body
            params: Query parameters
            
        Returns:
            Response data as dictionary
            
        Raises:
            FireVMError: On API errors
            NetworkError: On network errors
            TimeoutError: On timeout
        """
        url = f"{self.base_url}{path}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=json,
                params=params,
                timeout=self.timeout,
            )

            # Handle error responses
            if response.status_code >= 400:
                try:
                    error_data = response.json()
                    message = error_data.get("detail", response.text)
                except Exception:
                    message = response.text or response.reason

                raise error_from_response(
                    status_code=response.status_code,
                    message=message,
                    data=error_data if "error_data" in locals() else None,
                )

            # Parse successful response
            if response.status_code == 204:  # No content
                return {}

            return response.json()

        except requests.exceptions.Timeout as e:
            raise FireVMTimeoutError(f"Request timeout after {self.timeout}s") from e
        except requests.exceptions.ConnectionError as e:
            raise NetworkError(f"Connection error: {str(e)}") from e
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error: {str(e)}") from e

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request"""
        return self.request("GET", path, params=params)

    def post(self, path: str, json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make POST request"""
        return self.request("POST", path, json=json, params=params)

    def put(self, path: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make PUT request"""
        return self.request("PUT", path, json=json)

    def delete(self, path: str) -> Dict[str, Any]:
        """Make DELETE request"""
        return self.request("DELETE", path)

    def close(self):
        """Close the session"""
        self.session.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

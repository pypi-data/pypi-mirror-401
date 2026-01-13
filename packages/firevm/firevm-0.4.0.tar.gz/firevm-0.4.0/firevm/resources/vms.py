"""
VM Resource - VM management operations
"""

from typing import Optional, List, Dict, Any, TYPE_CHECKING

from firevm.models import VM, VMCreate, PaginatedResponse

if TYPE_CHECKING:
    from firevm.http_client import HTTPClient


class VMResource:
    """VM management operations"""

    def __init__(self, client: "HTTPClient"):
        """
        Initialize VM resource
        
        Args:
            client: HTTP client instance
        """
        self._client = client

    def create(
        self,
        name: str,
        tier: str,
        image: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> VM:
        """
        Create a new microVM
        
        Args:
            name: VM name (3-50 chars, alphanumeric + hyphens)
            tier: VM size tier (small, medium, large)
            image: OS image name (e.g., ubuntu-22.04)
            metadata: Optional metadata dictionary
            
        Returns:
            Created VM object
            
        Example:
            >>> vm = client.vms.create(
            ...     name="my-app-vm",
            ...     tier="small",
            ...     image="ubuntu-22.04"
            ... )
        """
        vm_data = VMCreate(
            name=name,
            tier=tier,
            image=image,
            metadata=metadata or {},
        )

        response = self._client.post("/api/v1/vms/", json=vm_data.model_dump())
        return VM(**response)

    def list(
        self,
        state: Optional[str] = None,
        tier: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
    ) -> PaginatedResponse[VM]:
        """
        List all VMs for the authenticated user
        
        Args:
            state: Filter by state (creating, running, stopped, paused, terminated)
            tier: Filter by tier (small, medium, large)
            page: Page number (starts at 1)
            limit: Items per page (max 100)
            
        Returns:
            Paginated list of VMs
            
        Example:
            >>> vms = client.vms.list(state="running", limit=50)
            >>> for vm in vms.data:
            ...     print(f"{vm.name}: {vm.state}")
        """
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if state:
            params["state"] = state
        if tier:
            params["tier"] = tier

        response = self._client.get("/api/v1/vms/", params=params)

        # Parse VM objects
        vms = [VM(**vm_data) for vm_data in response["data"]]

        return PaginatedResponse[VM](
            data=vms,
            page=response["page"],
            limit=response["limit"],
            total=response["total"],
            total_pages=response["total_pages"],
        )

    def get(self, vm_id: str) -> VM:
        """
        Get details of a specific VM
        
        Args:
            vm_id: VM identifier
            
        Returns:
            VM object
            
        Example:
            >>> vm = client.vms.get("vm_abc123")
            >>> print(f"VM {vm.name} is {vm.state}")
        """
        response = self._client.get(f"/api/v1/vms/{vm_id}")
        return VM(**response)

    def start(self, vm_id: str) -> VM:
        """
        Start a stopped or paused VM
        
        Args:
            vm_id: VM identifier
            
        Returns:
            Updated VM object
            
        Example:
            >>> vm = client.vms.start("vm_abc123")
        """
        response = self._client.post(f"/api/v1/vms/{vm_id}/start")
        return VM(**response)

    def stop(self, vm_id: str) -> VM:
        """
        Stop a running VM gracefully
        
        Args:
            vm_id: VM identifier
            
        Returns:
            Updated VM object
            
        Example:
            >>> vm = client.vms.stop("vm_abc123")
        """
        response = self._client.post(f"/api/v1/vms/{vm_id}/stop")
        return VM(**response)

    def restart(self, vm_id: str) -> VM:
        """
        Restart a VM
        
        Args:
            vm_id: VM identifier
            
        Returns:
            Updated VM object
            
        Example:
            >>> vm = client.vms.restart("vm_abc123")
        """
        response = self._client.post(f"/api/v1/vms/{vm_id}/restart")
        return VM(**response)

    def pause(self, vm_id: str) -> VM:
        """
        Pause a running VM (saves state to memory)
        
        Args:
            vm_id: VM identifier
            
        Returns:
            Updated VM object
            
        Example:
            >>> vm = client.vms.pause("vm_abc123")
        """
        response = self._client.post(f"/api/v1/vms/{vm_id}/pause")
        return VM(**response)

    def resume(self, vm_id: str) -> VM:
        """
        Resume a paused VM
        
        Args:
            vm_id: VM identifier
            
        Returns:
            Updated VM object
            
        Example:
            >>> vm = client.vms.resume("vm_abc123")
        """
        response = self._client.post(f"/api/v1/vms/{vm_id}/resume")
        return VM(**response)

    def kill(self, vm_id: str) -> VM:
        """
        Forcefully terminate a VM (cannot be undone)
        
        Args:
            vm_id: VM identifier
            
        Returns:
            Updated VM object
            
        Example:
            >>> vm = client.vms.kill("vm_abc123")
        """
        response = self._client.post(f"/api/v1/vms/{vm_id}/kill")
        return VM(**response)

    def status(self, vm_id: str) -> Dict[str, Any]:
        """
        Get current status and metrics of a VM
        
        Args:
            vm_id: VM identifier
            
        Returns:
            Status dictionary with state, uptime, CPU, memory
            
        Example:
            >>> status = client.vms.status("vm_abc123")
            >>> print(f"State: {status['state']}, Uptime: {status['uptime']}s")
        """
        return self._client.get(f"/api/v1/vms/{vm_id}/status")

    def logs(self, vm_id: str, lines: int = 100) -> str:
        """
        Get console logs from a VM
        
        Args:
            vm_id: VM identifier
            lines: Number of log lines to retrieve (default 100)
            
        Returns:
            Log content as string
            
        Example:
            >>> logs = client.vms.logs("vm_abc123", lines=50)
            >>> print(logs)
        """
        response = self._client.get(f"/api/v1/vms/{vm_id}/logs", params={"lines": lines})
        return response.get("logs", "")
    
    def run_code(
        self,
        vm_id: str,
        code: str,
        language: str = "python",
        timeout: int = 30
    ) -> Dict[str, Any]:
        """
        Execute code in a running VM and get the output
        
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
            
        Raises:
            HTTPError: If VM is not found or not running
            
        Example:
            >>> # Execute Python code
            >>> result = client.vms.run_code(
            ...     vm_id="vm_abc123",
            ...     code="print('Hello World!')\nprint(2 + 2)",
            ...     language="python"
            ... )
            >>> print(result["stdout"])
            Hello World!
            4
            >>> print(result["exit_code"])
            0
            
            >>> # Execute bash script
            >>> result = client.vms.run_code(
            ...     vm_id="vm_abc123",
            ...     code="ls -la /tmp && echo 'Done'",
            ...     language="bash"
            ... )
            >>> print(result["stdout"])
        """
        response = self._client.post(
            f"/api/v1/vms/{vm_id}/execute",
            params={
                "code": code,
                "language": language,
                "timeout": timeout
            }
        )
        return response

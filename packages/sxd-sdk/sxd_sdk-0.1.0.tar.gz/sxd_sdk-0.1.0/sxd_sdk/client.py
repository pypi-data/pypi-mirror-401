"""
SXD Client for interacting with the SentientX Data Platform.

Provides methods to:
- Submit workflows
- Upload data
- Query results
- Check job status
"""

import asyncio
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import httpx
from pydantic import BaseModel


@dataclass
class JobStatus:
    """Status of a submitted job."""

    workflow_id: str
    run_id: str
    status: str  # RUNNING, COMPLETED, FAILED, CANCELED, TERMINATED
    start_time: Optional[str] = None
    close_time: Optional[str] = None
    result: Optional[Any] = None
    error: Optional[str] = None

    @property
    def is_running(self) -> bool:
        return self.status == "RUNNING"

    @property
    def is_completed(self) -> bool:
        return self.status == "COMPLETED"

    @property
    def is_failed(self) -> bool:
        return self.status in ("FAILED", "TERMINATED", "CANCELED")


class SXDClient:
    """Client for interacting with SXD cluster.

    Example:
        # Using environment variables
        client = SXDClient()

        # Or explicit configuration
        client = SXDClient(
            host="cluster.example.com",
            api_key="your-api-key",
        )

        # Submit a job
        job = await client.submit("my-pipeline", {"source_url": "s3://bucket/file"})
        print(f"Job submitted: {job.workflow_id}")

        # Wait for completion
        result = await client.wait(job.workflow_id)
        print(f"Result: {result}")
    """

    def __init__(
        self,
        host: Optional[str] = None,
        api_key: Optional[str] = None,
        temporal_host: Optional[str] = None,
        temporal_port: int = 7233,
        timeout: float = 30.0,
    ):
        """Initialize the SXD client.

        Args:
            host: SXD cluster host (default: SXD_HOST env var)
            api_key: API key for authentication (default: SXD_API_KEY env var)
            temporal_host: Temporal server host (default: same as host)
            temporal_port: Temporal server port
            timeout: HTTP request timeout
        """
        self.host = host or os.getenv("SXD_HOST", "localhost")
        self.api_key = api_key or os.getenv("SXD_API_KEY")
        self.temporal_host = temporal_host or self.host
        self.temporal_port = temporal_port
        self.timeout = timeout

        self._http_client: Optional[httpx.AsyncClient] = None
        self._temporal_client = None

    async def _get_http_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._http_client is None:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            self._http_client = httpx.AsyncClient(
                base_url=f"https://{self.host}",
                headers=headers,
                timeout=self.timeout,
            )
        return self._http_client

    async def _get_temporal_client(self):
        """Get or create Temporal client."""
        if self._temporal_client is None:
            from temporalio.client import Client

            self._temporal_client = await Client.connect(
                f"{self.temporal_host}:{self.temporal_port}"
            )
        return self._temporal_client

    async def close(self):
        """Close the client connections."""
        if self._http_client:
            await self._http_client.aclose()
            self._http_client = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    # Job submission

    async def submit(
        self,
        workflow: str,
        input_data: Union[Dict[str, Any], BaseModel],
        task_queue: Optional[str] = None,
        workflow_id: Optional[str] = None,
        wait: bool = False,
    ) -> JobStatus:
        """Submit a workflow for execution.

        Args:
            workflow: Workflow name (e.g., "video-processor")
            input_data: Input data (dict or Pydantic model)
            task_queue: Task queue (default: inferred from workflow)
            workflow_id: Custom workflow ID (default: auto-generated)
            wait: If True, wait for completion before returning

        Returns:
            JobStatus with workflow_id and initial status
        """
        import uuid

        if isinstance(input_data, BaseModel):
            input_data = input_data.model_dump()

        workflow_id = workflow_id or f"{workflow}-{uuid.uuid4().hex[:8]}"
        task_queue = task_queue or f"{workflow}-processing"

        client = await self._get_temporal_client()

        # Get workflow class from registry or use generic execution
        handle = await client.start_workflow(
            workflow,
            input_data,
            id=workflow_id,
            task_queue=task_queue,
        )

        status = JobStatus(
            workflow_id=workflow_id,
            run_id=handle.result_run_id,
            status="RUNNING",
        )

        if wait:
            result = await handle.result()
            status.status = "COMPLETED"
            status.result = result

        return status

    async def status(self, workflow_id: str) -> JobStatus:
        """Get the status of a workflow.

        Args:
            workflow_id: Workflow ID to check

        Returns:
            JobStatus with current state
        """
        client = await self._get_temporal_client()
        handle = client.get_workflow_handle(workflow_id)

        try:
            desc = await handle.describe()

            status = desc.status.name if desc.status else "UNKNOWN"

            return JobStatus(
                workflow_id=workflow_id,
                run_id=desc.run_id,
                status=status,
                start_time=str(desc.start_time) if desc.start_time else None,
                close_time=str(desc.close_time) if desc.close_time else None,
            )
        except Exception as e:
            return JobStatus(
                workflow_id=workflow_id,
                run_id="",
                status="NOT_FOUND",
                error=str(e),
            )

    async def wait(
        self,
        workflow_id: str,
        timeout: Optional[float] = None,
    ) -> Any:
        """Wait for a workflow to complete and return the result.

        Args:
            workflow_id: Workflow ID to wait for
            timeout: Maximum time to wait (seconds)

        Returns:
            Workflow result

        Raises:
            TimeoutError: If workflow doesn't complete within timeout
            Exception: If workflow fails
        """
        client = await self._get_temporal_client()
        handle = client.get_workflow_handle(workflow_id)

        if timeout:
            return await asyncio.wait_for(handle.result(), timeout=timeout)
        return await handle.result()

    async def cancel(self, workflow_id: str) -> bool:
        """Cancel a running workflow.

        Args:
            workflow_id: Workflow ID to cancel

        Returns:
            True if canceled successfully
        """
        client = await self._get_temporal_client()
        handle = client.get_workflow_handle(workflow_id)

        try:
            await handle.cancel()
            return True
        except Exception:
            return False

    # Data operations

    async def upload(
        self,
        local_path: Union[str, Path],
        customer_id: str = "default",
        remote_path: Optional[str] = None,
    ) -> str:
        """Upload a file or directory to the cluster.

        Args:
            local_path: Local file or directory path
            customer_id: Customer ID for data isolation
            remote_path: Optional remote path (default: auto-generated)

        Returns:
            Remote path where data was uploaded
        """
        # This would use the IngestWorkflow or direct rsync
        # For now, return a placeholder
        local_path = Path(local_path)

        if not local_path.exists():
            raise FileNotFoundError(f"Path not found: {local_path}")

        # In production, this would submit an IngestWorkflow
        # or use direct rsync/scp to worker nodes
        raise NotImplementedError(
            "Direct upload requires cluster connection. "
            "Use 'sxd upload' command instead."
        )

    # Query operations

    async def query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Run a ClickHouse query.

        Args:
            query: SQL query or shortcut name
            params: Query parameters

        Returns:
            Query results as list of dicts
        """
        http = await self._get_http_client()

        response = await http.post(
            "/api/query",
            json={"query": query, "params": params or {}},
        )
        response.raise_for_status()
        return response.json()

    async def list_videos(
        self,
        customer_id: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """List processed videos.

        Args:
            customer_id: Filter by customer
            limit: Maximum results

        Returns:
            List of video records
        """
        query = "SELECT * FROM videos FINAL ORDER BY updated_at DESC LIMIT %(limit)s"
        params: dict[str, Any] = {"limit": limit}

        if customer_id:
            query = "SELECT * FROM videos FINAL WHERE customer_id = %(customer_id)s ORDER BY updated_at DESC LIMIT %(limit)s"
            params["customer_id"] = customer_id

        return await self.query(query, params)


async def connect(
    host: Optional[str] = None,
    api_key: Optional[str] = None,
    **kwargs,
) -> SXDClient:
    """Create and connect an SXD client.

    This is a convenience function for creating a client.

    Example:
        async with await connect() as client:
            job = await client.submit("my-pipeline", data)
    """
    return SXDClient(host=host, api_key=api_key, **kwargs)

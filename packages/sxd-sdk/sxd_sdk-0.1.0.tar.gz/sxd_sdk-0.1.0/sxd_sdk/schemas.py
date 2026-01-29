"""
Common schemas for SXD pipelines.

These base classes provide standard input/output structures that work well
with the SXD platform. You can extend them or create your own Pydantic models.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class PipelineInput(BaseModel):
    """Base input schema for pipelines.

    Extend this class to add pipeline-specific input fields.

    Example:
        class VideoInput(PipelineInput):
            resolution: str = "1080p"
            fps: int = 30
    """

    model_config = ConfigDict(extra="allow")

    source_url: str = Field(..., description="URL or path to input data")
    customer_id: str = Field(default="default", description="Customer/tenant ID")
    options: Dict[str, Any] = Field(
        default_factory=dict, description="Additional options"
    )


class PipelineOutput(BaseModel):
    """Base output schema for pipelines.

    Extend this class to add pipeline-specific output fields.

    Example:
        class VideoOutput(PipelineOutput):
            frame_count: int
            duration_seconds: float
    """

    model_config = ConfigDict(extra="allow")

    status: str = Field(..., description="Processing status: success, failed, partial")
    output_path: Optional[str] = Field(None, description="Path to output data")
    metrics: Dict[str, Any] = Field(
        default_factory=dict, description="Processing metrics"
    )
    errors: List[str] = Field(default_factory=list, description="Error messages if any")


class ProcessingResult(BaseModel):
    """Result from an individual activity.

    Use this for intermediate results within a workflow.
    """

    success: bool = Field(..., description="Whether the activity succeeded")
    output_path: Optional[str] = Field(None, description="Path to output")
    error: Optional[str] = Field(None, description="Error message if failed")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )

    @classmethod
    def ok(cls, output_path: Optional[str] = None, **metadata) -> "ProcessingResult":
        """Create a successful result."""
        return cls(success=True, output_path=output_path, error=None, metadata=metadata)

    @classmethod
    def fail(cls, error: str, **metadata) -> "ProcessingResult":
        """Create a failed result."""
        return cls(success=False, error=error, output_path=None, metadata=metadata)


class BatchInput(BaseModel):
    """Input for batch processing pipelines."""

    source_urls: List[str] = Field(..., description="List of URLs to process")
    customer_id: str = Field(default="default")
    batch_id: Optional[str] = Field(None, description="Optional batch identifier")
    max_concurrency: int = Field(default=4, description="Max parallel processing")
    options: Dict[str, Any] = Field(default_factory=dict)


class BatchOutput(BaseModel):
    """Output from batch processing pipelines."""

    batch_id: str
    total: int = Field(..., description="Total items in batch")
    succeeded: int = Field(default=0)
    failed: int = Field(default=0)
    results: List[ProcessingResult] = Field(default_factory=list)

    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        if self.total == 0:
            return 0.0
        return (self.succeeded / self.total) * 100


class FrameData(BaseModel):
    """Metadata for a video frame."""

    frame_number: int
    timestamp_ms: float
    path: str
    width: Optional[int] = None
    height: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class VideoMetadata(BaseModel):
    """Metadata for a video file."""

    video_id: str
    source_url: str
    duration_seconds: float
    fps: float
    width: int
    height: int
    codec: Optional[str] = None
    size_bytes: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

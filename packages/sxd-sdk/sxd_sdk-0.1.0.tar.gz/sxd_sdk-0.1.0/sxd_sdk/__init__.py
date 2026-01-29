"""
SXD SDK - Build data pipelines for SentientX Data Platform.

This SDK provides:
- Temporal workflow and activity decorators
- Schema classes for pipeline I/O
- Testing utilities for local development
- Client for submitting jobs to the cluster

Example:
    from sxd_sdk import activity, workflow
    from sxd_sdk.schemas import PipelineInput, PipelineOutput, ProcessingResult

    @activity
    async def process_frame(frame_path: str) -> ProcessingResult:
        # Your processing logic
        return ProcessingResult.ok(output_path="/output/result")

    @workflow
    class MyPipeline:
        async def run(self, input: PipelineInput) -> PipelineOutput:
            result = await self.execute_activity(process_frame, input.source_url)
            return PipelineOutput(status="success", output_path=result.output_path)
"""

__version__ = "0.1.0"

# Re-export Temporal decorators
from temporalio import activity as _activity
from temporalio import workflow as _workflow

activity = _activity.defn
workflow = _workflow.defn

# Schema classes
# Client for cluster interaction
from sxd_sdk.client import (  # noqa: E402
    SXDClient,
    connect,
)
from sxd_sdk.schemas import (  # noqa: E402
    BatchInput,
    BatchOutput,
    FrameData,
    PipelineInput,
    PipelineOutput,
    ProcessingResult,
    VideoMetadata,
)

# Testing utilities
from sxd_sdk.testing import (  # noqa: E402
    MockActivityEnvironment,
    WorkflowSimulator,
)

__all__ = [
    # Version
    "__version__",
    # Decorators
    "activity",
    "workflow",
    # Schemas
    "PipelineInput",
    "PipelineOutput",
    "ProcessingResult",
    "BatchInput",
    "BatchOutput",
    "FrameData",
    "VideoMetadata",
    # Testing
    "MockActivityEnvironment",
    "WorkflowSimulator",
    # Client
    "SXDClient",
    "connect",
]

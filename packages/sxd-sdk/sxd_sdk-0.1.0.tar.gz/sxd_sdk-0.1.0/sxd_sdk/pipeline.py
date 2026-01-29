"""
Pipeline definition helpers.

Provides configuration classes and utilities for defining SXD pipelines
with proper Temporal integration.
"""

from dataclasses import dataclass, field
from datetime import timedelta
from enum import Enum
from pathlib import Path
from typing import List, Optional


class RuntimeProvider(str, Enum):
    DOCKER = "docker"
    BOXLITE = "boxlite"


@dataclass
class RuntimeConfig:
    """Configuration for the app runtime environment."""

    provider: RuntimeProvider = RuntimeProvider.DOCKER
    image: Optional[str] = None
    dockerfile: Optional[str] = None
    # Boxlite specific or generic resource overrides
    memory_mb: Optional[int] = None
    cpu_cores: Optional[int] = None


@dataclass
class ActivityConfig:
    """Configuration for a Temporal activity.

    Example:
        config = ActivityConfig(
            name="process_frame",
            start_to_close_timeout=timedelta(minutes=10),
            retry_attempts=3,
        )
    """

    name: str
    start_to_close_timeout: timedelta = field(
        default_factory=lambda: timedelta(minutes=5)
    )
    schedule_to_close_timeout: Optional[timedelta] = None
    heartbeat_timeout: Optional[timedelta] = None
    retry_attempts: int = 3
    retry_initial_interval: timedelta = field(
        default_factory=lambda: timedelta(seconds=1)
    )
    retry_maximum_interval: timedelta = field(
        default_factory=lambda: timedelta(minutes=1)
    )
    retry_backoff_coefficient: float = 2.0
    task_queue: Optional[str] = None


@dataclass
class WorkflowConfig:
    """Configuration for a Temporal workflow.

    Example:
        config = WorkflowConfig(
            name="video-processor",
            task_queue="video-processing",
            execution_timeout=timedelta(hours=2),
        )
    """

    name: str
    task_queue: str = "default"
    execution_timeout: Optional[timedelta] = None
    run_timeout: Optional[timedelta] = None
    task_timeout: timedelta = field(default_factory=lambda: timedelta(seconds=10))
    retry_attempts: int = 0
    description: str = ""


@dataclass
class PipelineConfig:
    """Complete pipeline configuration.

    In the new model, this represents an SXD App which may contain
    one or more workflows sharing a single runtime.
    """

    name: str
    description: str = ""
    version: str = "0.1.0"
    
    # Simple top-level fields for cluster registration
    base_image: str = "sxd-base"
    timeout: int = 3600
    gpu: bool = False

    # Runtime configuration (One App = One Runtime)
    runtime: RuntimeConfig = field(default_factory=RuntimeConfig)

    # Workflow configurations (One or more)
    workflows: List[WorkflowConfig] = field(default_factory=list)

    # Activity configurations
    activities: List[ActivityConfig] = field(default_factory=list)


def load_pipeline_config(path: Path) -> PipelineConfig:
    """Load pipeline configuration from a YAML file.

    Args:
        path: Path to sxd.yaml or pipeline.yaml

    Returns:
        PipelineConfig object
    """
    import yaml

    with open(path) as f:
        data = yaml.safe_load(f)

    # Runtime parsing
    runtime_data = data.get("runtime", {})
    runtime = RuntimeConfig(
        provider=RuntimeProvider(runtime_data.get("provider", "docker")),
        image=runtime_data.get("image"),
        dockerfile=runtime_data.get("dockerfile"),
        memory_mb=runtime_data.get("memory_mb"),
        cpu_cores=runtime_data.get("cpu_cores"),
    )

    # Workflows parsing
    workflows = []
    workflows_data = data.get("workflows")
    if workflows_data:
        for wf_data in workflows_data:
            workflows.append(
                WorkflowConfig(
                    name=wf_data["name"],
                    task_queue=wf_data.get("task_queue", "default"),
                    description=wf_data.get("description", ""),
                )
            )

    activities = []
    for act_data in data.get("activities", []):
        activities.append(
            ActivityConfig(
                name=act_data["name"],
                start_to_close_timeout=timedelta(
                    seconds=act_data.get("timeout_seconds", 300)
                ),
                retry_attempts=act_data.get("retry_attempts", 3),
            )
        )

    return PipelineConfig(
        name=data.get("name", "unnamed"),
        description=data.get("description", ""),
        version=data.get("version", "0.1.0"),
        base_image=data.get("base_image", "sxd-base"),
        timeout=data.get("timeout", 3600),
        gpu=data.get("gpu", False),
        runtime=runtime,
        workflows=workflows,
        activities=activities,
    )

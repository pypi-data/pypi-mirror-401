"""
Pipeline scaffolding utilities for creating new pipeline projects.
"""

import re
from pathlib import Path


def to_class_name(name: str) -> str:
    """Convert a pipeline name to a Python class name.

    Args:
        name: The pipeline name (e.g., "video-processor", "my_pipeline")

    Returns:
        A valid Python class name in PascalCase (e.g., "VideoProcessor", "MyPipeline")
    """
    # Replace hyphens and underscores with spaces, then title case
    words = re.split(r"[-_]", name)
    return "".join(word.capitalize() for word in words)


def to_snake_case(name: str) -> str:
    """Convert a pipeline name to snake_case.

    Args:
        name: The pipeline name (e.g., "video-processor")

    Returns:
        A snake_case version (e.g., "video_processor")
    """
    return name.replace("-", "_")


def scaffold_pipeline(
    name: str,
    output_dir: Path,
    description: str = "",
    base_image: str = "sxd-base",
) -> None:
    """Create a new pipeline project with all necessary files.

    Args:
        name: The pipeline name (e.g., "video-processor")
        output_dir: Directory where the pipeline project will be created
        description: Optional description for the pipeline
        base_image: Base Docker image to use (default: "sxd-base")
    """
    from sxd_sdk.docker import generate_dockerfile

    # Create directory structure
    output_dir.mkdir(parents=True, exist_ok=True)

    package_name = to_snake_case(name)
    class_name = to_class_name(name)

    # Create package directory
    package_dir = output_dir / package_name
    package_dir.mkdir(exist_ok=True)

    tests_dir = output_dir / "tests"
    tests_dir.mkdir(exist_ok=True)

    # Write pyproject.toml
    pyproject_content = f"""[project]
name = "{name}"
version = "0.1.0"
description = "{description}"
requires-python = ">=3.11"
dependencies = [
    "sxd-sdk>=0.1.0",
    "temporalio>=1.5.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["{package_name}"]
"""
    (output_dir / "pyproject.toml").write_text(pyproject_content)

    # Write sxd.yaml
    sxd_yaml_content = f"""name: {name}
description: "{description}"
version: "0.1.0"
base_image: {base_image}

workflows:
  - name: {name}
    task_queue: {name}-processing
    timeout: 3600

activities:
  - name: process
    timeout: 600
"""
    (output_dir / "sxd.yaml").write_text(sxd_yaml_content)

    # Write Dockerfile
    dockerfile_content = generate_dockerfile(base_image=base_image)
    (output_dir / "Dockerfile").write_text(dockerfile_content)

    # Write README.md
    readme_content = f"""# {name}

{description}

## Getting Started

1. Install dependencies:
   ```bash
   pip install -e .
   ```

2. Run tests:
   ```bash
   pytest
   ```

3. Deploy to cluster:
   ```bash
   sxd publish
   ```
"""
    (output_dir / "README.md").write_text(readme_content)

    # Write package __init__.py
    init_content = f'''"""
{name} pipeline package.
"""

__version__ = "0.1.0"
'''
    (package_dir / "__init__.py").write_text(init_content)

    # Write workflows.py
    workflows_content = f'''"""
Workflow definitions for {name}.
"""

from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta

from .activities import process


@workflow.defn(name="{name}")
class {class_name}Workflow:
    """Main workflow for {name}."""

    @workflow.run
    async def run(self, input_data: dict) -> dict:
        result = await workflow.execute_activity(
            process,
            input_data,
            start_to_close_timeout=timedelta(minutes=10),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )
        return result
'''
    (package_dir / "workflows.py").write_text(workflows_content)

    # Write activities.py
    activities_content = f'''"""
Activity definitions for {name}.
"""

from temporalio import activity


@activity.defn(name="process")
async def process(input_data: dict) -> dict:
    """Process input data.

    Args:
        input_data: Input data dictionary

    Returns:
        Processed result dictionary
    """
    activity.logger.info("Processing input: %s", input_data)
    
    # Mock processing delay or logic
    video_id = input_data.get("video_id", "unknown")
    
    return {{
        "status": "success", 
        "video_id": video_id,
        "processed_at": activity.info().started_at.isoformat(),
        "result": {{"quality": 0.95}}
    }}
'''
    (package_dir / "activities.py").write_text(activities_content)

    # Write test file
    test_content = f'''"""
Tests for {name} pipeline.
"""

import pytest


class Test{class_name}:
    """Tests for {class_name} pipeline."""

    def test_placeholder(self):
        """Placeholder test."""
        assert True
'''
    (tests_dir / "test_pipeline.py").write_text(test_content)

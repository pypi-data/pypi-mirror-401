"""
Docker utilities for SXD pipelines.

Provides helpers for working with Dockerfiles and SXD base images.
"""

import re
from pathlib import Path
from typing import List, Optional

# Available SXD base images
SXD_BASE_IMAGES = {
    "sxd-base": "Python 3.12 with core dependencies",
    "sxd-pytorch": "PyTorch 2.x with CUDA support",
    "sxd-opencv": "OpenCV with video processing libs",
    "sxd-cuda": "CUDA runtime for GPU workloads",
}

# Registry URLs
LOCAL_REGISTRY = "localhost:5000"
PUBLIC_REGISTRY = "ghcr.io/sentient-x"


class DockerfileError(Exception):
    """Raised when there's an issue with a Dockerfile."""

    pass


def get_full_image_name(
    base_image: str, registry: str = PUBLIC_REGISTRY, tag: str = "latest"
) -> str:
    """Get the full image name with registry and tag.

    Args:
        base_image: Base image name (e.g., "sxd-pytorch")
        registry: Registry URL
        tag: Image tag

    Returns:
        Full image name (e.g., "ghcr.io/sentient-x/sxd-pytorch:latest")
    """
    # Handle if already has registry prefix
    if "/" in base_image and base_image.startswith(("localhost", "ghcr.io")):
        if ":" in base_image:
            return base_image
        return f"{base_image}:{tag}"

    return f"{registry}/{base_image}:{tag}"


def validate_dockerfile(dockerfile_path: Path) -> str:
    """Validate that a Dockerfile derives from an SXD base image.

    Args:
        dockerfile_path: Path to the Dockerfile

    Returns:
        The base image name found

    Raises:
        DockerfileError: If the Dockerfile doesn't use an SXD base image
    """
    if not dockerfile_path.exists():
        raise DockerfileError(f"Dockerfile not found: {dockerfile_path}")

    content = dockerfile_path.read_text()

    # Find FROM instructions
    from_pattern = re.compile(r"^\s*FROM\s+([^\s]+)", re.MULTILINE | re.IGNORECASE)
    matches = from_pattern.findall(content)

    if not matches:
        raise DockerfileError(f"No FROM instruction found in {dockerfile_path}")

    # Check the final stage base image
    final_base = matches[-1]
    base_image = final_base.split(":")[0]

    # Check against allowed base images
    valid_prefixes = (
        list(SXD_BASE_IMAGES.keys())
        + [f"{LOCAL_REGISTRY}/{img}" for img in SXD_BASE_IMAGES.keys()]
        + [f"{PUBLIC_REGISTRY}/{img}" for img in SXD_BASE_IMAGES.keys()]
    )

    is_valid = any(
        base_image == prefix or base_image.endswith(f"/{prefix.split('/')[-1]}")
        for prefix in valid_prefixes
    )

    if not is_valid:
        raise DockerfileError(
            f"Dockerfile must derive from an SXD base image.\n"
            f"Found: {final_base}\n"
            f"Allowed base images:\n"
            + "\n".join(f"  - {img}: {desc}" for img, desc in SXD_BASE_IMAGES.items())
        )

    return final_base


def generate_dockerfile(
    base_image: str = "sxd-base",
    dependencies: Optional[List[str]] = None,
    system_packages: Optional[List[str]] = None,
    registry: str = PUBLIC_REGISTRY,
    tag: str = "latest",
    workdir: str = "/app",
    entrypoint: Optional[str] = None,
) -> str:
    """Generate a Dockerfile for an SXD pipeline.

    Args:
        base_image: Base image to use
        dependencies: Python packages to install
        system_packages: System packages to install (apt)
        registry: Docker registry
        tag: Image tag
        workdir: Working directory
        entrypoint: Custom entrypoint command

    Returns:
        Dockerfile content as string

    Example:
        dockerfile = generate_dockerfile(
            base_image="sxd-pytorch",
            dependencies=["transformers", "accelerate"],
            system_packages=["libgl1"],
        )
        Path("Dockerfile").write_text(dockerfile)
    """
    full_image = get_full_image_name(base_image, registry, tag)

    lines = [
        f"FROM {full_image}",
        "",
        f"WORKDIR {workdir}",
        "",
    ]

    # System packages
    if system_packages:
        packages = " ".join(system_packages)
        lines.extend(
            [
                "# Install system dependencies",
                "RUN apt-get update && apt-get install -y --no-install-recommends \\",
                f"    {packages} \\",
                "    && rm -rf /var/lib/apt/lists/*",
                "",
            ]
        )

    # Copy and install Python dependencies
    lines.extend(
        [
            "# Copy project files",
            "COPY pyproject.toml .",
            "COPY . .",
            "",
        ]
    )

    # Pip dependencies
    if dependencies:
        deps = " ".join(f'"{dep}"' for dep in dependencies)
        lines.extend(
            [
                "# Install additional Python dependencies",
                f"RUN pip install --no-cache-dir {deps}",
                "",
            ]
        )

    # Install the pipeline package
    lines.extend(
        [
            "# Install pipeline package",
            "RUN pip install --no-cache-dir -e .",
            "",
        ]
    )

    # Entrypoint
    if entrypoint:
        lines.append(f'CMD ["{entrypoint}"]')
    else:
        lines.append('CMD ["python", "-m", "sxd_sdk.worker"]')

    return "\n".join(lines)


def write_dockerfile(
    output_path: Path,
    base_image: str = "sxd-base",
    dependencies: Optional[List[str]] = None,
    system_packages: Optional[List[str]] = None,
    **kwargs,
) -> Path:
    """Generate and write a Dockerfile.

    Args:
        output_path: Where to write the Dockerfile
        base_image: Base image to use
        dependencies: Python packages
        system_packages: System packages
        **kwargs: Additional arguments to generate_dockerfile

    Returns:
        Path to the written Dockerfile
    """
    content = generate_dockerfile(
        base_image=base_image,
        dependencies=dependencies,
        system_packages=system_packages,
        **kwargs,
    )
    output_path.write_text(content)
    return output_path

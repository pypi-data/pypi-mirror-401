"""GPU availability checker for Docker containers."""

import subprocess
from typing import NamedTuple

# Error messages for GPU availability issues
_ERROR_NO_DRIVERS = "NVIDIA GPU drivers not found. Please install NVIDIA drivers."
_ERROR_NO_TOOLKIT = (
    "NVIDIA Container Toolkit not found. "
    "Please install it from: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html"
)


class GPUAvailability(NamedTuple):
    """Result of GPU availability check."""

    available: bool
    nvidia_installed: bool
    nvidia_docker_available: bool
    error_message: str | None = None


def check_gpu_availability() -> GPUAvailability:
    """Check if GPU is available for Docker containers.

    This checks:
    1. If nvidia-smi is available (NVIDIA drivers installed)
    2. If Docker supports GPU passthrough (NVIDIA Container Toolkit installed)

    Returns:
        GPUAvailability tuple with check results
    """
    nvidia_installed = _check_nvidia_drivers()
    if not nvidia_installed:
        return GPUAvailability(
            available=False,
            nvidia_installed=False,
            nvidia_docker_available=False,
            error_message=_ERROR_NO_DRIVERS,
        )

    nvidia_docker_available = _check_nvidia_container_toolkit()
    if not nvidia_docker_available:
        return GPUAvailability(
            available=False,
            nvidia_installed=True,
            nvidia_docker_available=False,
            error_message=_ERROR_NO_TOOLKIT,
        )

    return GPUAvailability(
        available=True,
        nvidia_installed=True,
        nvidia_docker_available=True,
        error_message=None,
    )


def _check_nvidia_drivers() -> bool:
    """Check if nvidia-smi is available.

    Returns:
        True if nvidia-smi command succeeds
    """
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _check_nvidia_container_toolkit() -> bool:
    """Check if NVIDIA Container Toolkit is installed.

    This checks if Docker has access to NVIDIA runtime by attempting
    to run a simple GPU query through Docker.

    Returns:
        True if nvidia-docker is available
    """
    try:
        result = subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                "--gpus=all",
                "nvidia/cuda:11.0.3-base-ubuntu20.04",
                "nvidia-smi",
                "--query-gpu=name",
                "--format=csv,noheader",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def get_gpu_info() -> dict[str, str | list[str] | int]:
    """Get information about available GPUs.

    Returns:
        Dictionary with GPU information
    """
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            return {"error": "Failed to query GPU information"}

        return _parse_gpu_info(result.stdout)

    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        return {"error": f"Failed to query GPU: {e}"}


def _parse_gpu_info(stdout: str) -> dict[str, str | list[str] | int]:
    """Parse nvidia-smi output into GPU info dictionary.

    Args:
        stdout: Raw output from nvidia-smi

    Returns:
        Dictionary with GPU list and count
    """
    lines = stdout.strip().split("\n")
    gpus = []

    for i, line in enumerate(lines):
        parts = line.split(", ")
        if len(parts) >= 2:
            gpus.append(f"GPU {i}: {parts[0]} ({parts[1]} MB)")

    return {"gpus": gpus, "count": len(gpus)}

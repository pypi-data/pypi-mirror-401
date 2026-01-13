"""Docker container management for Speaches."""

import threading
import time
from collections.abc import Callable
from typing import Any

import docker
import httpx
from docker.errors import APIError, DockerException, NotFound
from docker.types import DeviceRequest

from video_summarizer.config import constants
from video_summarizer.core.base import ContainerManager
from video_summarizer.transcriber.stats_monitor import NetworkStats, NetworkStatsMonitor
from video_summarizer.utils.errors import ContainerError


class SpeachesContainerManager(ContainerManager):
    """Manages Speaches Docker container for Whisper transcription."""

    DEFAULT_IMAGE = "ghcr.io/speaches-ai/speaches:latest-cpu"
    DEFAULT_GPU_IMAGE = "ghcr.io/speaches-ai/speaches:latest-cuda"

    def __init__(
        self,
        container_name: str = "speaches",
        container_port: int = 8000,
        container_image: str = DEFAULT_IMAGE,
        use_gpu: bool = False,
    ) -> None:
        """Initialize container manager.

        Args:
            container_name: Name of the container
            container_port: Port to expose
            container_image: Docker image to use
            use_gpu: Whether to enable GPU support
        """
        self.container_name = container_name
        self.container_port = container_port
        self.container_image = container_image
        self.use_gpu = use_gpu
        self.client = docker.from_env()

    def is_running(self) -> bool:
        """Check if container is running.

        Returns:
            True if container is running
        """
        try:
            container = self.client.containers.get(self.container_name)
            return str(container.status) == "running"
        except NotFound:
            return False
        except DockerException as e:
            raise ContainerError(f"Failed to check container status: {e}") from e

    def start(self) -> None:
        """Start the container.

        Raises:
            ContainerError: If start fails
        """
        try:
            container = self._get_or_create_container()
            if container.status != "running":
                container.start()
            self._wait_for_health()
        except APIError as e:
            raise ContainerError(f"Failed to start container: {e}") from e

    def _get_or_create_container(self) -> Any:
        """Get existing container or create a new one.

        Returns:
            Docker container object
        """
        try:
            return self.client.containers.get(self.container_name)
        except NotFound:
            return self._create_container()

    def _create_container(self) -> Any:
        """Create and start a new container.

        Returns:
            Docker container object
        """
        container_kwargs = {
            "image": self.container_image,
            "name": self.container_name,
            "ports": {f"{self.container_port}/tcp": self.container_port},
            "volumes": {
                "hf-hub-cache": {
                    "bind": "/home/ubuntu/.cache/huggingface/hub",
                    "mode": "rw",
                }
            },
            "detach": True,
            "remove": True,
        }

        if self.use_gpu:
            container_kwargs["device_requests"] = [
                DeviceRequest(
                    count=-1,  # All available GPUs
                    capabilities=[["gpu"]],
                )
            ]

        return self.client.containers.run(**container_kwargs)

    def stop(self) -> None:
        """Stop the container.

        Raises:
            ContainerError: If stop fails
        """
        try:
            container = self.client.containers.get(self.container_name)
            container.stop()
        except NotFound:
            return
        except DockerException as e:
            raise ContainerError(f"Failed to stop container: {e}") from e

    def get_status(self) -> dict[str, Any]:
        """Get container status information.

        Returns:
            Dictionary with status information
        """
        try:
            container = self.client.containers.get(self.container_name)
            container.reload()
            image = container.image.tags[0] if container.image.tags else str(container.image.id)
            return self._build_status_dict(container.status, image)
        except NotFound:
            return self._build_status_dict("not_found", self.container_image)
        except DockerException as e:
            raise ContainerError(f"Failed to get container status: {e}") from e

    def _build_status_dict(self, status: str, image: str) -> dict[str, Any]:
        """Build status dictionary.

        Args:
            status: Container status string
            image: Container image identifier

        Returns:
            Status dictionary
        """
        return {
            "name": self.container_name,
            "status": status,
            "image": image,
            "port": self.container_port,
        }

    def _wait_for_health(self) -> None:
        """Wait for container to be healthy.

        Raises:
            ContainerError: If container doesn't become healthy
        """
        for _ in range(constants.HEALTH_CHECK_MAX_RETRIES):
            time.sleep(constants.CONTAINER_HEALTH_CHECK_INTERVAL)
            if self.is_running():
                return

        raise ContainerError(
            f"Container did not become healthy within {constants.CONTAINER_START_TIMEOUT} seconds"
        )

    def _get_api_base(self) -> str:
        """Get the API base URL for the container.

        Returns:
            API base URL
        """
        return f"http://localhost:{self.container_port}"

    def list_models(self, task: str | None = None) -> list[dict[str, Any]]:
        """List local models.

        Args:
            task: Optional task filter (automatic-speech-recognition or text-to-speech)

        Returns:
            List of model dictionaries

        Raises:
            ContainerError: If request fails
        """
        try:
            api_base = self._get_api_base()
            params = {"task": task} if task else {}

            response = httpx.get(
                f"{api_base}/v1/models",
                params=params,
                timeout=30.0,
            )
            response.raise_for_status()

            data = response.json()
            return list(data.get("data", []))
        except httpx.HTTPError as e:
            raise ContainerError(f"Failed to list models: {e}") from e

    def download_model(
        self,
        model_id: str,
        progress_callback: Callable[[dict], None] | None = None,
    ) -> dict:
        """Download a model to the container with network monitoring.

        The POST request to /v1/models/{model_id} is BLOCKING and only returns
        when the model download is fully complete. This method runs both the
        POST request and network monitoring in background threads so the main
        thread remains free to update the Rich Live UI.

        Args:
            model_id: Model ID to download
            progress_callback: Called with stats: {
                'bytes_downloaded': int,
                'speed_mbps': float,
                'elapsed_seconds': float
            }

        Returns:
            Dictionary with download statistics

        Raises:
            ContainerError: If download fails
        """
        if self._is_model_available(model_id):
            return {"status": "already_downloaded"}

        container = self.client.containers.get(self.container_name)
        download_state = _create_download_state()

        monitor = self._start_monitoring(container, download_state, progress_callback)
        post_exception = self._start_download_thread(model_id)

        if monitor:
            monitor.stop()

        self._check_download_error(post_exception)

        elapsed = time.time() - download_state["start_time"]
        return {
            "status": "complete",
            "bytes_downloaded": download_state["last_rx_bytes"],
            "elapsed_seconds": elapsed,
        }

    def _start_monitoring(
        self,
        container: Any,
        state: dict,
        progress_callback: Callable[[dict], None] | None,
    ) -> NetworkStatsMonitor | None:
        """Start network monitoring in background thread.

        Args:
            container: Docker container to monitor
            state: Download state dictionary
            progress_callback: Callback for progress updates

        Returns:
            Monitor instance or None if no callback
        """
        if not progress_callback:
            return None

        monitor = NetworkStatsMonitor(container)

        def stats_callback(network_stats: NetworkStats) -> None:
            current_time = time.time()
            elapsed = current_time - state["start_time"]

            time_delta = current_time - state["last_stats_time"]
            if time_delta > 0 and state["last_stats_time"] > 0:
                bytes_delta = network_stats.bytes_downloaded - state["last_rx_bytes"]
                speed_mbps = (bytes_delta / time_delta) / (1024 * 1024)
            else:
                speed_mbps = 0.0

            state["last_rx_bytes"] = network_stats.bytes_downloaded
            state["last_stats_time"] = current_time

            progress_callback(
                {
                    "bytes_downloaded": network_stats.bytes_downloaded,
                    "speed_mbps": speed_mbps,
                    "elapsed_seconds": elapsed,
                }
            )

        monitor.start(stats_callback)
        return monitor

    def _start_download_thread(self, model_id: str) -> Exception | None:
        """Start download POST request in background thread and wait for completion.

        Args:
            model_id: Model ID to download

        Returns:
            Exception if download failed, None otherwise
        """
        post_complete = threading.Event()
        post_exception: Exception | None = None

        def run_post_request() -> None:
            nonlocal post_exception
            try:
                api_base = self._get_api_base()
                response = httpx.post(
                    f"{api_base}/v1/models/{model_id}",
                    timeout=None,
                )
                response.raise_for_status()
            except Exception as e:
                post_exception = e
            finally:
                post_complete.set()

        threading.Thread(target=run_post_request, daemon=True).start()

        while not post_complete.is_set():
            post_complete.wait(timeout=0.1)

        return post_exception

    def _check_download_error(self, exception: Exception | None) -> None:
        """Check download error and raise appropriate ContainerError.

        Args:
            exception: Exception from download thread

        Raises:
            ContainerError: If exception indicates failure
        """
        if not exception:
            return

        if isinstance(exception, httpx.HTTPStatusError):
            raise ContainerError(
                f"Failed to download model (status {exception.response.status_code}): {exception}"
            ) from exception
        if isinstance(exception, httpx.RequestError):
            raise ContainerError(f"Failed to download model: {exception}") from exception

        raise ContainerError(f"Failed to download model: {exception}") from exception

    def _is_model_available(self, model_id: str) -> bool:
        """Check if a model is already downloaded.

        Args:
            model_id: Model ID to check

        Returns:
            True if model is in the list of downloaded models
        """
        try:
            models = self.list_models(task="automatic-speech-recognition")
            model_ids = [model.get("id") for model in models]
            return model_id in model_ids
        except Exception:
            return False

    def ensure_model(
        self,
        model_id: str,
        progress_callback: Callable[[dict], None] | None = None,
    ) -> dict:
        """Ensure a model is downloaded, downloading it if necessary.

        Args:
            model_id: Model ID to check/download
            progress_callback: Optional callback for progress updates

        Returns:
            Dictionary with download statistics
        """
        if self._is_model_available(model_id):
            return {"status": "already_downloaded"}

        return self.download_model(model_id, progress_callback=progress_callback)


def _create_download_state() -> dict:
    """Create state dictionary for download tracking.

    Returns:
        Dictionary with initial download state
    """
    return {
        "start_time": time.time(),
        "last_rx_bytes": 0,
        "last_stats_time": 0,
    }

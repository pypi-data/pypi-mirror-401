"""Monitor container network statistics during model downloads."""

import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class NetworkStats:
    """Network statistics at a point in time."""

    bytes_received: int
    bytes_sent: int
    timestamp: float

    @property
    def bytes_downloaded(self) -> int:
        return self.bytes_received


class NetworkStatsMonitor:
    """Monitor Docker container network statistics in real-time.

    Uses container.stats(stream=True) to receive continuous updates
    from Docker, ensuring no traffic is missed.
    """

    def __init__(self, container: Any) -> None:
        self.container = container
        self._monitoring = False
        self._thread: threading.Thread | None = None
        self._callback: Callable[[NetworkStats], None] | None = None
        self._initial_rx_bytes = 0

    def start(self, callback: Callable[[NetworkStats], None]) -> None:
        """Start monitoring network stats via streaming API.

        Args:
            callback: Function to call with each stats update
        """
        stats = self.container.stats(stream=False)
        self._initial_rx_bytes = self._get_rx_bytes(stats)

        self._callback = callback
        self._monitoring = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop monitoring network stats."""
        self._monitoring = False
        if self._thread:
            self._thread.join(timeout=5.0)
            self._thread = None

    def _monitor_loop(self) -> None:
        """Monitor network stats using Docker's streaming API.

        This method iterates over the stats stream from Docker, receiving
        updates approximately every 1 second. This ensures we capture all
        network traffic without polling gaps.
        """
        try:
            stats_stream = self.container.stats(stream=True, decode=True)

            for stats in stats_stream:
                if not self._monitoring:
                    break

                current_rx = self._get_rx_bytes(stats)

                network_stats = NetworkStats(
                    bytes_received=current_rx - self._initial_rx_bytes,
                    bytes_sent=0,
                    timestamp=time.time(),
                )

                if self._callback:
                    self._callback(network_stats)

        except Exception:
            pass

    def _get_rx_bytes(self, stats: dict) -> int:
        """Extract received bytes from Docker stats.

        Args:
            stats: Docker stats dictionary with format:
                {'networks': {'eth0': {'rx_bytes': 12345, 'tx_bytes': 6789}, ...}}

        Returns:
            Total received bytes across all network interfaces
        """
        try:
            networks = stats.get("networks", {})
            total_rx = sum(int(iface_stats.get("rx_bytes", 0)) for iface_stats in networks.values())
            return total_rx
        except (KeyError, TypeError):
            return 0

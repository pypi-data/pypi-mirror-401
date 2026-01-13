"""URL validation for video platforms."""

import re
from urllib.parse import urlparse


class VideoURLValidator:
    """Validate and classify video URLs."""

    # Known platform patterns
    PLATFORM_PATTERNS: dict[str, list[str]] = {
        "youtube": [
            r"https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+",
            r"https?://youtu\.be/[\w-]+",
        ],
        "bilibili": [r"https?://(?:www\.)?bilibili\.com/video/[\w]+"],
        "vimeo": [r"https?://vimeo\.com/\d+"],
    }

    def is_valid_url(self, url: str) -> bool:
        """Check if URL is valid format.

        Args:
            url: URL to validate

        Returns:
            True if URL format is valid
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def detect_platform(self, url: str) -> str | None:
        """Detect video platform from URL.

        Args:
            url: URL to check

        Returns:
            Platform name or None
        """
        for platform, patterns in self.PLATFORM_PATTERNS.items():
            for pattern in patterns:
                if re.match(pattern, url):
                    return platform
        return None

    def is_supported_platform(self, url: str) -> bool:
        """Check if URL is from a supported platform.

        Args:
            url: URL to check

        Returns:
            True if platform is supported
        """
        # yt-dlp supports 1000+ sites, so we're very permissive here
        # We just check if it's a valid HTTP(S) URL
        return self.is_valid_url(url)

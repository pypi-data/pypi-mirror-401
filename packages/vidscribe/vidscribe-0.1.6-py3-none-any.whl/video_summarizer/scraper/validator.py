"""URL validation for video platforms."""

from urllib.parse import urlparse


class VideoURLValidator:
    """Validate and classify video URLs."""

    def is_valid_url(self, url: str) -> bool:
        """Check if URL is valid format.

        Args:
            url: URL to validate

        Returns:
            True if URL format is valid
        """
        try:
            result = urlparse(url)
            return bool(result.scheme and result.netloc)
        except Exception:
            return False

    def is_supported_platform(self, url: str) -> bool:
        """Check if URL is from a supported platform.

        Args:
            url: URL to check

        Returns:
            True if platform is supported

        Note:
            yt-dlp supports 1000+ sites, so we accept any valid HTTP(S) URL.
        """
        return self.is_valid_url(url)

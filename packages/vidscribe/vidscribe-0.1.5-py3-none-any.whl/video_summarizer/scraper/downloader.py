"""Video downloader using yt-dlp."""

from pathlib import Path
from typing import Any

import yt_dlp

from video_summarizer.config.constants import AUDIO_QUALITY_MAP
from video_summarizer.core.base import VideoDownloader
from video_summarizer.utils.errors import DownloadError
from video_summarizer.utils.types import AudioQuality


class YtDlpDownloader(VideoDownloader):
    """Download videos from online platforms using yt-dlp."""

    def __init__(
        self, temp_dir: Path = Path("/tmp/vidscribe"), ffmpeg_location: str | None = None
    ) -> None:
        """Initialize downloader.

        Args:
            temp_dir: Directory for temporary downloads
            ffmpeg_location: Optional path to ffmpeg binary for yt-dlp post-processing
        """
        self.temp_dir = temp_dir
        self.ffmpeg_location = ffmpeg_location
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def is_supported_url(self, url: str) -> bool:
        """Check if URL is supported by yt-dlp.

        Args:
            url: URL to check

        Returns:
            True if supported
        """
        try:
            with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
                ydl.extract_info(url, download=False)
            return True
        except Exception:
            return False

    def download_audio(self, url: str, output_dir: Path, quality: str = "medium") -> Path:
        """Download audio from video URL.

        Args:
            url: Video URL
            output_dir: Directory to save audio
            quality: Audio quality (fast, medium, slow)

        Returns:
            Path to downloaded audio file
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        quality_enum = AudioQuality(quality)
        bitrate = AUDIO_QUALITY_MAP[quality_enum]

        ydl_opts: dict[str, Any] = {
            "format": "bestaudio[ext=m4a]/bestaudio/best",
            "outtmpl": str(output_dir / "%(id)s.%(ext)s"),
            "noplaylist": True,
            "quiet": False,
            "no_warnings": False,
        }

        if self.ffmpeg_location:
            ydl_opts["ffmpeg_location"] = self.ffmpeg_location

        is_youtube = "youtube.com" in url or "youtu.be" in url
        if not is_youtube:
            ydl_opts["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": bitrate,
                }
            ]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)

                video_id = info.get("id", "video")
                ext = "mp3" if "postprocessors" in ydl_opts else info.get("ext", "m4a")
                audio_path = output_dir / f"{video_id}.{ext}"

                if not audio_path.exists():
                    raise DownloadError(f"Downloaded file not found: {audio_path}")

                return audio_path

        except DownloadError:
            raise
        except Exception as e:
            raise DownloadError(f"Failed to download audio: {e}") from e

    def get_video_info(self, url: str) -> dict[str, Any]:
        """Get video metadata without downloading.

        Args:
            url: Video URL

        Returns:
            Dictionary with video metadata
        """
        try:
            with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
                info = ydl.extract_info(url, download=False)

                return {
                    "title": info.get("title", ""),
                    "duration": info.get("duration", 0),
                    "thumbnail": info.get("thumbnail"),
                    "platform": self._detect_platform_from_info(info),
                    "video_id": info.get("id", ""),
                    "uploader": info.get("uploader", ""),
                    "view_count": info.get("view_count", 0),
                }

        except Exception as e:
            raise DownloadError(f"Failed to get video info: {e}") from e

    def _detect_platform_from_info(self, info: dict[str, Any]) -> str:
        """Detect platform from yt-dlp info dict."""
        extractor = str(info.get("extractor", "")).lower()
        if "youtube" in extractor:
            return "youtube"
        if "bilibili" in extractor:
            return "bilibili"
        if "vimeo" in extractor:
            return "vimeo"
        return extractor

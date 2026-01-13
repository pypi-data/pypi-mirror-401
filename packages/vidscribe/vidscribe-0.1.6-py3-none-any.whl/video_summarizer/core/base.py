"""Abstract base classes for video summarizer components."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from video_summarizer.utils.types import AudioMetadata, Summary, Transcript


class AudioExtractor(ABC):
    """Abstract base class for audio extraction."""

    @abstractmethod
    def extract_audio(self, source: Path, output_path: Path | None = None) -> Path:
        """Extract audio from video file.

        Args:
            source: Path to video file
            output_path: Optional path for output audio file

        Returns:
            Path to extracted audio file

        Raises:
            AudioExtractionError: If extraction fails
        """

    @abstractmethod
    def get_metadata(self, source: Path) -> AudioMetadata:
        """Get audio metadata from file.

        Args:
            source: Path to audio/video file

        Returns:
            AudioMetadata object
        """


class Transcriber(ABC):
    """Abstract base class for speech-to-text transcription."""

    @abstractmethod
    def transcribe(self, audio_path: Path) -> Transcript:
        """Transcribe audio file to text.

        Args:
            audio_path: Path to audio file

        Returns:
            Transcript object with text and metadata

        Raises:
            TranscriptionError: If transcription fails
        """

    @abstractmethod
    def is_available(self) -> bool:
        """Check if transcription service is available.

        Returns:
            True if service is available
        """


class Summarizer(ABC):
    """Abstract base class for text summarization."""

    @abstractmethod
    def summarize(self, transcript: Transcript, style: str | None = None) -> Summary:
        """Summarize transcript text.

        Args:
            transcript: Transcript object
            style: Optional summary style

        Returns:
            Summary object

        Raises:
            SummarizationError: If summarization fails
        """

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Count tokens in text.

        Args:
            text: Input text

        Returns:
            Number of tokens
        """


class VideoDownloader(ABC):
    """Abstract base class for video downloading."""

    @abstractmethod
    def is_supported_url(self, url: str) -> bool:
        """Check if URL is supported.

        Args:
            url: URL to check

        Returns:
            True if URL is supported
        """

    @abstractmethod
    def download_audio(self, url: str, output_dir: Path, quality: str = "medium") -> Path:
        """Download audio from video URL.

        Args:
            url: Video URL
            output_dir: Directory to save audio
            quality: Audio quality setting

        Returns:
            Path to downloaded audio file

        Raises:
            DownloadError: If download fails
        """

    @abstractmethod
    def get_video_info(self, url: str) -> dict[str, Any]:
        """Get video metadata without downloading.

        Args:
            url: Video URL

        Returns:
            Dictionary with video metadata
        """


class ContainerManager(ABC):
    """Abstract base class for Docker container management."""

    @abstractmethod
    def is_running(self) -> bool:
        """Check if container is running.

        Returns:
            True if container is running
        """

    @abstractmethod
    def start(self) -> None:
        """Start the container.

        Raises:
            ContainerError: If start fails
        """

    @abstractmethod
    def stop(self) -> None:
        """Stop the container.

        Raises:
            ContainerError: If stop fails
        """

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """Get container status information.

        Returns:
            Dictionary with status information
        """

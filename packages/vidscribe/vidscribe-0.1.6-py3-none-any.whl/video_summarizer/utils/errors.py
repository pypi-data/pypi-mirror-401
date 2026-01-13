"""Custom exceptions for video summarizer."""


class VideoSummarizerError(Exception):
    """Base exception for all video summarizer errors."""


class ConfigurationError(VideoSummarizerError):
    """Raised when configuration is invalid or missing."""


class ContainerError(VideoSummarizerError):
    """Raised when Docker container operations fail."""


class AudioExtractionError(VideoSummarizerError):
    """Raised when audio extraction from video fails."""


class TranscriptionError(VideoSummarizerError):
    """Raised when transcription fails."""


class SummarizationError(VideoSummarizerError):
    """Raised when summarization fails."""


class DownloadError(VideoSummarizerError):
    """Raised when video download fails."""


class ValidationError(VideoSummarizerError):
    """Raised when input validation fails."""

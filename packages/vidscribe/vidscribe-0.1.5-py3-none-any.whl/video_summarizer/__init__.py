"""Video summarizer - Automatic video summarization using Whisper and LLMs."""

__version__ = "0.1.0"

from video_summarizer.config import Settings
from video_summarizer.core import (
    AudioExtractor,
    ContainerManager,
    Summarizer,
    Transcriber,
    VideoDownloader,
)
from video_summarizer.scraper import VideoURLValidator, YtDlpDownloader
from video_summarizer.summarizer import (
    OpenAISummarizer,
    TranscriptChunker,
    TranscriptPreprocessor,
)
from video_summarizer.transcriber import (
    MoviePyAudioExtractor,
    SpeachesContainerManager,
    SpeachesTranscriber,
)
from video_summarizer.utils import (
    AudioExtractionError,
    AudioMetadata,
    AudioQuality,
    ConfigurationError,
    ContainerError,
    DownloadError,
    SummarizationError,
    Summary,
    SummaryStyle,
    Transcript,
    TranscriptionError,
    ValidationError,
    VideoMetadata,
    VideoSummarizerError,
    setup_logging,
)

__all__ = [
    # Version
    "__version__",
    # Settings
    "Settings",
    # Core
    "AudioExtractor",
    "Transcriber",
    "Summarizer",
    "VideoDownloader",
    "ContainerManager",
    # Transcriber
    "SpeachesContainerManager",
    "MoviePyAudioExtractor",
    "SpeachesTranscriber",
    # Summarizer
    "TranscriptPreprocessor",
    "TranscriptChunker",
    "OpenAISummarizer",
    # Scraper
    "VideoURLValidator",
    "YtDlpDownloader",
    # Types
    "SummaryStyle",
    "AudioQuality",
    "Transcript",
    "Summary",
    "AudioMetadata",
    "VideoMetadata",
    # Errors
    "VideoSummarizerError",
    "ConfigurationError",
    "ContainerError",
    "AudioExtractionError",
    "TranscriptionError",
    "SummarizationError",
    "DownloadError",
    "ValidationError",
    # Logging
    "setup_logging",
]

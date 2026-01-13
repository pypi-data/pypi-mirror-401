"""Type definitions for video summarizer."""

from dataclasses import dataclass
from enum import Enum


class SummaryStyle(str, Enum):
    """Summary style options."""

    BRIEF = "brief"
    DETAILED = "detailed"
    BULLET_POINTS = "bullet-points"
    CONCISE = "concise"


class AudioQuality(str, Enum):
    """Audio quality settings for download."""

    FAST = "fast"  # 32 kbps
    MEDIUM = "medium"  # 64 kbps
    SLOW = "slow"  # 128 kbps


@dataclass
class Transcript:
    """Transcription result with metadata.

    The raw_response field contains the complete API response,
    which can be saved in different formats (json, text, srt, vtt).
    The text field is always available for summary generation.
    """

    text: str
    duration: float
    language: str | None = None
    confidence: float | None = None
    raw_response: dict | str | None = None  # Full API response
    response_format: str | None = None  # Format used (verbose_json, json, text, srt, vtt)


@dataclass
class Summary:
    """Summarization result."""

    text: str
    model: str
    tokens_used: int
    style: SummaryStyle


@dataclass
class AudioMetadata:
    """Audio file metadata."""

    duration: float
    sample_rate: int
    channels: int
    codec: str
    format: str


@dataclass
class VideoMetadata:
    """Video file metadata."""

    title: str
    duration: float
    thumbnail_url: str | None
    platform: str
    video_id: str

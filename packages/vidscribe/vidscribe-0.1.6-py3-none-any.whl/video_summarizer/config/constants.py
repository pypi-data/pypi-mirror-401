"""Constants for video summarizer."""

from video_summarizer.utils.types import AudioQuality

# Audio quality mapping for yt-dlp
AUDIO_QUALITY_MAP: dict[AudioQuality, str] = {
    AudioQuality.FAST: "32",
    AudioQuality.MEDIUM: "64",
    AudioQuality.SLOW: "128",
}

# Supported audio formats
SUPPORTED_AUDIO_FORMATS = [".wav", ".mp3", ".m4a", ".flac", ".ogg"]
SUPPORTED_VIDEO_FORMATS = [".mp4", ".avi", ".mov", ".mkv", ".webm", ".flv"]

# Whisper-recommended audio parameters
WHISPER_SAMPLE_RATE = 16000  # 16kHz
WHISPER_CHANNELS = 1  # Mono
WHISPER_CODEC = "pcm_s16le"  # 16-bit PCM

# Container health check settings
CONTAINER_START_TIMEOUT = 60  # seconds
CONTAINER_HEALTH_CHECK_INTERVAL = 1  # second
HEALTH_CHECK_MAX_RETRIES = 30

# API retry settings
MAX_API_RETRIES = 3
API_RETRY_DELAY = 1  # second
API_BACKOFF_FACTOR = 2

# Transcript chunking settings
CHUNK_OVERHEAD = 100  # tokens reserved for system message
CHUNK_OVERLAP = 200  # tokens overlap between chunks

# Default prompts
DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant that summarizes video transcripts."
DEFAULT_SUMMARY_PROMPT = "Please provide a concise summary of the following video transcript:"

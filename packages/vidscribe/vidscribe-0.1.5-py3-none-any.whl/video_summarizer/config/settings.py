"""Configuration management using Pydantic."""

import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from video_summarizer.utils.types import AudioQuality, SummaryStyle

# MoviePy environment variables
_MOVIEPY_ENV_VARS = {
    "FFMPEG_BINARY": "ffmpeg_binary",
    "FFPLAY_BINARY": "ffplay_binary",
    "FFPROBE_BINARY": "ffprobe_binary",
}


class TranscriberConfig(BaseSettings):
    """Configuration for audio transcriber."""

    container_name: str = "speaches"
    container_port: int = 8000
    container_image: str = "ghcr.io/speaches-ai/speaches:latest-cpu"
    use_gpu: bool = False
    gpu_container_image: str = "ghcr.io/speaches-ai/speaches:latest-cuda"
    model: str = "Systran/faster-distil-whisper-small.en"
    auto_start_container: bool = True

    # Transcription parameters
    response_format: str = "verbose_json"
    vad_filter: bool = False
    language: str | None = None
    chunk_duration_sec: int = 60
    chunk_duration_threshold: int = 120
    chunk_overlap_sec: int = 0

    def get_container_image(self) -> str:
        """Get the appropriate container image based on GPU setting.

        Returns:
            GPU image if use_gpu is True, otherwise CPU image
        """
        return self.gpu_container_image if self.use_gpu else self.container_image

    model_config = SettingsConfigDict(
        env_prefix="SPEACHES_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class MoviePyConfig(BaseSettings):
    """Configuration for MoviePy audio/video processing."""

    ffmpeg_binary: str = "auto-detect"
    ffplay_binary: str = "auto-detect"
    ffprobe_binary: str = "auto-detect"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class SummarizerConfig(BaseSettings):
    """Configuration for transcript summarizer."""

    api_base: str = "https://api.openai.com/v1"
    api_key: str = Field(default="")
    model: str = "gpt-4o"
    max_tokens: int = 2000
    temperature: float = 0.7
    summary_style: SummaryStyle = SummaryStyle.CONCISE
    max_transcript_length: int = 128000

    model_config = SettingsConfigDict(
        env_prefix="OPENAI_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class ScraperConfig(BaseSettings):
    """Configuration for video scraper."""

    output_format: str = "wav"
    audio_quality: AudioQuality = AudioQuality.MEDIUM
    temp_dir: Path = Field(default_factory=lambda: Path("/tmp/vidscribe"))

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class OutputConfig(BaseSettings):
    """Configuration for output settings."""

    save_transcript: bool = False
    save_summary: bool = True
    summary_format: str = "markdown"
    output_dir: Path = Field(default_factory=lambda: Path("./summaries"))

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class LoggingConfig(BaseSettings):
    """Configuration for logging."""

    log_level: str = "INFO"
    log_file: str | None = None

    model_config = SettingsConfigDict(
        env_prefix="LOG_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class Settings:
    """Main settings class that aggregates all configs."""

    def __init__(self, config_file: Path | None = None) -> None:
        """Initialize settings.

        Args:
            config_file: Optional path to config file
        """
        env_file = str(config_file) if config_file else ".env"

        self.transcriber = TranscriberConfig(_env_file=env_file)
        self.summarizer = SummarizerConfig(_env_file=env_file)
        self.scraper = ScraperConfig(_env_file=env_file)
        self.output = OutputConfig(_env_file=env_file)
        self.logging = LoggingConfig(_env_file=env_file)
        self.moviepy = MoviePyConfig(_env_file=env_file)

        # Set MoviePy environment variables
        # MoviePy reads these directly from os.environ, so we need to set them
        # after loading from the config file
        for env_var, attr_name in _MOVIEPY_ENV_VARS.items():
            os.environ[env_var] = getattr(self.moviepy, attr_name)

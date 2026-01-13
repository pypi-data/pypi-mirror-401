"""Audio extraction from video files using MoviePy."""

from pathlib import Path

from moviepy import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

from video_summarizer.config import constants
from video_summarizer.core.base import AudioExtractor
from video_summarizer.utils.errors import AudioExtractionError
from video_summarizer.utils.types import AudioMetadata


class MoviePyAudioExtractor(AudioExtractor):
    """Extract audio from video files using MoviePy."""

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
        if not source.exists():
            raise AudioExtractionError(f"Source file does not exist: {source}")

        if output_path is None:
            output_path = source.with_suffix(".wav")

        try:
            with VideoFileClip(str(source)) as video:
                if video.audio is None:
                    raise AudioExtractionError(f"Video has no audio track: {source}")

                _write_audio_file(video, output_path)

            return output_path

        except AudioExtractionError:
            raise
        except Exception as e:
            raise AudioExtractionError(f"Failed to extract audio: {e}") from e

    def get_metadata(self, source: Path) -> AudioMetadata:
        """Get audio metadata from file.

        Args:
            source: Path to audio/video file

        Returns:
            AudioMetadata object

        Raises:
            AudioExtractionError: If metadata retrieval fails
        """
        try:
            if source.suffix.lower() in constants.SUPPORTED_VIDEO_FORMATS:
                return self._get_video_metadata(source)
            return self._get_audio_metadata(source)
        except Exception as e:
            raise AudioExtractionError(f"Failed to get metadata: {e}") from e

    def _get_video_metadata(self, source: Path) -> AudioMetadata:
        """Get metadata from video file.

        Args:
            source: Path to video file

        Returns:
            AudioMetadata object
        """
        with VideoFileClip(str(source)) as video:
            if video.audio is None:
                return AudioMetadata(
                    duration=0.0,
                    sample_rate=0,
                    channels=0,
                    codec="none",
                    format=str(source.suffix),
                )
            return AudioMetadata(
                duration=video.audio.duration,
                sample_rate=int(video.audio.fps),
                channels=video.audio.nchannels,
                codec="pcm_s16le",
                format=str(source.suffix),
            )

    def _get_audio_metadata(self, source: Path) -> AudioMetadata:
        """Get metadata from audio file.

        Args:
            source: Path to audio file

        Returns:
            AudioMetadata object
        """
        with AudioFileClip(str(source)) as audio:
            return AudioMetadata(
                duration=audio.duration,
                sample_rate=int(audio.fps),
                channels=audio.nchannels,
                codec="pcm_s16le",
                format=str(source.suffix),
            )


def _write_audio_file(video: VideoFileClip, output_path: Path) -> None:
    """Write audio file with Whisper-optimized settings.

    Args:
        video: VideoFileClip with audio track
        output_path: Path for output audio file
    """
    video.audio.write_audiofile(
        str(output_path),
        codec=constants.WHISPER_CODEC,
        ffmpeg_params=[
            "-ac",
            str(constants.WHISPER_CHANNELS),
            "-ar",
            str(constants.WHISPER_SAMPLE_RATE),
        ],
    )

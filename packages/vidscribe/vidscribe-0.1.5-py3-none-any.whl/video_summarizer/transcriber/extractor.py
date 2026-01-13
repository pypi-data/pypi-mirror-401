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
        """
        if not source.exists():
            raise AudioExtractionError(f"Source file does not exist: {source}")

        # Generate output path if not provided
        if output_path is None:
            output_path = source.with_suffix(".wav")

        try:
            with VideoFileClip(str(source)) as video:
                if video.audio is None:
                    raise AudioExtractionError(f"Video has no audio track: {source}")

                # Extract audio with Whisper-optimized settings
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
        """
        try:
            # Check if it's a video or audio file
            if source.suffix.lower() in constants.SUPPORTED_VIDEO_FORMATS:
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
            else:
                # It's an audio file
                with AudioFileClip(str(source)) as audio:
                    return AudioMetadata(
                        duration=audio.duration,
                        sample_rate=int(audio.fps),
                        channels=audio.nchannels,
                        codec="pcm_s16le",
                        format=str(source.suffix),
                    )

        except Exception as e:
            raise AudioExtractionError(f"Failed to get metadata: {e}") from e

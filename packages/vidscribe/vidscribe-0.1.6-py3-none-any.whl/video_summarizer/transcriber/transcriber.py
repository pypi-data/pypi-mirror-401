"""Speech-to-text transcription using Speaches."""

import logging
import os
import shutil
import subprocess
import tempfile
import typing
from pathlib import Path

import httpx

from video_summarizer.core.base import Transcriber
from video_summarizer.utils.errors import TranscriptionError
from video_summarizer.utils.types import Transcript

logger = logging.getLogger(__name__)

# Bitrate for duration estimation from file size
_ESTIMATED_BITRATE = 128_000  # 128 kbps in bits per second


class SpeachesTranscriber(Transcriber):
    """Transcribe audio using Speaches Whisper API."""

    def __init__(
        self,
        api_base: str = "http://localhost:8000/v1",
        model: str = "Systran/faster-distil-whisper-small.en",
        timeout: int = 600,
        chunk_duration_sec: int = 60,
        chunk_overlap_sec: int = 0,
        chunk_duration_threshold: int = 120,
        response_format: str = "verbose_json",
        vad_filter: bool = False,
        language: str | None = None,
    ) -> None:
        """Initialize transcriber.

        Args:
            api_base: Base URL for Speaches API
            model: Whisper model to use
            timeout: Request timeout in seconds
            chunk_duration_sec: Duration of each audio chunk in seconds
            chunk_overlap_sec: Overlap between chunks in seconds
            chunk_duration_threshold: Duration threshold for using chunked transcription
            response_format: API response format (verbose_json, json, text, srt, vtt)
            vad_filter: Enable voice activity detection filter
            language: Language code (e.g., "en", "zh")
        """
        self.api_base = api_base.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.chunk_duration_sec = chunk_duration_sec
        self.chunk_overlap_sec = chunk_overlap_sec
        self.chunk_duration_threshold = chunk_duration_threshold
        self.response_format = response_format
        self.vad_filter = vad_filter
        self.language = language
        self.client = httpx.Client(timeout=timeout)

    def transcribe(self, audio_path: Path) -> Transcript:
        """Transcribe audio file to text with chunking.

        Args:
            audio_path: Path to audio file

        Returns:
            Transcript object

        Raises:
            TranscriptionError: If transcription fails
        """
        if not audio_path.exists():
            raise TranscriptionError(f"Audio file does not exist: {audio_path}")

        duration = self._get_audio_duration(audio_path)
        logger.info(f"Detected audio duration: {duration}")

        return self._route_transcription(audio_path, duration)

    def _route_transcription(self, audio_path: Path, duration: float | None) -> Transcript:
        """Route to appropriate transcription method based on duration.

        Args:
            audio_path: Path to audio file
            duration: Detected audio duration in seconds

        Returns:
            Transcript object
        """
        if duration is None:
            return self._transcribe_with_estimated_duration(audio_path)

        if duration > self.chunk_duration_threshold:
            logger.info(
                f"Audio duration {duration:.1f}s exceeds {self.chunk_duration_threshold}s, "
                "using chunked transcription"
            )
            return self._transcribe_chunked(audio_path, duration)

        logger.info(f"Audio duration {duration:.1f}s, using single-request transcription")
        return self._transcribe_single(audio_path)

    def _transcribe_with_estimated_duration(self, audio_path: Path) -> Transcript:
        """Transcribe with estimated duration from file size.

        Args:
            audio_path: Path to audio file

        Returns:
            Transcript object
        """
        logger.warning(
            "Could not detect audio duration (ffprobe unavailable). "
            "Using chunked transcription to ensure completeness. "
            "Install ffprobe or set FFPROBE_BINARY in .env for accurate duration detection."
        )
        estimated_duration = estimate_duration_from_file_size(audio_path)
        logger.info(f"Estimated duration from file size: {estimated_duration:.1f}s")
        return self._transcribe_chunked(audio_path, estimated_duration)

    def _get_audio_duration(self, audio_path: Path) -> float | None:
        """Get audio duration using multiple methods.

        Tries multiple methods in order:
        1. ffprobe (most accurate)
        2. mutagen library (if available)

        Args:
            audio_path: Path to audio file

        Returns:
            Duration in seconds, or None if detection fails
        """
        duration = get_duration_via_ffprobe(audio_path)
        if duration is not None:
            return duration

        return get_duration_via_mutagen(audio_path)

    def _split_audio(self, audio_path: Path) -> list[Path]:
        """Split audio file into chunks.

        Args:
            audio_path: Path to audio file

        Returns:
            List of paths to audio chunks
        """
        chunk_dir = tempfile.mkdtemp(prefix="video_summarizer_chunks_")
        chunk_pattern = str(Path(chunk_dir) / "chunk_%03d.mp3")

        ffmpeg_path = get_ffmpeg_path()
        cmd = [
            ffmpeg_path,
            "-i",
            str(audio_path),
            "-f",
            "segment",
            "-segment_time",
            str(self.chunk_duration_sec),
            "-c",
            "copy",
            "-map",
            "0:a",  # Only copy audio stream
            chunk_pattern,
        ]

        result = run_subprocess(cmd)
        if result.returncode != 0:
            raise TranscriptionError(f"Failed to split audio: {result.stderr}")

        chunks = sorted(Path(chunk_dir).glob("chunk_*.mp3"))
        logger.info(f"Split audio into {len(chunks)} chunks")
        for i, chunk in enumerate(chunks):
            logger.debug(f"  Chunk {i}: {chunk.name} ({chunk.stat().st_size / 1024:.1f} KB)")

        return chunks

    def _transcribe_single(self, audio_path: Path) -> Transcript:
        """Transcribe audio in a single request.

        Args:
            audio_path: Path to audio file

        Returns:
            Transcript object
        """
        import mimetypes

        url = f"{self.api_base}/audio/transcriptions"
        content_type = mimetypes.guess_type(audio_path)[0] or "audio/mpeg"

        try:
            with open(audio_path, "rb") as audio_file:
                files = {"file": (audio_path.name, audio_file, content_type)}
                data = self._build_request_data()

                response = self.client.post(url, files=files, data=data)
                response.raise_for_status()

                return self._parse_response(response, audio_path)

        except httpx.HTTPStatusError as e:
            raise TranscriptionError(f"API request failed: {e.response.status_code}") from e
        except httpx.RequestError as e:
            raise TranscriptionError(f"Request failed: {e}") from e
        except Exception as e:
            raise TranscriptionError(f"Transcription failed: {e}") from e

    def _build_request_data(self) -> dict:
        """Build request data for API call.

        Returns:
            Dictionary with request parameters
        """
        data = {"model": self.model}

        if self.response_format:
            data["response_format"] = self.response_format
        if self.vad_filter:
            data["vad_filter"] = "true"
        if self.language:
            data["language"] = self.language

        return data

    def _parse_response(self, response: httpx.Response, audio_path: Path) -> Transcript:
        """Parse API response based on format.

        Args:
            response: HTTP response from API
            audio_path: Original audio path for duration fallback

        Returns:
            Transcript object
        """
        if self.response_format in ("verbose_json", "json"):
            return self._parse_json_response(response)
        return self._parse_text_response(response, audio_path)

    def _parse_json_response(self, response: httpx.Response) -> Transcript:
        """Parse JSON response from API.

        Args:
            response: HTTP response

        Returns:
            Transcript object
        """
        result = response.json()

        if "text" not in result:
            raise TranscriptionError("API response missing 'text' field")

        logger.info(
            f"Transcription completed: {len(result.get('text', ''))} chars, "
            f"duration={result.get('duration', 0):.1f}s"
        )

        return Transcript(
            text=result.get("text", ""),
            duration=result.get("duration", 0.0),
            language=result.get("language"),
            confidence=None,
            raw_response=result,
            response_format=self.response_format,
        )

    def _parse_text_response(self, response: httpx.Response, audio_path: Path) -> Transcript:
        """Parse text/srt/vtt response from API.

        Args:
            response: HTTP response
            audio_path: Original audio path for duration fallback

        Returns:
            Transcript object
        """
        result = response.text
        duration = self._get_audio_duration(audio_path) or 0.0

        logger.info(f"Transcription completed: {len(result)} chars, duration={duration:.1f}s")

        return Transcript(
            text=result,
            duration=duration,
            language=self.language,
            confidence=None,
            raw_response=result,
            response_format=self.response_format,
        )

    def _transcribe_chunked(self, audio_path: Path, total_duration: float) -> Transcript:
        """Transcribe audio by splitting into chunks.

        Args:
            audio_path: Path to audio file
            total_duration: Total audio duration in seconds

        Returns:
            Transcript object with combined results
        """
        chunks = self._split_audio(audio_path)

        try:
            if self.response_format in ("verbose_json", "json"):
                return self._merge_chunked_json_responses(chunks, total_duration)
            return self._merge_chunked_text_responses(chunks, total_duration)
        finally:
            cleanup_chunk_directory(chunks)

    def _merge_chunked_json_responses(
        self, chunks: list[Path], total_duration: float
    ) -> Transcript:
        """Merge chunked JSON responses with timestamp adjustment.

        Adjusts segment and word timestamps based on chunk position.
        Only called when response_format is verbose_json or json.

        Args:
            chunks: List of chunk file paths
            total_duration: Total audio duration in seconds

        Returns:
            Transcript object with merged JSON response
        """
        logger.info(f"Created {len(chunks)} chunks for {total_duration:.1f}s audio")
        for chunk in chunks:
            logger.debug(f"  Chunk: {chunk.name} ({chunk.stat().st_size / 1024:.1f} KB)")

        merger = JsonChunkMerger(self.chunk_duration_sec)
        merger.process_chunks(chunks, self._transcribe_single)

        if merger.successful_chunks == 0:
            logger.error("All chunks failed to transcribe")
            return Transcript(
                text="",
                duration=total_duration,
                language=None,
                confidence=None,
                raw_response={"error": "All transcription chunks failed"},
                response_format=self.response_format,
            )

        merged_response = merger.build_response(total_duration)
        logger.info(
            f"Chunked JSON merge complete: {len(merger.all_text)} chars, "
            f"{merger.successful_chunks}/{len(chunks)} chunks, "
            f"{len(merger.combined_segments)} segments, "
            f"{len(merger.combined_words)} words"
        )

        return Transcript(
            text=" ".join(merger.all_text),
            duration=total_duration,
            language=merger.detected_language,
            confidence=None,
            raw_response=merged_response,
            response_format=self.response_format,
        )

    def _merge_chunked_text_responses(
        self, chunks: list[Path], total_duration: float
    ) -> Transcript:
        """Merge chunked text responses.

        Used for text, srt, vtt formats where JSON merging is not applicable.

        Args:
            chunks: List of chunk file paths
            total_duration: Total audio duration in seconds

        Returns:
            Transcript object with combined text
        """
        logger.info(f"Created {len(chunks)} chunks for {total_duration:.1f}s audio")
        for chunk in chunks:
            logger.debug(f"  Chunk: {chunk.name} ({chunk.stat().st_size / 1024:.1f} KB)")

        all_text = []

        for i, chunk_path in enumerate(chunks, 1):
            logger.info(f"Transcribing chunk {i}/{len(chunks)}: {chunk_path.name}")

            try:
                transcript = self._transcribe_single(chunk_path)
                logger.debug(f"  Chunk {i} transcript: {transcript.text[:100]}...")
                all_text.append(transcript.text)
            except Exception as e:
                logger.error(f"Failed to transcribe chunk {i}: {e}")
                all_text.append(f"[Chunk {i} transcription failed]")

        combined_text = " ".join(all_text)

        logger.info(
            f"Chunked transcription complete: {len(combined_text)} chars from {len(chunks)} chunks"
        )

        return Transcript(
            text=combined_text,
            duration=total_duration,
            language=None,
            confidence=None,
            raw_response=None,
            response_format=None,
        )

    def is_available(self) -> bool:
        """Check if Speaches API is available.

        Returns:
            True if API is reachable
        """
        try:
            response = self.client.get(f"{self.api_base}/models")
            return bool(response.status_code == 200)
        except Exception:
            return False

    def __del__(self) -> None:
        """Cleanup HTTP client."""
        if hasattr(self, "client"):
            self.client.close()


class JsonChunkMerger:
    """Helper class to merge JSON transcript chunks with timestamp adjustment."""

    def __init__(self, chunk_duration_sec: int):
        """Initialize merger.

        Args:
            chunk_duration_sec: Duration of each chunk in seconds
        """
        self.chunk_duration_sec = chunk_duration_sec
        self.all_text: list[str] = []
        self.combined_segments: list[dict] = []
        self.combined_words: list[dict] = []
        self.segment_id_counter = 0
        self.detected_language: str | None = None
        self.successful_chunks = 0

    def process_chunks(
        self, chunks: list[Path], transcribe_func: typing.Callable[[Path], Transcript]
    ) -> None:
        """Process all chunks and merge results.

        Args:
            chunks: List of chunk file paths
            transcribe_func: Function to transcribe a single chunk
        """
        for i, chunk_path in enumerate(chunks):
            time_offset = i * self.chunk_duration_sec
            logger.info(f"Transcribing chunk {i + 1}/{len(chunks)}: {chunk_path.name}")

            try:
                transcript = transcribe_func(chunk_path)
                if isinstance(transcript.raw_response, dict):
                    self._merge_chunk_data(transcript.raw_response, transcript.text, time_offset, i)
                self.successful_chunks += 1
            except Exception as e:
                logger.error(f"Failed to transcribe chunk {i}: {e}")

    def _merge_chunk_data(
        self, chunk_data: dict, text: str, time_offset: float, chunk_index: int
    ) -> None:
        """Merge data from a single chunk.

        Args:
            chunk_data: Raw response data from API
            text: Transcribed text
            time_offset: Time offset for this chunk
            chunk_index: Index of the chunk
        """
        if not isinstance(chunk_data, dict):
            logger.warning(f"Chunk {chunk_index}: raw_response is not dict, skipping in merge")
            return

        self.all_text.append(text)

        if self.detected_language is None:
            self.detected_language = chunk_data.get("language")

        self._merge_segments(chunk_data, time_offset)
        self._merge_words(chunk_data, time_offset)

        logger.debug(
            f"  Chunk {chunk_index}: {len(text)} chars, "
            f"{len(chunk_data.get('segments', []))} segments"
        )

    def _merge_segments(self, chunk_data: dict, time_offset: float) -> None:
        """Merge and adjust segment timestamps.

        Args:
            chunk_data: Chunk data dictionary
            time_offset: Time offset to add to timestamps
        """
        segments = chunk_data.get("segments")
        if not isinstance(segments, list):
            return

        for segment in segments:
            adjusted_segment = segment.copy()
            adjusted_segment["id"] = self.segment_id_counter
            adjusted_segment["start"] = segment["start"] + time_offset
            adjusted_segment["end"] = segment["end"] + time_offset
            self.combined_segments.append(adjusted_segment)
            self.segment_id_counter += 1

    def _merge_words(self, chunk_data: dict, time_offset: float) -> None:
        """Merge and adjust word timestamps.

        Args:
            chunk_data: Chunk data dictionary
            time_offset: Time offset to add to timestamps
        """
        words = chunk_data.get("words")
        if not isinstance(words, list):
            return

        for word in words:
            adjusted_word = word.copy()
            adjusted_word["start"] = word["start"] + time_offset
            adjusted_word["end"] = word["end"] + time_offset
            self.combined_words.append(adjusted_word)

    def build_response(self, total_duration: float) -> dict:
        """Build the final merged response.

        Args:
            total_duration: Total audio duration

        Returns:
            Merged response dictionary
        """
        merged_response = {
            "text": " ".join(self.all_text),
            "duration": total_duration,
            "language": self.detected_language,
            "segments": self.combined_segments,
        }

        if self.combined_words:
            merged_response["words"] = self.combined_words

        return merged_response


# Utility functions


def get_ffmpeg_path() -> str:
    """Get ffmpeg path from environment or default.

    Returns:
        Path to ffmpeg binary
    """
    ffmpeg_path = os.environ.get("FFMPEG_BINARY", "auto-detect")
    return "ffmpeg" if ffmpeg_path == "auto-detect" else ffmpeg_path


def get_ffprobe_path() -> str:
    """Get ffprobe path from environment or default.

    Returns:
        Path to ffprobe binary
    """
    ffprobe_path = os.environ.get("FFPROBE_BINARY", "auto-detect")
    return "ffprobe" if ffprobe_path == "auto-detect" else ffprobe_path


def run_subprocess(cmd: list[str], timeout: int = 10) -> subprocess.CompletedProcess[str]:
    """Run subprocess command and return result.

    Args:
        cmd: Command and arguments
        timeout: Timeout in seconds

    Returns:
        subprocess.CompletedProcess result with text output
    """
    import subprocess

    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def get_duration_via_ffprobe(audio_path: Path) -> float | None:
    """Get audio duration using ffprobe.

    Args:
        audio_path: Path to audio file

    Returns:
        Duration in seconds or None if detection fails
    """
    cmd = [
        get_ffprobe_path(),
        "-i",
        str(audio_path),
        "-show_entries",
        "format=duration",
        "-v",
        "quiet",
        "-of",
        "csv=p=0",
    ]

    try:
        result = run_subprocess(cmd)
        if result.returncode == 0:
            duration_str = result.stdout.strip()
            if duration_str:
                return float(duration_str)
    except Exception as e:
        logger.debug(f"ffprobe duration detection failed: {e}")

    return None


def get_duration_via_mutagen(audio_path: Path) -> float | None:
    """Get audio duration using mutagen library.

    Args:
        audio_path: Path to audio file

    Returns:
        Duration in seconds or None if detection fails
    """
    try:
        from mutagen import File

        audio_file = File(audio_path)
        if audio_file and audio_file.info.length:
            duration: float = audio_file.info.length
            logger.info(f"Got duration from mutagen: {duration:.1f}s")
            return duration
    except ImportError:
        logger.debug("mutagen not available for duration detection")
    except Exception as e:
        logger.debug(f"mutagen duration detection failed: {e}")

    logger.warning("Could not detect audio duration with any available method")
    return None


def estimate_duration_from_file_size(audio_path: Path) -> float:
    """Estimate audio duration from file size as fallback.

    This is a rough heuristic used when ffprobe is unavailable.
    Assumes typical audio compression: ~128 kbps for MP3/M4A.

    Args:
        audio_path: Path to audio file

    Returns:
        Estimated duration in seconds
    """
    file_size_bytes = audio_path.stat().st_size
    file_size_bits = file_size_bytes * 8
    estimated_duration = file_size_bits / _ESTIMATED_BITRATE

    logger.debug(
        f"Estimated duration from file size: {estimated_duration:.1f}s "
        f"(file size: {file_size_bytes / 1024:.1f} KB)"
    )

    return estimated_duration


def cleanup_chunk_directory(chunks: list[Path]) -> None:
    """Clean up temporary chunk directory.

    Args:
        chunks: List of chunk file paths
    """
    chunk_dir = chunks[0].parent if chunks else None
    if chunk_dir and chunk_dir.exists():
        shutil.rmtree(chunk_dir, ignore_errors=True)

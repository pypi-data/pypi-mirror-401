"""Speech-to-text transcription using Speaches."""

import logging
import os
import shutil
import tempfile
from pathlib import Path

import httpx

from video_summarizer.core.base import Transcriber
from video_summarizer.utils.errors import TranscriptionError
from video_summarizer.utils.types import Transcript

logger = logging.getLogger(__name__)


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
        """
        if not audio_path.exists():
            raise TranscriptionError(f"Audio file does not exist: {audio_path}")

        # Check if file needs chunking
        duration = self._get_audio_duration(audio_path)
        logger.info(f"Detected audio duration: {duration}")

        if duration is None:
            # Duration unknown - use chunked transcription as safer fallback
            logger.warning(
                "Could not detect audio duration (ffprobe unavailable). "
                "Using chunked transcription to ensure completeness. "
                "Install ffprobe or set FFPROBE_BINARY in .env for accurate duration detection."
            )
            estimated_duration = self._estimate_duration_from_file_size(audio_path)
            logger.info(f"Estimated duration from file size: {estimated_duration:.1f}s")
            return self._transcribe_chunked(audio_path, estimated_duration)
        elif duration > self.chunk_duration_threshold:
            logger.info(
                f"Audio duration {duration:.1f}s exceeds {self.chunk_duration_threshold}s, "
                "using chunked transcription"
            )
            return self._transcribe_chunked(audio_path, duration)
        else:
            logger.info(f"Audio duration {duration:.1f}s, using single-request transcription")
            return self._transcribe_single(audio_path)

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
        import subprocess

        # Method 1: Try ffprobe
        ffprobe_path = os.environ.get("FFPROBE_BINARY", "auto-detect")
        if ffprobe_path == "auto-detect":
            ffprobe_path = "ffprobe"

        cmd = [
            ffprobe_path,
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
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                duration_str = result.stdout.strip()
                if duration_str:
                    return float(duration_str)
        except (subprocess.TimeoutExpired, ValueError, FileNotFoundError) as e:
            logger.debug(f"ffprobe duration detection failed: {e}")

        # Method 2: Try mutagen (optional dependency)
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

    def _estimate_duration_from_file_size(self, audio_path: Path) -> float:
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

        # Conservative estimate: assume 128 kbps (typical MP3/M4A bitrate)
        estimated_bitrate = 128_000  # 128 kbps in bits per second
        estimated_duration = file_size_bits / estimated_bitrate

        logger.debug(
            f"Estimated duration from file size: {estimated_duration:.1f}s "
            f"(file size: {file_size_bytes / 1024:.1f} KB)"
        )

        return estimated_duration

    def _split_audio(self, audio_path: Path) -> list[Path]:
        """Split audio file into chunks.

        Args:
            audio_path: Path to audio file

        Returns:
            List of paths to audio chunks
        """
        import subprocess

        chunk_dir = tempfile.mkdtemp(prefix="video_summarizer_chunks_")
        chunk_pattern = str(Path(chunk_dir) / "chunk_%03d.mp3")

        # Get ffmpeg path from configuration
        ffmpeg_path = os.environ.get("FFMPEG_BINARY", "auto-detect")
        if ffmpeg_path == "auto-detect":
            ffmpeg_path = "ffmpeg"

        # Use ffmpeg to split audio into chunks
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

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise TranscriptionError(f"Failed to split audio: {result.stderr}")

        # Sort chunks by name to ensure correct order (chunk_000, chunk_001, etc.)
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
                data = {"model": self.model}

                # Add optional parameters
                if self.response_format:
                    data["response_format"] = self.response_format
                if self.vad_filter:
                    data["vad_filter"] = "true"
                if self.language:
                    data["language"] = self.language

                response = self.client.post(url, files=files, data=data)
                response.raise_for_status()

                # Handle different response formats
                if self.response_format in ["verbose_json", "json"]:
                    # JSON response - parse as dict
                    result = response.json()

                    # Validate response
                    if "text" not in result:
                        raise TranscriptionError("API response missing 'text' field")

                    # Log for debugging
                    logger.info(
                        f"Transcription completed: {len(result.get('text', ''))} chars, "
                        f"duration={result.get('duration', 0):.1f}s"
                    )

                    return Transcript(
                        text=result.get("text", ""),
                        duration=result.get("duration", 0.0),
                        language=result.get("language"),
                        confidence=None,
                        raw_response=result,  # Store full JSON response
                        response_format=self.response_format,
                    )
                else:
                    # text, srt, vtt - response is plain text
                    result = response.text

                    # For text/srt/vtt, duration may not be in response
                    duration = self._get_audio_duration(audio_path) or 0.0

                    logger.info(
                        f"Transcription completed: {len(result)} chars, duration={duration:.1f}s"
                    )

                    return Transcript(
                        text=result,  # Full response is the text
                        duration=duration,
                        language=self.language,  # Use configured language if set
                        confidence=None,
                        raw_response=result,  # Store raw text/srt/vtt
                        response_format=self.response_format,
                    )

        except httpx.HTTPStatusError as e:
            raise TranscriptionError(f"API request failed: {e.response.status_code}") from e
        except httpx.RequestError as e:
            raise TranscriptionError(f"Request failed: {e}") from e
        except Exception as e:
            raise TranscriptionError(f"Transcription failed: {e}") from e

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
            # Route based on response format
            if self.response_format in ["verbose_json", "json"]:
                return self._merge_chunked_json_responses(chunks, total_duration)
            else:
                return self._merge_chunked_text_responses(chunks, total_duration)
        finally:
            # Clean up temporary chunks
            chunk_dir = chunks[0].parent if chunks else None
            if chunk_dir and chunk_dir.exists():
                shutil.rmtree(chunk_dir, ignore_errors=True)

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

        # Initialize accumulators
        all_text = []
        combined_segments = []
        combined_words = []
        segment_id_counter = 0
        detected_language = None
        successful_chunks = 0

        for i, chunk_path in enumerate(chunks, start=0):
            time_offset = i * self.chunk_duration_sec
            logger.info(f"Transcribing chunk {i + 1}/{len(chunks)}: {chunk_path.name}")

            try:
                transcript = self._transcribe_single(chunk_path)

                # Validate response is JSON dict
                if not isinstance(transcript.raw_response, dict):
                    logger.warning(f"Chunk {i}: raw_response is not dict, skipping in merge")
                    continue

                chunk_data = transcript.raw_response
                all_text.append(transcript.text)

                # Capture language from first successful chunk
                if detected_language is None:
                    detected_language = chunk_data.get("language")

                # Merge and adjust segments
                if "segments" in chunk_data and isinstance(chunk_data["segments"], list):
                    for segment in chunk_data["segments"]:
                        adjusted_segment = segment.copy()
                        adjusted_segment["id"] = segment_id_counter
                        adjusted_segment["start"] = segment["start"] + time_offset
                        adjusted_segment["end"] = segment["end"] + time_offset
                        combined_segments.append(adjusted_segment)
                        segment_id_counter += 1

                # Merge and adjust words (if present)
                if "words" in chunk_data and isinstance(chunk_data["words"], list):
                    for word in chunk_data["words"]:
                        adjusted_word = word.copy()
                        adjusted_word["start"] = word["start"] + time_offset
                        adjusted_word["end"] = word["end"] + time_offset
                        combined_words.append(adjusted_word)

                successful_chunks += 1
                logger.debug(
                    f"  Chunk {i}: {len(transcript.text)} chars, "
                    f"{len(chunk_data.get('segments', []))} segments"
                )

            except Exception as e:
                logger.error(f"Failed to transcribe chunk {i}: {e}")
                # Continue with next chunk

        # Handle complete failure
        if successful_chunks == 0:
            logger.error("All chunks failed to transcribe")
            return Transcript(
                text="",
                duration=total_duration,
                language=None,
                confidence=None,
                raw_response={"error": "All transcription chunks failed"},
                response_format=self.response_format,
            )

        # Build combined response
        combined_text = " ".join(all_text)
        merged_response = {
            "text": combined_text,
            "duration": total_duration,
            "language": detected_language,
            "segments": combined_segments,
        }

        # Only include words if we have any
        if combined_words:
            merged_response["words"] = combined_words

        logger.info(
            f"Chunked JSON merge complete: {len(combined_text)} chars, "
            f"{successful_chunks}/{len(chunks)} chunks, "
            f"{len(combined_segments)} segments, "
            f"{len(combined_words)} words"
        )

        return Transcript(
            text=combined_text,
            duration=total_duration,
            language=detected_language,
            confidence=None,
            raw_response=merged_response,
            response_format=self.response_format,
        )

    def _merge_chunked_text_responses(
        self, chunks: list[Path], total_duration: float
    ) -> Transcript:
        """Merge chunked text responses (original behavior).

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
                # Continue with next chunk instead of failing completely
                all_text.append(f"[Chunk {i} transcription failed]")

        # Combine all chunks with proper spacing
        combined_text = " ".join(all_text)

        logger.info(
            f"Chunked transcription complete: {len(combined_text)} chars from {len(chunks)} chunks"
        )

        return Transcript(
            text=combined_text,
            duration=total_duration,
            language=None,
            confidence=None,
            raw_response=None,  # Cannot preserve chunked responses for text formats
            response_format=None,  # Indicates combined transcript
        )

    def is_available(self) -> bool:
        """Check if Speaches API is available."""
        try:
            response = self.client.get(f"{self.api_base}/models")
            return bool(response.status_code == 200)
        except Exception:
            return False

    def __del__(self) -> None:
        """Cleanup HTTP client."""
        if hasattr(self, "client"):
            self.client.close()

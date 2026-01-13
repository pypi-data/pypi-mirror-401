"""Transcript chunking for long content."""

from dataclasses import dataclass


@dataclass
class TextChunk:
    """A chunk of text with metadata."""

    text: str
    start_token: int
    end_token: int
    chunk_index: int


class TranscriptChunker:
    """Split long transcripts into manageable chunks."""

    def __init__(
        self,
        max_tokens: int = 4000,
        overlap_tokens: int = 200,
        overhead_tokens: int = 100,
    ) -> None:
        """Initialize chunker.

        Args:
            max_tokens: Maximum tokens per chunk
            overlap_tokens: Overlap between chunks
            overhead_tokens: Tokens reserved for system message
        """
        self.max_tokens = max_tokens - overhead_tokens
        self.overlap_tokens = overlap_tokens
        self.overhead_tokens = overhead_tokens

    def chunk(self, text: str, token_count: int) -> list[TextChunk]:
        """Split text into chunks based on token count.

        Args:
            text: Text to chunk
            token_count: Total token count of text

        Returns:
            List of TextChunk objects
        """
        if token_count <= self.max_tokens:
            return [
                TextChunk(
                    text=text,
                    start_token=0,
                    end_token=token_count,
                    chunk_index=0,
                )
            ]

        chunks: list[TextChunk] = []
        # Simple character-based splitting (rough approximation)
        # For production, use proper tokenizer
        chars_per_token = len(text) / token_count
        max_chars = int(self.max_tokens * chars_per_token)
        overlap_chars = int(self.overlap_tokens * chars_per_token)

        start = 0
        chunk_index = 0

        while start < len(text):
            end = min(start + max_chars, len(text))

            # Try to break at sentence boundary
            if end < len(text):
                end = self._find_sentence_boundary(text, end)

            chunk_text = text[start:end].strip()
            chunks.append(
                TextChunk(
                    text=chunk_text,
                    start_token=start,
                    end_token=end,
                    chunk_index=chunk_index,
                )
            )

            chunk_index += 1

            # If we've reached the end, we're done
            if end >= len(text):
                break

            start = end - overlap_chars

        return chunks

    def _find_sentence_boundary(self, text: str, position: int) -> int:
        """Find nearest sentence boundary near position."""
        # Look for sentence endings within 100 characters
        search_window = 100
        window_start = max(0, position - search_window)
        window_end = min(len(text), position + search_window)
        window = text[window_start:window_end]

        # Search for common sentence endings
        for pattern in [". ", "! ", "? ", "\n"]:
            idx = window.rfind(pattern, 0, position - window_start + search_window // 2)
            if idx != -1:
                return window_start + idx + len(pattern)

        # No sentence boundary found, return original position
        return position

"""Transcript chunking for long content."""

from dataclasses import dataclass

# Sentence boundary patterns for chunk splitting
_SENTENCE_ENDINGS = (". ", "! ", "? ", "\n")
_SEARCH_WINDOW = 100  # Characters to search for sentence boundaries


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

        return self._split_into_chunks(text, token_count)

    def _split_into_chunks(self, text: str, token_count: int) -> list[TextChunk]:
        """Split text into multiple chunks.

        Args:
            text: Text to chunk
            token_count: Total token count of text

        Returns:
            List of TextChunk objects
        """
        chunks: list[TextChunk] = []
        chars_per_token = len(text) / token_count
        max_chars = int(self.max_tokens * chars_per_token)
        overlap_chars = int(self.overlap_tokens * chars_per_token)

        start = 0
        chunk_index = 0

        while start < len(text):
            end = self._find_chunk_end(text, start, max_chars)
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

            if end >= len(text):
                break

            start = end - overlap_chars

        return chunks

    def _find_chunk_end(self, text: str, start: int, max_chars: int) -> int:
        """Find the end position for a chunk.

        Args:
            text: Full text
            start: Starting position for chunk
            max_chars: Maximum characters for chunk

        Returns:
            End position for the chunk
        """
        end = min(start + max_chars, len(text))

        if end < len(text):
            end = self._find_sentence_boundary(text, end)

        return end

    def _find_sentence_boundary(self, text: str, position: int) -> int:
        """Find nearest sentence boundary near position.

        Args:
            text: Full text
            position: Desired end position

        Returns:
            Position of sentence boundary, or original position if none found
        """
        window_start = max(0, position - _SEARCH_WINDOW)
        window_end = min(len(text), position + _SEARCH_WINDOW)
        window = text[window_start:window_end]

        for pattern in _SENTENCE_ENDINGS:
            idx = window.rfind(pattern, 0, position - window_start + _SEARCH_WINDOW // 2)
            if idx != -1:
                return window_start + idx + len(pattern)

        return position

"""Transcript preprocessing and cleaning."""

import re

from video_summarizer.utils.types import Transcript


class TranscriptPreprocessor:
    """Clean and preprocess transcript text."""

    # Common filler words to remove
    FILLER_WORDS = [
        "um",
        "uh",
        "like",
        "you know",
        "actually",
        "basically",
        "literally",
        "I mean",
        "kind of",
        "sort of",
    ]

    def __init__(self, remove_fillers: bool = True, normalize_whitespace: bool = True) -> None:
        """Initialize preprocessor.

        Args:
            remove_fillers: Whether to remove filler words
            normalize_whitespace: Whether to normalize whitespace
        """
        self.remove_fillers = remove_fillers
        self.normalize_whitespace = normalize_whitespace

    def clean(self, transcript: Transcript) -> str:
        """Clean transcript text.

        Args:
            transcript: Transcript object

        Returns:
            Cleaned text string
        """
        text = transcript.text

        if self.normalize_whitespace:
            text = self._normalize_whitespace(text)

        if self.remove_fillers:
            text = self._remove_filler_words(text)

        text = self._remove_timestamps(text)
        text = self._clean_punctuation(text)

        return text.strip()

    def _normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace in text.

        Args:
            text: Input text

        Returns:
            Text with normalized whitespace
        """
        return re.sub(r"\s+", " ", text)

    def _remove_filler_words(self, text: str) -> str:
        """Remove common filler words.

        Args:
            text: Input text

        Returns:
            Text with filler words removed
        """
        pattern = r"\b(?:{})\b".format("|".join(re.escape(w) for w in self.FILLER_WORDS))
        return re.sub(pattern, "", text, flags=re.IGNORECASE)

    def _remove_timestamps(self, text: str) -> str:
        """Remove timestamp patterns like [00:01:23].

        Args:
            text: Input text

        Returns:
            Text with timestamps removed
        """
        return re.sub(r"\[\d{1,2}:\d{2}:\d{2}\]", "", text)

    def _clean_punctuation(self, text: str) -> str:
        """Clean up excessive punctuation.

        Args:
            text: Input text

        Returns:
            Text with cleaned punctuation
        """
        # Remove multiple consecutive punctuation marks
        text = re.sub(r"([!?.]){2,}", r"\1", text)
        # Remove punctuation before sentence end
        text = re.sub(r"[,:;]+(?=[.!?])", "", text)
        return text

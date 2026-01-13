"""Text summarization using LLM APIs."""

import time
from dataclasses import dataclass

from openai import APIConnectionError, APIError, OpenAI, RateLimitError

from video_summarizer.config import constants
from video_summarizer.core.base import Summarizer
from video_summarizer.utils.errors import SummarizationError
from video_summarizer.utils.types import Summary, SummaryStyle, Transcript


@dataclass
class ResponseInfo:
    """API response information."""

    content: str
    total_tokens: int


class OpenAISummarizer(Summarizer):
    """Summarize transcripts using OpenAI-compatible API."""

    # Style instructions for different summary types
    _STYLE_INSTRUCTIONS: dict[SummaryStyle, str] = {
        SummaryStyle.BRIEF: "Provide a very brief 2-3 sentence summary.",
        SummaryStyle.DETAILED: "Provide a comprehensive summary with key details.",
        SummaryStyle.BULLET_POINTS: "Provide a summary using bullet points.",
        SummaryStyle.CONCISE: "Provide a concise summary in one paragraph.",
    }

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.openai.com/v1",
        model: str = "gpt-4o",
        max_tokens: int = 2000,
        temperature: float = 0.7,
    ) -> None:
        """Initialize summarizer.

        Args:
            api_key: OpenAI API key
            base_url: API base URL
            model: Model to use
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
        """
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

    def summarize(self, transcript: Transcript, style: str | None = None) -> Summary:
        """Summarize transcript text.

        Args:
            transcript: Transcript object
            style: Optional summary style

        Returns:
            Summary object

        Raises:
            SummarizationError: If summarization fails
        """
        summary_style = SummaryStyle(style) if style else SummaryStyle.CONCISE
        prompt = self._build_prompt(transcript.text, summary_style)

        try:
            response = self._call_api_with_retry(prompt)

            return Summary(
                text=response.content,
                model=self.model,
                tokens_used=response.total_tokens,
                style=summary_style,
            )

        except Exception as e:
            raise SummarizationError(f"Summarization failed: {e}") from e

    def count_tokens(self, text: str) -> int:
        """Count tokens in text (rough approximation).

        Args:
            text: Input text

        Returns:
            Estimated token count
        """
        # Rough approximation: ~4 characters per token for English
        return len(text) // 4

    def _build_prompt(self, text: str, style: SummaryStyle) -> str:
        """Build summarization prompt.

        Args:
            text: Transcript text
            style: Summary style

        Returns:
            Formatted prompt
        """
        instruction = self._STYLE_INSTRUCTIONS.get(
            style, self._STYLE_INSTRUCTIONS[SummaryStyle.CONCISE]
        )
        return f"{instruction}\n\nTranscript:\n{text}"

    def _call_api_with_retry(self, prompt: str) -> ResponseInfo:
        """Call API with retry logic.

        Args:
            prompt: Prompt to send

        Returns:
            Response info object

        Raises:
            SummarizationError: If all retries fail
        """
        last_error: Exception | None = None

        for attempt in range(constants.MAX_API_RETRIES):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": constants.DEFAULT_SYSTEM_PROMPT,
                        },
                        {"role": "user", "content": prompt},
                    ],
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                )

                return ResponseInfo(
                    content=response.choices[0].message.content or "",
                    total_tokens=response.usage.total_tokens if response.usage else 0,
                )

            except RateLimitError as e:
                last_error = e
                wait_time = constants.API_RETRY_DELAY * (constants.API_BACKOFF_FACTOR**attempt)
                time.sleep(wait_time)

            except (APIConnectionError, APIError) as e:
                last_error = e
                if attempt == constants.MAX_API_RETRIES - 1:
                    raise

        raise SummarizationError(
            f"API call failed after {constants.MAX_API_RETRIES} attempts: {last_error}"
        )

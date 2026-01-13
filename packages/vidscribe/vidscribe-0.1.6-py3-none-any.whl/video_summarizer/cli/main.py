"""Main CLI application for video summarizer."""

from pathlib import Path
from typing import TYPE_CHECKING

import rich_click as click

if TYPE_CHECKING:
    import httpx
from rich.console import Console
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.style import Style
from rich.text import Text

from video_summarizer.config.settings import OutputConfig, Settings
from video_summarizer.scraper.downloader import YtDlpDownloader
from video_summarizer.scraper.validator import VideoURLValidator
from video_summarizer.summarizer.preprocessor import TranscriptPreprocessor
from video_summarizer.summarizer.summarizer import OpenAISummarizer
from video_summarizer.transcriber.container import SpeachesContainerManager
from video_summarizer.transcriber.extractor import MoviePyAudioExtractor
from video_summarizer.transcriber.transcriber import SpeachesTranscriber
from video_summarizer.utils.errors import VideoSummarizerError
from video_summarizer.utils.gpu_checker import GPUAvailability, check_gpu_availability, get_gpu_info
from video_summarizer.utils.logging import setup_logging
from video_summarizer.utils.types import Summary, Transcript

console = Console(force_terminal=True, legacy_windows=False)


def _check_gpu_if_requested(use_gpu: bool) -> None:
    """Check GPU availability if requested and warn if unavailable.

    Args:
        use_gpu: Whether GPU was requested

    Raises:
        click.ClickException: If GPU requested but not available
    """
    if not use_gpu:
        return

    gpu_check = check_gpu_availability()

    if not gpu_check.available:
        _print_gpu_unavailable_message(gpu_check)
        raise click.ClickException("GPU support requested but not available")

    _print_gpu_available_message()


def _print_gpu_unavailable_message(gpu_check: GPUAvailability) -> None:
    """Print GPU unavailability error with suggested solutions.

    Args:
        gpu_check: GPU availability check results
    """
    console.print("[bold red]✗[/bold red] GPU support requested but not available:\n")
    console.print(f"  [red]{gpu_check.error_message}[/red]\n")
    console.print("[yellow]Solutions:[/yellow]")

    if not gpu_check.nvidia_installed:
        console.print("  1. Install NVIDIA GPU drivers for your system")
        console.print("  2. Verify installation: nvidia-smi")
    elif not gpu_check.nvidia_docker_available:
        console.print("  1. Install NVIDIA Container Toolkit:")
        console.print(
            "     https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html"
        )
        console.print("  2. Restart Docker after installation")
        console.print(
            "  3. Verify: docker run --rm --gpus all nvidia/cuda:11.0.3-base-ubuntu20.04 nvidia-smi"
        )

    console.print("\n[dim]Or use CPU mode (remove --gpu flag)[/dim]")


def _print_gpu_available_message() -> None:
    """Print GPU availability information."""
    gpu_info = get_gpu_info()
    gpus = gpu_info.get("gpus")

    if not gpus or not isinstance(gpus, list):
        return

    console.print(f"[green]✓[/green] GPU available: {gpu_info['count']} GPU(s) detected")
    for gpu in gpus:
        console.print(f"  [dim]{gpu}[/dim]")


def _get_ffmpeg_location(settings: Settings) -> str | None:
    """Get ffmpeg location from settings, returning None if set to auto-detect."""
    if settings.moviepy.ffmpeg_binary == "auto-detect":
        return None
    return settings.moviepy.ffmpeg_binary


def _ensure_container_running(settings: Settings) -> SpeachesContainerManager:
    """Ensure the Speaches container is running and return the manager."""
    console.print("[cyan]Ensuring Speaches container is running...[/cyan]")
    container_mgr = SpeachesContainerManager(
        container_name=settings.transcriber.container_name,
        container_port=settings.transcriber.container_port,
        container_image=settings.transcriber.get_container_image(),
        use_gpu=settings.transcriber.use_gpu,
    )

    if not container_mgr.is_running():
        gpu_msg = " (GPU)" if settings.transcriber.use_gpu else " (CPU)"
        with console.status(f"[bold green]Starting Speaches container{gpu_msg}..."):
            container_mgr.start()
        console.print("[green]✓[/green] Container started")

    return container_mgr


def _download_model_with_progress(
    container_mgr: SpeachesContainerManager,
    model: str,
) -> dict:
    """Download model with live progress display."""
    console.print(f"[cyan]Ensuring Whisper model is available: {model}[/cyan]")
    status_text = Text.from_markup("[bold green]Initializing download...[/bold green]")

    def progress_callback(stats: dict) -> None:
        mb_downloaded = stats["bytes_downloaded"] / (1024 * 1024)
        speed = stats["speed_mbps"]
        elapsed = stats["elapsed_seconds"]

        status_text.plain = (
            f"Downloading {model}\n"
            f"  Downloaded: {mb_downloaded:.1f} MB\n"
            f"  Speed: {speed:.2f} MB/s\n"
            f"  Elapsed: {elapsed:.0f}s"
        )
        status_text.stylize(Style(bold=True, color="green"), 0, len(f"Downloading {model}"))

    with Live(status_text, console=console, refresh_per_second=2) as live:

        def update_display(stats: dict) -> None:
            progress_callback(stats)
            live.update(status_text)

        result = container_mgr.ensure_model(model, progress_callback=update_display)

    return result


def _print_download_result(result: dict) -> None:
    """Print the result of a model download operation.

    Args:
        result: Dictionary with download status and statistics
    """
    status = result.get("status")

    if status == "complete":
        elapsed = result.get("elapsed_seconds", 0)
        mb = result.get("bytes_downloaded", 0) / (1024 * 1024)
        if mb > 0:
            console.print(f"[green]✓[/green] Model ready ({mb:.1f} MB in {elapsed:.0f}s)")
            return

    console.print("[green]✓[/green] Model ready")


def _save_outputs(
    summary: Summary,
    transcript: Transcript,
    input_path: str,
    output: Path | None,
    settings: Settings,
    save_transcript: bool,
) -> None:
    """Save summary and transcript outputs to files.

    Args:
        summary: Summary result to save
        transcript: Transcript result to save
        input_path: Original input path for deriving output filenames
        output: Optional user-specified output path
        settings: Application settings
        save_transcript: Whether to save transcript
    """
    base_name = Path(input_path).stem

    if output or settings.output.save_summary:
        _save_summary(summary, output, settings.output, base_name)

    if save_transcript or settings.output.save_transcript:
        _save_transcript(transcript, settings.output, base_name)


def _save_summary(
    summary: Summary, output: Path | None, output_config: OutputConfig, base_name: str
) -> None:
    """Save summary to file.

    Args:
        summary: Summary result to save
        output: Optional user-specified output path
        output_config: Output configuration settings
        base_name: Base name for the output file
    """
    output_path = Path(output or output_config.output_dir / f"{base_name}_summary.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(summary.text, encoding="utf-8")
    console.print(f"[green]✓[/green] Saved to: {output_path}")


def _save_transcript(transcript: Transcript, output_config: OutputConfig, base_name: str) -> None:
    """Save transcript to file.

    Args:
        transcript: Transcript result to save
        output_config: Output configuration settings
        base_name: Base name for the output file
    """
    response_format = transcript.response_format or "txt"
    extension = _get_transcript_extension(response_format)
    transcript_path = output_config.output_dir / f"{base_name}_transcript.{extension}"
    transcript_path.parent.mkdir(parents=True, exist_ok=True)

    _write_transcript_file(transcript_path, transcript, response_format)
    console.print(f"[green]✓[/green] Transcript saved to: {transcript_path}")


def _get_transcript_extension(response_format: str) -> str:
    """Map response format to file extension.

    Args:
        response_format: API response format

    Returns:
        File extension for the format
    """
    extension_map = {
        "verbose_json": "json",
        "json": "json",
        "text": "txt",
        "srt": "srt",
        "vtt": "vtt",
    }
    return extension_map.get(response_format, "txt")


def _write_transcript_file(
    transcript_path: Path, transcript: Transcript, response_format: str
) -> None:
    """Write transcript content to file based on format.

    Args:
        transcript_path: Path to write the transcript
        transcript: Transcript data
        response_format: Format type (verbose_json, json, text, srt, vtt)
    """
    if response_format in ("verbose_json", "json"):
        import json

        with open(transcript_path, "w", encoding="utf-8") as f:
            json.dump(transcript.raw_response, f, indent=2, ensure_ascii=False)
    else:
        transcript_path.write_text(str(transcript.raw_response), encoding="utf-8")


@click.group()
@click.version_option()
@click.option("--config", type=click.Path(exists=True), help="Path to config file")
@click.option("--verbose", is_flag=True, help="Enable verbose logging")
@click.option("--gpu", is_flag=True, help="Use GPU container (CUDA)")
@click.pass_context
def cli(ctx: click.Context, config: Path | None, verbose: bool, gpu: bool) -> None:
    """Vidscribe - Automatically summarize video content."""
    # Initialize settings
    settings = Settings(config_file=config)

    if gpu:
        settings.transcriber.use_gpu = True
        _check_gpu_if_requested(use_gpu=True)

    # Setup logging
    log_level = "DEBUG" if verbose else settings.logging.log_level
    setup_logging(level=log_level, log_file=settings.logging.log_file)

    # Store settings in context
    ctx.ensure_object(dict)
    ctx.obj["settings"] = settings


@cli.command()
@click.argument("input", type=click.STRING)
@click.option("--output", "-o", type=click.Path(), help="Output file path")
@click.option(
    "--summary-style",
    type=click.Choice(["brief", "detailed", "bullet-points", "concise"]),
    help="Summary style",
)
@click.option("--model", help="LLM model to use")
@click.option("--save-transcript", is_flag=True, help="Save raw transcript")
@click.pass_context
def summarize(
    ctx: click.Context,
    input: str,
    output: Path | None,
    summary_style: str | None,
    model: str | None,
    save_transcript: bool,
) -> None:
    """Summarize a video file or URL."""
    settings = ctx.obj["settings"]

    try:
        audio_path = _get_audio(input, settings)

        container_mgr = _ensure_container_running(settings)
        result = _download_model_with_progress(container_mgr, settings.transcriber.model)
        _print_download_result(result)

        transcript = _transcribe_audio(audio_path, settings)
        summary = _generate_summary(transcript, summary_style, model, settings)

        console.print("[green]✓[/green] Summary complete!")
        console.print()
        console.print("[bold]Summary:[/bold]")
        console.print(summary.text)

        _save_outputs(summary, transcript, input, output, settings, save_transcript)

    except VideoSummarizerError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort() from e


def _get_audio(input: str, settings: Settings) -> Path:
    """Get audio from URL or local file."""
    validator = VideoURLValidator()

    if validator.is_valid_url(input):
        return _download_audio(input, settings)

    return _extract_audio(input)


def _download_audio(url: str, settings: Settings) -> Path:
    """Download audio from URL."""
    console.print(f"[cyan]Downloading audio from: {url}[/cyan]")
    downloader = YtDlpDownloader(
        temp_dir=settings.scraper.temp_dir,
        ffmpeg_location=_get_ffmpeg_location(settings),
    )

    with console.status("[bold green]Downloading audio..."):
        audio_path = downloader.download_audio(
            url,
            settings.scraper.temp_dir,
            settings.scraper.audio_quality.value,
        )
    console.print(f"[green]✓[/green] Downloaded to: {audio_path}")
    return audio_path


def _extract_audio(input_path: str) -> Path:
    """Extract audio from local file."""
    video_path = Path(input_path)
    if not video_path.exists():
        console.print(f"[red]Error: File not found: {input_path}[/red]")
        raise click.Abort()

    console.print(f"[cyan]Extracting audio from: {input_path}[/cyan]")
    extractor = MoviePyAudioExtractor()

    with console.status("[bold green]Extracting audio..."):
        audio_path = extractor.extract_audio(video_path)
    console.print(f"[green]✓[/green] Extracted to: {audio_path}")
    return audio_path


def _transcribe_audio(audio_path: Path, settings: Settings) -> Transcript:
    """Transcribe audio file."""
    console.print("[cyan]Transcribing audio...[/cyan]")
    transcriber = SpeachesTranscriber(
        api_base=f"http://localhost:{settings.transcriber.container_port}/v1",
        model=settings.transcriber.model,
        chunk_duration_sec=settings.transcriber.chunk_duration_sec,
        chunk_overlap_sec=settings.transcriber.chunk_overlap_sec,
        chunk_duration_threshold=settings.transcriber.chunk_duration_threshold,
        response_format=settings.transcriber.response_format,
        vad_filter=settings.transcriber.vad_filter,
        language=settings.transcriber.language,
    )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("[bold green]Transcribing...", total=None)
        transcript = transcriber.transcribe(audio_path)

    console.print(f"[green]✓[/green] Transcription complete ({len(transcript.text)} characters)")
    return transcript


def _generate_summary(
    transcript: Transcript,
    summary_style: str | None,
    model: str | None,
    settings: Settings,
) -> Summary:
    """Generate summary from transcript."""
    console.print("[cyan]Generating summary...[/cyan]")

    preprocessor = TranscriptPreprocessor()
    clean_text = preprocessor.clean(transcript)

    summarizer = OpenAISummarizer(
        api_key=settings.summarizer.api_key,
        base_url=settings.summarizer.api_base,
        model=model or settings.summarizer.model,
        max_tokens=settings.summarizer.max_tokens,
        temperature=settings.summarizer.temperature,
    )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("[bold green]Summarizing...", total=None)
        summary = summarizer.summarize(
            Transcript(text=clean_text, duration=transcript.duration),
            style=summary_style or settings.summarizer.summary_style.value,
        )

    return summary


@cli.command()
@click.option("--gpu", is_flag=True, help="Use GPU container")
@click.pass_context
def container_start(ctx: click.Context, gpu: bool) -> None:
    """Start the Speaches container."""
    settings = ctx.obj["settings"]
    if gpu:
        settings.transcriber.use_gpu = True
        _check_gpu_if_requested(use_gpu=True)

    container_mgr = SpeachesContainerManager(
        container_name=settings.transcriber.container_name,
        container_port=settings.transcriber.container_port,
        container_image=settings.transcriber.get_container_image(),
        use_gpu=settings.transcriber.use_gpu,
    )

    gpu_msg = " (GPU)" if settings.transcriber.use_gpu else " (CPU)"
    console.print(f"[cyan]Starting Speaches container{gpu_msg}...[/cyan]")
    container_mgr.start()
    console.print("[green]✓[/green] Container started")


@cli.command()
@click.pass_context
def container_stop(ctx: click.Context) -> None:
    """Stop the Speaches container."""
    settings = ctx.obj["settings"]
    container_mgr = SpeachesContainerManager(
        container_name=settings.transcriber.container_name,
    )

    console.print("[cyan]Stopping Speaches container...[/cyan]")
    container_mgr.stop()
    console.print("[green]✓[/green] Container stopped")


@cli.command()
@click.pass_context
def container_status(ctx: click.Context) -> None:
    """Check Speaches container status."""
    settings = ctx.obj["settings"]
    container_mgr = SpeachesContainerManager(
        container_name=settings.transcriber.container_name,
    )

    status = container_mgr.get_status()

    console.print("[bold]Container Status:[/bold]")
    console.print(f"  Name: {status['name']}")
    console.print(f"  Status: {status['status']}")
    console.print(f"  Image: {status['image']}")
    console.print(f"  Port: {status['port']}")


@cli.command()
@click.option("--gpu", is_flag=True, help="Use GPU container")
@click.pass_context
def list_models(ctx: click.Context, gpu: bool) -> None:
    """List all available Whisper models from Speaches API."""
    import httpx

    settings = ctx.obj["settings"]

    if gpu:
        settings.transcriber.use_gpu = True
        _check_gpu_if_requested(use_gpu=True)

    _ensure_container_running(settings)

    api_base = f"http://localhost:{settings.transcriber.container_port}/v1"

    try:
        downloaded_models = _fetch_downloaded_models(api_base)
        _display_downloaded_models(downloaded_models)
        _display_available_models()
        _display_model_usage_notes()
    except httpx.HTTPStatusError as e:
        _handle_http_status_error(e, api_base)
    except httpx.RequestError as e:
        _handle_request_error(e, api_base)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        raise click.Abort() from e


def _fetch_downloaded_models(api_base: str) -> list[dict[str, object]]:
    """Fetch downloaded models from Speaches API.

    Args:
        api_base: Base URL for the API

    Returns:
        List of model dictionaries
    """
    import httpx

    url = f"{api_base}/models"

    with console.status("[bold green]Fetching downloaded models..."):
        response = httpx.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

    console.print("[green]✓[/green] Models retrieved\n")
    result = data.get("data", [])
    if isinstance(result, list):
        return result
    return []


def _display_downloaded_models(models: list[dict]) -> None:
    """Display downloaded models.

    Args:
        models: List of model dictionaries from the API
    """
    if not models:
        console.print("[yellow]No models currently downloaded[/yellow]\n")
        return

    console.print("[bold]Downloaded Models (ready to use):[/bold]\n")

    for model in models:
        model_id = model.get("id", "unknown")
        model_info = _format_model_info(model)
        console.print(f"  • [green bold]{model_id}[/green bold]{model_info}")

    console.print(f"\n[dim]Total: {len(models)} model(s) downloaded[/dim]\n")


def _format_model_info(model: dict) -> str:
    """Format model metadata for display.

    Args:
        model: Model dictionary

    Returns:
        Formatted info string
    """
    info_parts = []

    if "object" in model:
        info_parts.append(f"type: {model['object']}")
    if "created" in model:
        info_parts.append(f"created: {model['created']}")

    return f" [dim]({', '.join(info_parts)})[/dim]" if info_parts else ""


def _display_available_models() -> None:
    """Display all available Whisper models organized by category."""
    console.print("[bold]Available Models (can be downloaded):[/bold]\n")

    _print_model_list("OpenAI Whisper Models:", _OPENAI_MODELS)
    console.print()
    _print_model_list(
        "Systran Faster-Whisper Models (distilled, faster inference):",
        _SYSTRAN_FASTER_MODELS,
    )
    console.print()
    _print_model_list(
        "Systran Distil-Whisper Models (smaller, fastest inference):",
        _SYSTRAN_DISTIL_MODELS,
    )


def _print_model_list(header: str, models: list[str]) -> None:
    """Print a category of models.

    Args:
        header: Section header text
        models: List of model IDs
    """
    console.print(f"[dim]{header}[/dim]")
    for model in models:
        console.print(f"  • {model}")


def _display_model_usage_notes() -> None:
    """Display usage notes for models."""
    console.print(
        "\n[dim]Note: Models ending with '.en' are English-only. Others are multilingual.[/dim]"
    )
    console.print(
        "[dim]To use a different model, set WHISPER_MODEL in .env or use --model option.[/dim]"
    )


def _handle_http_status_error(error: httpx.HTTPStatusError, api_base: str) -> None:
    """Handle HTTP status errors from API calls.

    Args:
        error: The HTTP error exception
        api_base: API base URL for error message
    """
    console.print(f"[red]Error fetching models: {error.response.status_code}[/red]")
    if error.response.status_code == 404:
        console.print(
            "[dim]The /v1/models endpoint may not be available on this Speaches version[/dim]"
        )
    raise click.Abort() from error


def _handle_request_error(error: httpx.RequestError, api_base: str) -> None:
    """Handle request errors from API calls.

    Args:
        error: The request error exception
        api_base: API base URL for error message
    """
    console.print(f"[red]Error connecting to Speaches API: {error}[/red]")
    console.print(f"[dim]Make sure the container is running at {api_base}[/dim]")
    raise click.Abort() from error


# Available model lists
_OPENAI_MODELS = [
    "openai/whisper-tiny",
    "openai/whisper-base",
    "openai/whisper-small",
    "openai/whisper-medium",
    "openai/whisper-large",
    "openai/whisper-large-v2",
    "openai/whisper-large-v3",
    "openai/whisper-large-v3-turbo",
]

_SYSTRAN_FASTER_MODELS = [
    "Systran/faster-whisper-tiny",
    "Systran/faster-whisper-tiny.en",
    "Systran/faster-whisper-base",
    "Systran/faster-whisper-base.en",
    "Systran/faster-whisper-small",
    "Systran/faster-whisper-small.en",
    "Systran/faster-whisper-medium",
    "Systran/faster-whisper-medium.en",
    "Systran/faster-whisper-large-v1",
    "Systran/faster-whisper-large-v2",
    "Systran/faster-whisper-large-v3",
]

_SYSTRAN_DISTIL_MODELS = [
    "Systran/distil-whisper-tiny",
    "Systran/distil-whisper-tiny.en",
    "Systran/distil-whisper-base",
    "Systran/distil-whisper-base.en",
    "Systran/distil-whisper-small",
    "Systran/distil-whisper-small.en",
    "Systran/distil-whisper-medium",
    "Systran/distil-whisper-medium.en",
]


@cli.command()
@click.pass_context
def getenv(ctx: click.Context) -> None:
    """Create .env file from .env.example template.

    If .env already exists in the current directory, prompts for overwrite.
    """
    from importlib import resources

    # Define paths - .env goes in current working directory
    env_path = Path.cwd() / ".env"

    # Check if .env already exists
    if env_path.exists():
        console.print(f"[yellow].env file already exists at:[/yellow] {env_path}")
        overwrite = click.confirm(
            "Do you want to overwrite it?",
            default=False,
            show_default=True,
        )

        if not overwrite:
            console.print("[dim]Operation cancelled.[/dim]")
            return

    # Read .env.example from package resources
    console.print("[cyan]Reading .env.example template from package...[/cyan]")

    try:
        # Use importlib.resources to read from installed package
        # This works both in development and in installed wheel
        with resources.files("video_summarizer.resources").joinpath(".env.example").open("r") as f:
            env_content = f.read()
    except (FileNotFoundError, AttributeError) as e:
        console.print("[red]Error: Could not find .env.example template in package[/red]")
        console.print(f"[dim]Debug info: {e}[/dim]")
        raise click.ClickException(".env.example template not found in package") from e

    # Write to .env file
    console.print(f"[cyan]Creating .env file at:[/cyan] {env_path}")
    env_path.write_text(env_content, encoding="utf-8")

    console.print("[green]✓[/green] .env file created successfully!")
    console.print()
    console.print("[bold yellow]Next steps:[/bold yellow]")
    console.print("1. Edit .env and configure your API keys and settings")
    console.print("2. Set OPENAI_API_KEY to your actual API key")
    console.print("3. Adjust other settings as needed")
    console.print()
    console.print("[dim]See .env file comments for detailed configuration options.[/dim]")

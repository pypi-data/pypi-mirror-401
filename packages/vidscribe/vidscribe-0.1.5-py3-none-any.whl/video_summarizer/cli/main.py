"""Main CLI application for video summarizer."""

from pathlib import Path

import rich_click as click
from rich.console import Console
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.style import Style
from rich.text import Text

from video_summarizer.config.settings import Settings
from video_summarizer.scraper.downloader import YtDlpDownloader
from video_summarizer.scraper.validator import VideoURLValidator
from video_summarizer.summarizer.preprocessor import TranscriptPreprocessor
from video_summarizer.summarizer.summarizer import OpenAISummarizer
from video_summarizer.transcriber.container import SpeachesContainerManager
from video_summarizer.transcriber.extractor import MoviePyAudioExtractor
from video_summarizer.transcriber.transcriber import SpeachesTranscriber
from video_summarizer.utils.errors import VideoSummarizerError
from video_summarizer.utils.gpu_checker import check_gpu_availability, get_gpu_info
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
        raise click.ClickException("GPU support requested but not available")

    # GPU is available - show info
    gpu_info = get_gpu_info()
    if "gpus" in gpu_info:
        gpus = gpu_info["gpus"]
        if isinstance(gpus, list):
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
    """Print the result of a model download operation."""
    if result.get("status") == "complete":
        elapsed = result.get("elapsed_seconds", 0)
        mb = result.get("bytes_downloaded", 0) / (1024 * 1024)
        if mb > 0:
            console.print(f"[green]✓[/green] Model ready ({mb:.1f} MB in {elapsed:.0f}s)")
        else:
            console.print("[green]✓[/green] Model ready")
    else:
        console.print("[green]✓[/green] Model ready")


def _save_outputs(
    summary: Summary,
    transcript: Transcript,
    input_path: str,
    output: Path | None,
    settings: Settings,
    save_transcript: bool,
) -> None:
    """Save summary and transcript outputs to files."""
    base_name = Path(input_path).stem

    if output or settings.output.save_summary:
        output_path = Path(output or settings.output.output_dir / f"{base_name}_summary.md")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(summary.text, encoding="utf-8")
        console.print(f"[green]✓[/green] Saved to: {output_path}")

    if save_transcript or settings.output.save_transcript:
        # Determine file extension and content based on response format
        response_format = transcript.response_format or "txt"  # Default to txt for chunked

        # Map response format to file extension
        extension_map = {
            "verbose_json": "json",
            "json": "json",
            "text": "txt",
            "srt": "srt",
            "vtt": "vtt",
        }

        extension = extension_map.get(response_format, "txt")
        transcript_path = settings.output.output_dir / f"{base_name}_transcript.{extension}"
        transcript_path.parent.mkdir(parents=True, exist_ok=True)

        # Save based on format
        if response_format in ["verbose_json", "json"]:
            # Save as JSON with proper formatting
            import json

            with open(transcript_path, "w", encoding="utf-8") as f:
                json.dump(transcript.raw_response, f, indent=2, ensure_ascii=False)
        else:
            # Save as plain text (txt, srt, vtt)
            transcript_path.write_text(str(transcript.raw_response), encoding="utf-8")

        console.print(f"[green]✓[/green] Transcript saved to: {transcript_path}")


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

    # Ensure container is running
    console.print("[cyan]Ensuring Speaches container is running...[/cyan]")
    container_mgr = SpeachesContainerManager(
        container_name=settings.transcriber.container_name,
        container_port=settings.transcriber.container_port,
        container_image=settings.transcriber.get_container_image(),
        use_gpu=settings.transcriber.use_gpu,
    )

    if not container_mgr.is_running():
        with console.status("[bold green]Starting Speaches container..."):
            container_mgr.start()
        console.print("[green]✓[/green] Container started")

    # Query the models endpoint
    api_base = f"http://localhost:{settings.transcriber.container_port}/v1"
    url = f"{api_base}/models"

    try:
        with console.status("[bold green]Fetching downloaded models..."):
            response = httpx.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

        console.print("[green]✓[/green] Models retrieved\n")

        # Display currently downloaded models
        if "data" in data and len(data["data"]) > 0:
            console.print("[bold]Downloaded Models (ready to use):[/bold]\n")

            for model in data["data"]:
                model_id = model.get("id", "unknown")
                model_info = []

                if "object" in model:
                    model_info.append(f"type: {model['object']}")
                if "created" in model:
                    model_info.append(f"created: {model['created']}")

                info_str = f" [dim]({', '.join(model_info)})[/dim]" if model_info else ""
                console.print(f"  • [green bold]{model_id}[/green bold]{info_str}")

            console.print(f"\n[dim]Total: {len(data['data'])} model(s) downloaded[/dim]\n")
        else:
            console.print("[yellow]No models currently downloaded[/yellow]\n")

        # Display all available models that can be downloaded
        console.print("[bold]Available Models (can be downloaded):[/bold]\n")

        # Standard OpenAI Whisper models
        console.print("[dim]OpenAI Whisper Models:[/dim]")
        openai_models = [
            "openai/whisper-tiny",
            "openai/whisper-base",
            "openai/whisper-small",
            "openai/whisper-medium",
            "openai/whisper-large",
            "openai/whisper-large-v2",
            "openai/whisper-large-v3",
            "openai/whisper-large-v3-turbo",
        ]
        for model in openai_models:
            console.print(f"  • {model}")

        # Systran faster-whisper models (distilled, faster inference)
        console.print("\n[dim]Systran Faster-Whisper Models (distilled, faster inference):[/dim]")
        systran_models = [
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
        for model in systran_models:
            console.print(f"  • {model}")

        # Systran distil-whisper models (even smaller, faster)
        console.print("\n[dim]Systran Distil-Whisper Models (smaller, fastest inference):[/dim]")
        distil_models = [
            "Systran/distil-whisper-tiny",
            "Systran/distil-whisper-tiny.en",
            "Systran/distil-whisper-base",
            "Systran/distil-whisper-base.en",
            "Systran/distil-whisper-small",
            "Systran/distil-whisper-small.en",
            "Systran/distil-whisper-medium",
            "Systran/distil-whisper-medium.en",
        ]
        for model in distil_models:
            console.print(f"  • {model}")

        console.print(
            "\n[dim]Note: Models ending with '.en' are English-only. Others are multilingual.[/dim]"
        )
        console.print(
            "[dim]To use a different model, set WHISPER_MODEL in .env or use --model option.[/dim]"
        )

    except httpx.HTTPStatusError as e:
        console.print(f"[red]Error fetching models: {e.response.status_code}[/red]")
        if e.response.status_code == 404:
            console.print(
                "[dim]The /v1/models endpoint may not be available on this Speaches version[/dim]"
            )
        raise click.Abort() from e
    except httpx.RequestError as e:
        console.print(f"[red]Error connecting to Speaches API: {e}[/red]")
        console.print(f"[dim]Make sure the container is running at {api_base}[/dim]")
        raise click.Abort() from e
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        raise click.Abort() from e

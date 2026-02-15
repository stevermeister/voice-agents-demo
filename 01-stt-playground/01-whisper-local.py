"""Local Speech-to-Text with OpenAI Whisper.

Records from your microphone and transcribes using Whisper (runs entirely on your machine).
No API key needed – everything runs locally.

Available models (smallest → largest):
  tiny, base, small, medium, large-v3, turbo

Usage::

    uv run 01-stt-playground/01-whisper-local.py              # default: turbo
    uv run 01-stt-playground/01-whisper-local.py --model base  # pick a model
    uv run 01-stt-playground/01-whisper-local.py --duration 10 # record longer
"""

import argparse

import numpy as np
import sounddevice as sd
import whisper
from rich.console import Console

console = Console()

SAMPLE_RATE = 16_000


def record_audio(duration: int = 5) -> np.ndarray:
    console.print(f"[bold green]🎤 Recording for {duration}s …[/]")
    audio = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="float32")
    sd.wait()
    console.print("[bold green]✅ Recording complete[/]")
    return audio.flatten()


def transcribe(audio: np.ndarray, model_name: str = "turbo") -> str:
    console.print(f"[yellow]Loading Whisper model '{model_name}' …[/]")
    model = whisper.load_model(model_name)
    result = model.transcribe(audio, fp16=False)
    return result["text"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Local STT with OpenAI Whisper")
    parser.add_argument("--model", default="turbo", choices=whisper.available_models(), help="Whisper model to use (default: turbo)")
    parser.add_argument("--duration", type=int, default=5, help="Recording duration in seconds (default: 5)")
    args = parser.parse_args()

    audio = record_audio(args.duration)
    text = transcribe(audio, args.model)
    console.print(f"\n[bold cyan]Transcript:[/] {text}")

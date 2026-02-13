"""Local Speech-to-Text with OpenAI Whisper.

Records from your microphone and transcribes using Whisper (runs entirely on your machine).
"""

import whisper
import numpy as np
import sounddevice as sd
from rich.console import Console

console = Console()

SAMPLE_RATE = 16_000
DURATION_SEC = 5


def record_audio(duration: int = DURATION_SEC) -> np.ndarray:
    console.print(f"[bold green]🎤 Recording for {duration}s …[/]")
    audio = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="float32")
    sd.wait()
    console.print("[bold green]✅ Recording complete[/]")
    return audio.flatten()


def transcribe(audio: np.ndarray, model_name: str = "base") -> str:
    console.print(f"[yellow]Loading Whisper model '{model_name}' …[/]")
    model = whisper.load_model(model_name)
    result = model.transcribe(audio, fp16=False)
    return result["text"]


if __name__ == "__main__":
    audio = record_audio()
    text = transcribe(audio)
    console.print(f"\n[bold cyan]Transcript:[/] {text}")

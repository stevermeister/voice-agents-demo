"""Compare STT providers: accuracy, latency & cost.

Sends the same audio clip to multiple providers and prints a comparison table.
"""

import time
import os

from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv()
console = Console()

AUDIO_FILE = "sample.wav"  # place a test WAV file here


def transcribe_whisper_local(path: str) -> tuple[str, float]:
    import whisper

    model = whisper.load_model("base")
    start = time.perf_counter()
    result = model.transcribe(path, fp16=False)
    elapsed = time.perf_counter() - start
    return result["text"].strip(), elapsed


def transcribe_deepgram(path: str) -> tuple[str, float]:
    from deepgram import DeepgramClient, PrerecordedOptions

    client = DeepgramClient(os.getenv("DEEPGRAM_API_KEY"))
    with open(path, "rb") as f:
        payload = {"buffer": f.read(), "mimetype": "audio/wav"}
    start = time.perf_counter()
    response = client.listen.rest.v("1").transcribe_file(payload, PrerecordedOptions(model="nova-2"))
    elapsed = time.perf_counter() - start
    transcript = response.results.channels[0].alternatives[0].transcript
    return transcript, elapsed


def main():
    if not os.path.exists(AUDIO_FILE):
        console.print(f"[red]Place a '{AUDIO_FILE}' in this directory first.[/]")
        return

    table = Table(title="STT Provider Comparison")
    table.add_column("Provider")
    table.add_column("Latency (s)", justify="right")
    table.add_column("Transcript")

    providers = [
        ("Whisper (local)", transcribe_whisper_local),
        ("Deepgram Nova-2", transcribe_deepgram),
    ]

    for name, fn in providers:
        try:
            text, latency = fn(AUDIO_FILE)
            table.add_row(name, f"{latency:.2f}", text[:80])
        except Exception as e:
            table.add_row(name, "—", f"[red]{e}[/]")

    console.print(table)


if __name__ == "__main__":
    main()

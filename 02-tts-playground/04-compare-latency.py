"""Compare TTS provider latency: time-to-first-byte.

Measures how quickly each provider starts streaming audio back.
"""

import os
import time

from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv()
console = Console()

TEXT = "The quick brown fox jumps over the lazy dog."


def measure_cartesia() -> float:
    from cartesia import Cartesia

    client = Cartesia(api_key=os.getenv("CARTESIA_API_KEY"))
    start = time.perf_counter()
    client.tts.bytes(
        model_id="sonic-english",
        transcript=TEXT,
        voice_id="a0e99841-438c-4a64-b679-ae501e7d6091",
        output_format={"container": "wav", "sample_rate": 44100, "encoding": "pcm_f32le"},
    )
    return time.perf_counter() - start


def measure_elevenlabs() -> float:
    from elevenlabs import ElevenLabs

    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    start = time.perf_counter()
    gen = client.text_to_speech.convert(
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        text=TEXT,
        model_id="eleven_turbo_v2",
    )
    next(iter(gen))  # time to first chunk
    return time.perf_counter() - start


def main():
    table = Table(title="TTS Latency Comparison")
    table.add_column("Provider")
    table.add_column("Time-to-first-byte (s)", justify="right")

    providers = [
        ("Cartesia Sonic", measure_cartesia),
        ("ElevenLabs Turbo v2", measure_elevenlabs),
    ]

    for name, fn in providers:
        try:
            latency = fn()
            table.add_row(name, f"{latency:.3f}")
        except Exception as e:
            table.add_row(name, f"[red]{e}[/]")

    console.print(table)


if __name__ == "__main__":
    main()

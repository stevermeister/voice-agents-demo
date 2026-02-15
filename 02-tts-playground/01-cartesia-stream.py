"""Stream TTS audio from Cartesia's Sonic 3 model.

Streams audio chunks from Cartesia and plays them back locally.
Requires CARTESIA_API_KEY in .env.

Usage::

    uv run 02-tts-playground/01-cartesia-stream.py
"""

import asyncio
import os
import subprocess
import sys

from cartesia import AsyncCartesia
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()

OUTPUT_FILE = "cartesia_output.wav"


async def main():
    api_key = os.getenv("CARTESIA_API_KEY")
    if not api_key:
        console.print("[red]Set CARTESIA_API_KEY in .env[/]")
        return

    client = AsyncCartesia(api_key=api_key)

    text = "Hello! I'm a voice agent built with Cartesia Sonic 3. How can I help you today?"
    voice_id = "a0e99841-438c-4a64-b679-ae501e7d6091"  # Barbershop Man

    console.print(f"[bold green]🔊 Streaming:[/] {text}")

    with open(OUTPUT_FILE, "wb") as f:
        bytes_iter = client.tts.bytes(
            model_id="sonic-3",
            transcript=text,
            voice={
                "mode": "id",
                "id": voice_id,
            },
            language="en",
            output_format={
                "container": "wav",
                "sample_rate": 44100,
                "encoding": "pcm_s16le",
            },
        )
        async for chunk in bytes_iter:
            f.write(chunk)

    console.print(f"[bold green]✅ Saved to {OUTPUT_FILE}[/]")

    # Play the audio
    if sys.platform == "darwin":
        subprocess.run(["afplay", OUTPUT_FILE])
    else:
        subprocess.run(["ffplay", "-autoexit", "-nodisp", OUTPUT_FILE])


if __name__ == "__main__":
    asyncio.run(main())

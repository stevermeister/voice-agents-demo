"""Stream TTS audio from Cartesia's Sonic model.

Requires CARTESIA_API_KEY in .env.
"""

import os

from cartesia import Cartesia
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()


def main():
    api_key = os.getenv("CARTESIA_API_KEY")
    if not api_key:
        console.print("[red]Set CARTESIA_API_KEY in .env[/]")
        return

    client = Cartesia(api_key=api_key)

    text = "Hello! I'm a voice agent built with Cartesia. How can I help you today?"
    voice_id = "a0e99841-438c-4a64-b679-ae501e7d6091"  # Barbershop Man

    console.print(f"[bold green]🔊 Streaming: [/]{text}")

    output = client.tts.bytes(
        model_id="sonic-english",
        transcript=text,
        voice_id=voice_id,
        output_format={"container": "wav", "sample_rate": 44100, "encoding": "pcm_f32le"},
    )

    # Save to file for playback
    with open("cartesia_output.wav", "wb") as f:
        f.write(output)

    console.print("[bold green]✅ Saved to cartesia_output.wav[/]")


if __name__ == "__main__":
    main()

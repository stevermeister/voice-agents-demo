"""Stream TTS audio from ElevenLabs.

Streams audio chunks from ElevenLabs and plays them back locally.
Requires ELEVENLABS_API_KEY in .env.

Usage::

    uv run 02-tts-playground/02-elevenlabs-stream.py
"""

import os
import subprocess
import sys

from elevenlabs import ElevenLabs
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()

OUTPUT_FILE = "elevenlabs_output.mp3"


def main():
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        console.print("[red]Set ELEVENLABS_API_KEY in .env[/]")
        return

    client = ElevenLabs(api_key=api_key)

    text = "Hello! I'm a voice agent built with ElevenLabs. How can I help you today?"

    console.print(f"[bold green]🔊 Streaming:[/] {text}")

    try:
        audio_generator = client.text_to_speech.convert(
            voice_id="JBFqnCBsd6RMkjVDRZzb",  # George
            text=text,
            model_id="eleven_flash_v2_5",
            output_format="mp3_44100_128",
        )

        # Collect streamed chunks and save
        with open(OUTPUT_FILE, "wb") as f:
            for chunk in audio_generator:
                f.write(chunk)
    except Exception as e:
        if "quota_exceeded" in str(e):
            console.print("[red]ElevenLabs quota exceeded – top up credits or shorten the text.[/]")
        else:
            console.print(f"[red]ElevenLabs error:[/] {e}")
        return

    console.print(f"[bold green]✅ Saved to {OUTPUT_FILE}[/]")

    # Play the audio
    if sys.platform == "darwin":
        subprocess.run(["afplay", OUTPUT_FILE])
    else:
        subprocess.run(["ffplay", "-autoexit", "-nodisp", OUTPUT_FILE])


if __name__ == "__main__":
    main()

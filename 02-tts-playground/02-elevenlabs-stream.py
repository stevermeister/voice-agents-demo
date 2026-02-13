"""Stream TTS audio from ElevenLabs.

Requires ELEVENLABS_API_KEY in .env.
"""

import os

from elevenlabs import ElevenLabs
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()


def main():
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        console.print("[red]Set ELEVENLABS_API_KEY in .env[/]")
        return

    client = ElevenLabs(api_key=api_key)

    text = "Hello! I'm a voice agent built with ElevenLabs. How can I help you today?"

    console.print(f"[bold green]🔊 Streaming: [/]{text}")

    audio_generator = client.text_to_speech.convert(
        voice_id="JBFqnCBsd6RMkjVDRZzb",  # George
        text=text,
        model_id="eleven_turbo_v2",
    )

    # Collect streamed chunks and save
    with open("elevenlabs_output.mp3", "wb") as f:
        for chunk in audio_generator:
            f.write(chunk)

    console.print("[bold green]✅ Saved to elevenlabs_output.mp3[/]")


if __name__ == "__main__":
    main()

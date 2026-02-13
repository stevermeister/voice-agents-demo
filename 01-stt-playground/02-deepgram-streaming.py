"""Real-time streaming STT with Deepgram.

Streams microphone audio to Deepgram and prints interim + final transcripts.
Requires DEEPGRAM_API_KEY in .env.
"""

import asyncio
import os

from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()


async def main():
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        console.print("[red]Set DEEPGRAM_API_KEY in .env[/]")
        return

    deepgram = DeepgramClient(api_key)
    connection = deepgram.listen.asynclive.v("1")

    async def on_message(self, result, **kwargs):
        transcript = result.channel.alternatives[0].transcript
        if transcript:
            if result.is_final:
                console.print(f"[bold cyan]Final:[/] {transcript}")
            else:
                console.print(f"[dim]Interim:[/] {transcript}", end="\r")

    connection.on(LiveTranscriptionEvents.Transcript, on_message)

    options = LiveOptions(model="nova-2", language="en", smart_format=True)
    await connection.start(options)

    console.print("[bold green]🎤 Listening … (Ctrl+C to stop)[/]")

    # TODO: pipe microphone audio into connection.send()
    # For demo purposes, keep connection alive
    try:
        while True:
            await asyncio.sleep(0.1)
    except KeyboardInterrupt:
        pass

    await connection.finish()
    console.print("[bold green]Done.[/]")


if __name__ == "__main__":
    asyncio.run(main())

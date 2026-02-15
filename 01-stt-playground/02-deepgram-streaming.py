"""Real-time streaming STT with Deepgram.

Streams microphone audio to Deepgram and prints interim + final transcripts.
Requires DEEPGRAM_API_KEY in .env.
"""

import asyncio
import os

import sounddevice as sd
from deepgram import AsyncDeepgramClient
from deepgram.core.events import EventType
from deepgram.extensions.types.sockets import (
    ListenV1MediaMessage,
    ListenV1SocketClientResponse,
)
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()

SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_MS = 100  # send audio every 100ms


async def main():
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        console.print("[red]Set DEEPGRAM_API_KEY in .env[/]")
        return

    client = AsyncDeepgramClient(api_key=api_key)

    async with client.listen.v1.connect(
        model="nova-3",
        language="en",
        smart_format="true",
        interim_results="true",
        encoding="linear16",
        sample_rate=str(SAMPLE_RATE),
        channels=str(CHANNELS),
    ) as connection:

        def on_message(message: ListenV1SocketClientResponse) -> None:
            # Each message may contain multiple result types; look for transcripts
            channel = getattr(message, "channel", None)
            if channel is None:
                return
            transcript = channel.alternatives[0].transcript
            if not transcript:
                return
            is_final = getattr(message, "is_final", False)
            if is_final:
                console.print(f"[bold cyan]Final:[/] {transcript}")
            else:
                console.print(f"[dim]Interim:[/] {transcript}", end="\r")

        connection.on(EventType.OPEN, lambda _: None)
        connection.on(EventType.MESSAGE, on_message)
        connection.on(
            EventType.ERROR, lambda err: console.print(f"[red]Error:[/] {err}")
        )
        connection.on(EventType.CLOSE, lambda _: None)

        await connection.start_listening()
        console.print("[bold green]🎤 Listening … (Ctrl+C to stop)[/]")

        # Stream microphone audio to Deepgram
        audio_queue: asyncio.Queue[bytes] = asyncio.Queue()
        chunk_samples = int(SAMPLE_RATE * CHUNK_MS / 1000)

        def _audio_callback(indata, frames, time_info, status):
            if status:
                console.print(f"[yellow]Audio warning:[/] {status}")
            audio_queue.put_nowait(indata.tobytes())

        stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16",
            blocksize=chunk_samples,
            callback=_audio_callback,
        )

        try:
            stream.start()
            while True:
                audio_bytes = await audio_queue.get()
                await connection.send_media(ListenV1MediaMessage(audio_bytes))
        except (KeyboardInterrupt, asyncio.CancelledError):
            pass
        finally:
            stream.stop()
            stream.close()

    console.print("[bold green]Done.[/]")


if __name__ == "__main__":
    asyncio.run(main())

"""Real-time streaming STT with Deepgram.

Streams microphone audio to Deepgram and prints interim + final transcripts.
Requires DEEPGRAM_API_KEY in .env.
"""

import asyncio
import os
import queue

import sounddevice as sd
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
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

    deepgram = DeepgramClient(api_key)
    connection = deepgram.listen.asyncwebsocket.v("1")

    async def on_message(self, result, **kwargs):
        transcript = result.channel.alternatives[0].transcript
        if transcript:
            if result.is_final:
                console.print(f"[bold cyan]Final:[/] {transcript}")
            else:
                console.print(f"[dim]Interim:[/] {transcript}", end="\r")

    async def on_error(self, error, **kwargs):
        console.print(f"[red]Error:[/] {error}")

    connection.on(LiveTranscriptionEvents.Transcript, on_message)
    connection.on(LiveTranscriptionEvents.Error, on_error)

    options = LiveOptions(
        model="nova-3",
        language="en",
        smart_format=True,
        interim_results=True,
        encoding="linear16",
        sample_rate=SAMPLE_RATE,
        channels=CHANNELS,
    )

    # Thread-safe queue for audio from the sounddevice callback thread
    audio_buf: queue.Queue[bytes] = queue.Queue()
    chunk_samples = int(SAMPLE_RATE * CHUNK_MS / 1000)

    def _audio_callback(indata, frames, time_info, status):
        if status:
            console.print(f"[yellow]Audio warning:[/] {status}")
        audio_buf.put_nowait(indata.tobytes())

    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16",
        blocksize=chunk_samples,
        callback=_audio_callback,
    )

    # Start mic first, then open WebSocket so audio is ready immediately
    stream.start()

    started = await connection.start(options)
    if not started:
        console.print("[red]Failed to connect to Deepgram[/]")
        stream.stop()
        stream.close()
        return

    console.print("[bold green]🎤 Listening … (Ctrl+C to stop)[/]")

    try:
        while True:
            # Poll the thread-safe queue from the async loop
            try:
                audio_bytes = audio_buf.get(timeout=0.05)
            except queue.Empty:
                await asyncio.sleep(0.01)
                continue
            if not await connection.send(audio_bytes):
                break
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
    finally:
        stream.stop()
        stream.close()
        await connection.finish()

    console.print("[bold green]Done.[/]")


if __name__ == "__main__":
    asyncio.run(main())

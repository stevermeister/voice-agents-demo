"""Minimal voice agent with LiveKit Agents.

A simple voice bot using LiveKit's agent framework.
Requires LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET, and OPENAI_API_KEY in .env.
"""

import asyncio
import os

from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()


async def main():
    required = ["LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET", "OPENAI_API_KEY"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        console.print(f"[red]Missing env vars: {', '.join(missing)}[/]")
        return

    console.print("[bold green]🤖 LiveKit Hello Voice Agent[/]")
    console.print("This demo creates a minimal LiveKit voice agent: STT → LLM → TTS")

    # TODO: Build LiveKit agent
    # from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli
    # from livekit.agents.voice_assistant import VoiceAssistant
    # from livekit.plugins import openai, silero
    #
    # async def entrypoint(ctx: JobContext):
    #     await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    #     assistant = VoiceAssistant(
    #         vad=silero.VAD.load(),
    #         stt=openai.STT(),
    #         llm=openai.LLM(model="gpt-4o-mini"),
    #         tts=openai.TTS(),
    #     )
    #     assistant.start(ctx.room)
    #
    # cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))

    console.print("[yellow]Agent scaffold ready – uncomment and customize above.[/]")


if __name__ == "__main__":
    asyncio.run(main())

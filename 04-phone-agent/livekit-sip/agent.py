"""LiveKit SIP phone agent.

A voice agent that handles inbound phone calls via LiveKit's SIP integration.
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

    console.print("[bold green]📞 LiveKit SIP Phone Agent[/]")
    console.print("This agent handles inbound phone calls via SIP trunk.")
    console.print("See sip-config.yaml for SIP trunk configuration.")

    # TODO: Build LiveKit SIP agent
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
    #     await assistant.say("Hello, thanks for calling! How can I help?")
    #
    # cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))

    console.print("[yellow]Agent scaffold ready – uncomment and customize above.[/]")


if __name__ == "__main__":
    asyncio.run(main())

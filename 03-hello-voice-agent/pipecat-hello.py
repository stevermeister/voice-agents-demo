"""Minimal voice agent with Pipecat.

A simple voice bot that listens, thinks (LLM), and speaks.
Requires OPENAI_API_KEY in .env.
"""

import asyncio
import os

from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()


async def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        console.print("[red]Set OPENAI_API_KEY in .env[/]")
        return

    console.print("[bold green]🤖 Pipecat Hello Voice Agent[/]")
    console.print("This demo creates a minimal voice pipeline: STT → LLM → TTS")

    # TODO: Build Pipecat pipeline
    # from pipecat.pipeline.pipeline import Pipeline
    # from pipecat.services.openai import OpenAILLMService
    # from pipecat.transports.local import LocalTransport
    #
    # transport = LocalTransport()
    # llm = OpenAILLMService(api_key=api_key, model="gpt-4o-mini")
    # pipeline = Pipeline([transport.input(), llm, transport.output()])
    # await pipeline.run()

    console.print("[yellow]Pipeline scaffold ready – uncomment and customize above.[/]")


if __name__ == "__main__":
    asyncio.run(main())

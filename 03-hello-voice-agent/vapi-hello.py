"""Minimal voice agent with VAPI.

Creates a VAPI assistant and starts a web call.
Requires VAPI_API_KEY in .env.
"""

import os

from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()


def main():
    api_key = os.getenv("VAPI_API_KEY")
    if not api_key:
        console.print("[red]Set VAPI_API_KEY in .env[/]")
        return

    console.print("[bold green]🤖 VAPI Hello Voice Agent[/]")
    console.print("This demo creates a minimal VAPI assistant with a single API call.")

    # TODO: Create and start a VAPI assistant
    # from vapi import Vapi
    #
    # client = Vapi(api_key=api_key)
    #
    # assistant = client.assistants.create(
    #     model={"provider": "openai", "model": "gpt-4o-mini"},
    #     voice={"provider": "cartesia", "voiceId": "a0e99841-438c-4a64-b679-ae501e7d6091"},
    #     first_message="Hello! I'm a VAPI voice agent. How can I help you?",
    #     transcriber={"provider": "deepgram", "model": "nova-2"},
    # )
    # console.print(f"[bold cyan]Assistant created:[/] {assistant.id}")
    #
    # # Start a web call
    # call = client.calls.create(assistant_id=assistant.id, type="web")
    # console.print(f"[bold cyan]Call started:[/] {call.id}")
    # console.print(f"[bold cyan]Web URL:[/] {call.web_call_url}")

    console.print("[yellow]Agent scaffold ready – uncomment and customize above.[/]")


if __name__ == "__main__":
    main()

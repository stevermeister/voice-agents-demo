"""Retell AI phone agent quickstart.

Creates a Retell agent and phone number via the API.
Requires RETELL_API_KEY in .env.
"""

import os

from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()


def main():
    api_key = os.getenv("RETELL_API_KEY")
    if not api_key:
        console.print("[red]Set RETELL_API_KEY in .env[/]")
        return

    console.print("[bold green]📞 Retell AI Quickstart[/]")

    # TODO: Create agent via Retell SDK
    # from retell import Retell
    #
    # client = Retell(api_key=api_key)
    #
    # # Create an agent
    # agent = client.agent.create(
    #     response_engine={"type": "retell-llm", "llm_id": "..."},
    #     voice_id="...",
    #     agent_name="Demo Agent",
    # )
    # console.print(f"Agent created: {agent.agent_id}")
    #
    # # Create a phone number
    # phone = client.phone_number.create(agent_id=agent.agent_id)
    # console.print(f"Phone number: {phone.phone_number}")

    console.print("[yellow]Setup scaffold ready – uncomment and customize above.[/]")


if __name__ == "__main__":
    main()

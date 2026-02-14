"""VAPI Quick Call – make an outbound phone call using the VAPI SDK.

Places a call to a phone number using the official vapi-server-sdk.
See: https://docs.vapi.ai/calls/outbound-calling

Prerequisites:
    1. VAPI_API_KEY in .env
    2. A VAPI phone number (free or imported) – grab the ID from the dashboard.

Usage:
    uv run 04-phone-agent/vapi-quickstart/quick-call.py +11234567890
"""

import os
import sys

from vapi import Vapi
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()


def make_call(destination: str):
    api_key = os.getenv("VAPI_API_KEY")
    phone_number_id = os.getenv("VAPI_PHONE_NUMBER_ID")

    if not api_key:
        console.print("[red]Set VAPI_API_KEY in .env[/]")
        return
    if not phone_number_id:
        console.print("[red]Set VAPI_PHONE_NUMBER_ID in .env (from VAPI dashboard → Phone Numbers)[/]")
        return

    client = Vapi(token=api_key)

    call = client.calls.create(
        phone_number_id=phone_number_id,
        customer={"number": destination},
        assistant={
            "model": {
                "provider": "openai",
                "model": "gpt-4o-mini",
                "system_prompt": (
                    "You are a friendly demo assistant. "
                    "Greet the user, ask how they are, then say goodbye. "
                    "Keep it under 30 seconds."
                ),
            },
            "voice": {
                "provider": "cartesia",
                "voice_id": "a0e99841-438c-4a64-b679-ae501e7d6091",
            },
            "first_message": "Hey! This is a quick demo call from VAPI. How are you?",
            "transcriber": {"provider": "deepgram", "model": "nova-2"},
            "end_call_message": "Thanks for trying the demo. Bye!",
            "max_duration_seconds": 60,
        },
    )

    console.print(f"[bold green]📞 Call created![/]")
    console.print(f"  Call ID:  {call.id}")
    console.print(f"  Status:   {call.status}")
    console.print(f"  To:       {destination}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[yellow]Usage: uv run 04-phone-agent/vapi-quickstart/quick-call.py +11234567890[/]")
        sys.exit(1)

    make_call(sys.argv[1])

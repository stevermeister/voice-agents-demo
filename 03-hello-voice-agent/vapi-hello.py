"""Minimal voice agent with VAPI.

Creates a VAPI assistant and serves a local web page where you can talk to it.
Requires VAPI_API_KEY (private) and VAPI_PUBLIC_KEY in .env.

Usage::

    uv run 03-hello-voice-agent/vapi-hello.py
    # Then open http://localhost:8080 in your browser
"""

import http.server
import os
import string
import threading
import webbrowser
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from vapi import Vapi

load_dotenv()
console = Console()

PORT = 8080
TEMPLATE_PATH = Path(__file__).parent / "vapi-hello.html"


def main():
    api_key = os.getenv("VAPI_API_KEY")
    public_key = os.getenv("VAPI_PUBLIC_KEY")

    if not api_key:
        console.print("[red]Set VAPI_API_KEY in .env (private key from dashboard)[/]")
        return
    if not public_key:
        console.print("[red]Set VAPI_PUBLIC_KEY in .env (public key from dashboard)[/]")
        return

    client = Vapi(token=api_key)

    console.print("[bold green]🤖 VAPI Hello Voice Agent[/]")
    console.print("Creating assistant …")

    try:
        assistant = client.assistants.create(
            name="Hello Voice Agent",
            first_message="Hello! I'm a VAPI voice agent. How can I help you today?",
            model={
                "provider": "openai",
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a friendly voice assistant. Keep your answers short "
                            "and conversational since they will be spoken aloud."
                        ),
                    }
                ],
            },
            voice={
                "provider": "cartesia",
                "voiceId": "a0e99841-438c-4a64-b679-ae501e7d6091",
            },
            transcriber={
                "provider": "deepgram",
                "model": "nova-3",
            },
        )
    except Exception as e:
        console.print(f"[red]Failed to create assistant:[/] {e}")
        return

    console.print(f"[bold cyan]Assistant:[/] {assistant.name} ({assistant.id})")

    # Build the HTML page from the template file
    template = string.Template(TEMPLATE_PATH.read_text())
    html = template.safe_substitute(
        assistant_id=assistant.id,
        assistant_name=assistant.name,
        public_key=public_key,
    )

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())

        def log_message(self, format, *args):
            pass  # suppress request logs

    server = http.server.HTTPServer(("", PORT), Handler)
    console.print(f"[bold green]🌐 Open http://localhost:{PORT} to talk to your agent[/]")
    console.print("[dim]Press Ctrl+C to stop[/]")

    # Open browser automatically
    threading.Timer(0.5, lambda: webbrowser.open(f"http://localhost:{PORT}")).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        console.print("\n[yellow]Shutting down …[/]")
        server.shutdown()


if __name__ == "__main__":
    main()

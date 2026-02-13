"""VAPI webhook server for phone agent events.

Receives call events from VAPI and handles them.
Requires VAPI_API_KEY in .env.
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()

PORT = 8080


class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        payload = json.loads(body)

        event_type = payload.get("message", {}).get("type", "unknown")
        console.print(f"[bold cyan]Event:[/] {event_type}")
        console.print(f"[dim]{json.dumps(payload, indent=2)[:200]}[/]")

        # Respond based on event type
        response = {"results": []}

        if event_type == "function-call":
            function_name = payload["message"].get("functionCall", {}).get("name")
            console.print(f"[yellow]Function call: {function_name}[/]")
            response["results"].append({"result": "Function executed successfully"})

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def log_message(self, format, *args):
        pass  # suppress default logging


def main():
    if not os.getenv("VAPI_API_KEY"):
        console.print("[yellow]Warning: VAPI_API_KEY not set in .env[/]")

    console.print(f"[bold green]🌐 VAPI webhook server running on http://localhost:{PORT}[/]")
    console.print("[dim]Use ngrok or similar to expose this endpoint to VAPI.[/]")

    server = HTTPServer(("", PORT), WebhookHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        console.print("\n[bold green]Server stopped.[/]")


if __name__ == "__main__":
    main()

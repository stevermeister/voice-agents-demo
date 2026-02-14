"""VAPI Server URL (webhook) handler.

Receives server events from VAPI during calls and responds where required.
See: https://docs.vapi.ai/server-url/events

All VAPI events arrive as POST requests with this shape:
    { "message": { "type": "<event-type>", "call": { ... }, ... } }

Most events are informational (respond with 200 OK).
These event types require a meaningful response body:
    - "assistant-request"   → return assistant config
    - "tool-calls"          → return tool results
    - "transfer-destination-request" → return transfer destination

Usage:
    1. Start this server:  uv run 04-phone-agent/vapi-quickstart/webhook-server.py
    2. Expose via tunnel:  ngrok http 3000
    3. Set the ngrok URL as your Server URL in the VAPI dashboard.
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()

PORT = 3000


class VapiWebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        payload = json.loads(body)

        message = payload.get("message", {})
        event_type = message.get("type", "unknown")

        console.print(f"\n[bold cyan]━━ Event: {event_type} ━━[/]")

        response = self._handle_event(event_type, message)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def _handle_event(self, event_type: str, message: dict) -> dict:
        """Route event to the appropriate handler."""

        if event_type == "assistant-request":
            return self._handle_assistant_request(message)

        if event_type == "tool-calls":
            return self._handle_tool_calls(message)

        if event_type == "transfer-destination-request":
            return self._handle_transfer_request(message)

        if event_type == "status-update":
            status = message.get("status", "")
            console.print(f"  Call status → [yellow]{status}[/]")

        elif event_type == "transcript":
            role = message.get("role", "")
            transcript_type = message.get("transcriptType", "")
            text = message.get("transcript", "")
            console.print(f"  [{transcript_type}] {role}: {text}")

        elif event_type == "end-of-call-report":
            reason = message.get("endedReason", "unknown")
            console.print(f"  Call ended: [red]{reason}[/]")
            artifact = message.get("artifact", {})
            if artifact.get("transcript"):
                console.print(f"  [dim]Transcript: {artifact['transcript'][:200]}[/]")

        elif event_type == "hang":
            console.print("  [red]⚠ Assistant is hanging (no response)[/]")

        elif event_type == "speech-update":
            status = message.get("status", "")
            role = message.get("role", "")
            console.print(f"  Speech {status} ({role})")

        elif event_type == "conversation-update":
            msgs = message.get("messages", [])
            console.print(f"  Conversation updated ({len(msgs)} messages)")

        else:
            console.print(f"  [dim]{json.dumps(message, indent=2)[:300]}[/]")

        return {}

    def _handle_assistant_request(self, message: dict) -> dict:
        """Return assistant configuration dynamically.

        VAPI sends this when a call starts and no assistant is pre-configured,
        allowing you to return different assistants per caller.
        """
        call = message.get("call", {})
        caller = call.get("customer", {}).get("number", "unknown")
        console.print(f"  Assistant requested for caller: [green]{caller}[/]")

        return {
            "assistant": {
                "model": {
                    "provider": "openai",
                    "model": "gpt-4o-mini",
                    "systemPrompt": "You are a helpful phone assistant. Be concise.",
                },
                "voice": {
                    "provider": "cartesia",
                    "voiceId": "a0e99841-438c-4a64-b679-ae501e7d6091",
                },
                "firstMessage": "Hello! How can I help you today?",
                "transcriber": {"provider": "deepgram", "model": "nova-2"},
            }
        }

    def _handle_tool_calls(self, message: dict) -> dict:
        """Execute tool calls and return results.

        VAPI sends this when the LLM invokes a tool defined in the assistant config.
        Each tool call must be answered with a matching toolCallId.
        """
        tool_call_list = message.get("toolCallList", [])
        results = []

        for tool_call in tool_call_list:
            name = tool_call.get("name", "")
            call_id = tool_call.get("id", "")
            params = tool_call.get("parameters", {})
            console.print(f"  Tool: [yellow]{name}[/] (id={call_id})")
            console.print(f"    Params: {json.dumps(params)}")

            # TODO: implement your tool logic here
            result = f'{{"status": "ok", "message": "{name} executed successfully"}}'

            results.append({
                "name": name,
                "toolCallId": call_id,
                "result": result,
            })

        return {"results": results}

    def _handle_transfer_request(self, message: dict) -> dict:
        """Return a transfer destination when the assistant requests a call transfer."""
        console.print("  [yellow]Transfer requested[/]")

        # TODO: look up the right number based on conversation context
        return {
            "destination": {"type": "number", "number": "+11234567890"},
            "message": {"type": "request-start", "message": "Transferring you now."},
        }

    def log_message(self, format, *args):
        pass  # suppress default HTTP logging


def main():
    if not os.getenv("VAPI_API_KEY"):
        console.print("[yellow]Warning: VAPI_API_KEY not set in .env[/]")

    console.print(f"[bold green]🌐 VAPI webhook server on http://localhost:{PORT}[/]")
    console.print("[dim]Expose with: ngrok http 3000[/]")
    console.print("[dim]Then set the ngrok URL as your Server URL in the VAPI dashboard.[/]\n")

    server = HTTPServer(("", PORT), VapiWebhookHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        console.print("\n[bold green]Server stopped.[/]")


if __name__ == "__main__":
    main()

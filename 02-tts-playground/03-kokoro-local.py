"""Local TTS with Kokoro – no API key needed.

Runs Kokoro TTS entirely on your machine.
"""

from rich.console import Console

console = Console()


def main():
    # TODO: integrate kokoro-onnx or kokoro python package
    # pip install kokoro-onnx
    console.print("[bold yellow]Kokoro local TTS demo[/]")
    console.print("This demo runs TTS entirely on your machine using Kokoro.")
    console.print("[dim]Implementation coming soon – install kokoro-onnx to get started.[/]")

    text = "Hello! I'm a voice agent running entirely on your local machine."
    console.print(f"\n[bold cyan]Text:[/] {text}")
    console.print("[yellow]TODO: Generate audio with Kokoro and save to kokoro_output.wav[/]")


if __name__ == "__main__":
    main()

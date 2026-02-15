"""Local TTS with Kokoro – no API key needed.

Runs Kokoro TTS entirely on your machine using the Kokoro-82M model.
First run downloads the model (~327 MB) and voice pack.

Usage::

    uv run 02-tts-playground/03-kokoro-local.py
    uv run 02-tts-playground/03-kokoro-local.py --voice af_heart
"""

import argparse
import os
import subprocess
import sys
import warnings

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "0"
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

import numpy as np
import soundfile as sf
from kokoro import KPipeline
from rich.console import Console

console = Console()

OUTPUT_FILE = "kokoro_output.wav"
SAMPLE_RATE = 24000


def main():
    parser = argparse.ArgumentParser(description="Local TTS with Kokoro")
    parser.add_argument(
        "--voice", default="af_heart",
        help="Kokoro voice name (default: af_heart). See https://huggingface.co/hexgrad/Kokoro-82M",
    )
    args = parser.parse_args()

    text = "Hello! I'm a voice agent running entirely on your local machine. No API key needed."

    console.print(f"[bold green]🔊 Generating:[/] {text}")
    console.print(f"[dim]Voice: {args.voice}[/]")

    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    generator = pipeline(text, voice=args.voice)

    # Concatenate all audio chunks and save
    chunks = []
    for _i, (_gs, _ps, audio) in enumerate(generator):
        chunks.append(audio)

    full_audio = np.concatenate(chunks)
    sf.write(OUTPUT_FILE, full_audio, SAMPLE_RATE)

    console.print(f"[bold green]✅ Saved to {OUTPUT_FILE}[/]")

    # Play the audio
    if sys.platform == "darwin":
        subprocess.run(["afplay", OUTPUT_FILE])
    else:
        subprocess.run(["ffplay", "-autoexit", "-nodisp", OUTPUT_FILE])


if __name__ == "__main__":
    main()

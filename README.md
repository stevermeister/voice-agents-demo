# 🎙️ Voice Agents Crash Course

> Demo code for my talk at [AI Coding Summit](https://aicodingsummit.com/#person-stepan-suvorov)

## Structure

| Module | What you'll learn |
|--------|-------------------|
| **01-stt-playground** | Speech-to-Text: Whisper local, Deepgram streaming, provider comparison |
| **02-tts-playground** | Text-to-Speech: Cartesia, ElevenLabs, Kokoro local, latency comparison |
| **03-hello-voice-agent** | Minimal voice agents with Pipecat & LiveKit |
| **04-phone-agent** | Phone integration: VAPI, LiveKit SIP, Retell |
| **cost-calculator.html** | Interactive cost calculator: managed vs self-hosted |

## Quick Start

```bash
# 1. Clone & enter
git clone https://github.com/stevermeister/voice-agents-demo.git
cd voice-agents-demo

# 2. Install dependencies (requires uv)
uv sync

# 3. Copy env and fill in your API keys
cp .env.example .env

# 4. Run any demo
uv run 01-stt-playground/01-whisper-local.py
```

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- API keys (see `.env.example`)

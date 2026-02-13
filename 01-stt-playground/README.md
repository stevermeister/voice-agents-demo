# 01 – Speech-to-Text Playground

Explore different STT approaches: local Whisper, cloud streaming, and a head-to-head comparison.

## Demos

| Script | Description |
|--------|-------------|
| `01-whisper-local.py` | Run OpenAI Whisper locally – no API key needed |
| `02-deepgram-streaming.py` | Real-time streaming transcription with Deepgram |
| `03-compare-providers.py` | Compare accuracy, latency & cost across providers |

## Run

```bash
uv run 01-stt-playground/01-whisper-local.py
uv run 01-stt-playground/02-deepgram-streaming.py
uv run 01-stt-playground/03-compare-providers.py
```

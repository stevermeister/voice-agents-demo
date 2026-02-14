# 04 – Phone Agent

Build voice agents that work over the phone using four different platforms.

## Demos

| Directory | Description |
|-----------|-------------|
| `vapi-quickstart/` | Managed phone agent with VAPI – assistant config + webhook server |
| `livekit-sip/` | Self-hosted phone agent with LiveKit SIP |
| `retell-quickstart/` | Managed phone agent with Retell AI |
| `pipecat-phone/` | Self-hosted phone agent with Pipecat + Daily/Twilio |

## Run

```bash
# VAPI
uv run 04-phone-agent/vapi-quickstart/webhook-server.py

# LiveKit SIP
uv run 04-phone-agent/livekit-sip/agent.py

# Retell
uv run 04-phone-agent/retell-quickstart/setup.py

# Pipecat
uv run 04-phone-agent/pipecat-phone/agent.py
```

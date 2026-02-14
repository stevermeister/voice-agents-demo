"""Pipecat Quick Call – make an outbound phone call with a voice AI agent.

Dials a phone number via Daily PSTN and runs a Pipecat voice pipeline.
See: https://docs.pipecat.ai/guides/telephony/daily-pstn

Requires: DAILY_API_KEY, OPENAI_API_KEY, DEEPGRAM_API_KEY, CARTESIA_API_KEY in .env

Usage:
    uv run 04-phone-agent/pipecat-phone/quickstart.py +11234567890
"""

import asyncio
import os
import sys

import httpx
from dotenv import load_dotenv
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import (
    LLMContextAggregatorPair,
    LLMUserAggregatorParams,
)
from pipecat.services.cartesia.tts import CartesiaTTSService
from pipecat.services.deepgram.stt import DeepgramSTTService
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.transports.daily.transport import DailyParams, DailyTransport

load_dotenv(override=True)

DAILY_API_KEY = os.getenv("DAILY_API_KEY", "")


async def main(phone_number: str):
    # Create a Daily room with dial-out enabled
    headers = {"Authorization": f"Bearer {DAILY_API_KEY}"}
    async with httpx.AsyncClient() as client:
        room = (await client.post("https://api.daily.co/v1/rooms", headers=headers, json={"properties": {"enable_dialout": True}})).json()
        token = (await client.post("https://api.daily.co/v1/meeting-tokens", headers=headers, json={"properties": {"room_name": room["name"], "is_owner": True}})).json()["token"]

    # Transport
    transport = DailyTransport(room["url"], token, "Phone Agent", params=DailyParams(api_key=DAILY_API_KEY, audio_in_enabled=True, audio_out_enabled=True))

    # AI services
    stt = DeepgramSTTService(api_key=os.getenv("DEEPGRAM_API_KEY"))
    llm = OpenAILLMService(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini")
    tts = CartesiaTTSService(api_key=os.getenv("CARTESIA_API_KEY", ""), voice_id="a0e99841-438c-4a64-b679-ae501e7d6091")

    # Conversation context (same prompt as the VAPI quick-call demo)
    context = LLMContext([{"role": "system", "content": "You are a friendly demo assistant. Greet the user, ask how they are, then say goodbye. Keep it under 30 seconds."}])
    user_aggregator, assistant_aggregator = LLMContextAggregatorPair(context, user_params=LLMUserAggregatorParams(vad_analyzer=SileroVADAnalyzer()))

    # Pipeline
    pipeline = Pipeline([transport.input(), stt, user_aggregator, llm, tts, transport.output(), assistant_aggregator])
    task = PipelineTask(pipeline, params=PipelineParams(audio_in_sample_rate=8000, audio_out_sample_rate=8000))

    # Dial out when bot joins the room
    @transport.event_handler("on_joined")
    async def on_joined(transport, data):
        await transport.start_dialout([{"phoneNumber": phone_number}])

    @transport.event_handler("on_participant_left")
    async def on_participant_left(transport, participant, reason):
        await task.cancel()

    await PipelineRunner().run(task)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run quickstart.py +1234567890")
        sys.exit(1)
    asyncio.run(main(sys.argv[1]))

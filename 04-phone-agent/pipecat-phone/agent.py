"""Pipecat phone agent via Daily PSTN.

A voice agent that handles inbound phone calls using Pipecat with Daily's
PSTN dial-in capabilities. Deploy to Pipecat Cloud or run locally.

Required env vars: OPENAI_API_KEY, DEEPGRAM_API_KEY, CARTESIA_API_KEY.

Run locally::

    uv run agent.py

See https://docs.pipecat.ai/examples for the full phone-chatbot examples.
"""

import os

from dotenv import load_dotenv
from loguru import logger
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.audio.vad.vad_analyzer import VADParams
from pipecat.frames.frames import LLMRunFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import (
    LLMContextAggregatorPair,
    LLMUserAggregatorParams,
)
from pipecat.runner.types import DailyDialinRequest, RunnerArguments
from pipecat.services.cartesia.tts import CartesiaTTSService
from pipecat.services.deepgram.stt import DeepgramSTTService
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.transports.base_transport import BaseTransport
from pipecat.transports.daily.transport import DailyDialinSettings, DailyParams, DailyTransport

load_dotenv(override=True)


async def run_bot(transport: BaseTransport, handle_sigint: bool) -> None:
    """Run the voice bot pipeline for an inbound phone call."""

    stt = DeepgramSTTService(api_key=os.getenv("DEEPGRAM_API_KEY"))

    tts = CartesiaTTSService(
        api_key=os.getenv("CARTESIA_API_KEY", ""),
        voice_id="b7d50908-b17c-442d-ad8d-810c63997ed9",  # Helpful Woman
    )

    llm = OpenAILLMService(api_key=os.getenv("OPENAI_API_KEY"))

    messages = [
        {
            "role": "system",
            "content": (
                "You are a friendly phone assistant. Your responses will be read aloud, "
                "so keep them concise and conversational. Avoid special characters or "
                "formatting. Begin by greeting the caller and asking how you can help them today."
            ),
        },
    ]

    context = LLMContext(messages)
    user_aggregator, assistant_aggregator = LLMContextAggregatorPair(
        context,
        user_params=LLMUserAggregatorParams(
            vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=0.2)),
        ),
    )

    pipeline = Pipeline(
        [
            transport.input(),
            stt,
            user_aggregator,
            llm,
            tts,
            transport.output(),
            assistant_aggregator,
        ]
    )

    task = PipelineTask(
        pipeline,
        params=PipelineParams(
            enable_metrics=True,
            enable_usage_metrics=True,
            audio_in_sample_rate=8000,
            audio_out_sample_rate=8000,
        ),
    )

    @transport.event_handler("on_first_participant_joined")
    async def on_first_participant_joined(transport, participant):
        logger.debug(f"First participant joined: {participant['id']}")
        await task.queue_frames([LLMRunFrame()])

    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):
        logger.info(f"Client disconnected")
        await task.cancel()

    @transport.event_handler("on_dialin_error")
    async def on_dialin_error(transport, data):
        logger.error(f"Dial-in error: {data}")
        await task.cancel()

    runner = PipelineRunner(handle_sigint=handle_sigint)
    await runner.run(task)


async def bot(runner_args: RunnerArguments):
    """Main bot entry point compatible with Pipecat Cloud.

    Parses runner arguments, configures Daily transport with dial-in
    settings, and starts the bot to handle the incoming call.
    """
    try:
        request = DailyDialinRequest.model_validate(runner_args.body)

        daily_dialin_settings = DailyDialinSettings(
            call_id=request.dialin_settings.call_id,
            call_domain=request.dialin_settings.call_domain,
        )

        transport = DailyTransport(
            runner_args.room_url,
            runner_args.token,
            "Pipecat Phone Agent",
            params=DailyParams(
                api_key=request.daily_api_key,
                api_url=request.daily_api_url,
                dialin_settings=daily_dialin_settings,
                audio_in_enabled=True,
                audio_out_enabled=True,
            ),
        )

        if request.dialin_settings.From:
            logger.info(f"Handling call from: {request.dialin_settings.From}")

        await run_bot(transport, runner_args.handle_sigint)

    except Exception as e:
        logger.error(f"Error running bot: {e}")
        raise


if __name__ == "__main__":
    from pipecat.runner.run import main

    main()

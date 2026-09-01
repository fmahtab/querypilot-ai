import asyncio
import uuid

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.services.agent.agent import root_agent

load_dotenv()

APP_NAME = "querypilot"
USER_ID = "querypilot-user"


async def _run_knowledge_agent(question: str) -> str:
    session_service = InMemorySessionService()

    session_id = str(uuid.uuid4())

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    message = types.Content(
        role="user",
        parts=[types.Part(text=question)],
    )

    final_answer = ""

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=message,
    ):
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if part.text:
                    final_answer = part.text

    return final_answer


def run_knowledge_agent(question: str) -> str:
    return asyncio.run(_run_knowledge_agent(question))
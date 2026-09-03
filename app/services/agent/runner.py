import asyncio
import uuid

from dataclasses import dataclass
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.genai.errors import ClientError, ServerError

from app.services.agent.agent import root_agent

load_dotenv()

APP_NAME = "querypilot"
USER_ID = "querypilot-user"

@dataclass
class KnowledgeAgentResult:
    answer: str
    sources: list[str]


async def _run_knowledge_agent(
    question: str,
    memory_context: str = "",
    ) -> KnowledgeAgentResult:
    session_service = InMemorySessionService()

    session_id = str(uuid.uuid4())

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
        state={
            "memory_context": memory_context or "No durable user memory available.",
        },
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
    sources: list[str] = []

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=message,
    ):
       
        if event.content:
            for part in event.content.parts:
                if part.function_response:
                    response = part.function_response.response

                    if isinstance(response, dict):
                        for result in response.get("results", []):
                            source = result.get("source")

                            if source and source not in sources:
                                sources.append(source)
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if part.text:
                    final_answer = part.text

    return KnowledgeAgentResult(
        answer=final_answer,
        sources=sources,
    )


def run_knowledge_agent(
    question: str,
    memory_context: str = "",
    ) -> KnowledgeAgentResult:
    try:
        return asyncio.run(
            _run_knowledge_agent(
                question,
                memory_context,
            )
        )
    except (ClientError, ServerError) as exc:
        raise RuntimeError(
            "The knowledge agent is temporarily unavailable."
        ) from exc
import asyncio

from dotenv import load_dotenv

load_dotenv()


from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.services.agent.agent import root_agent


APP_NAME = "querypilot"
USER_ID = "test-user"
SESSION_ID = "test-session"


async def main():
    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    message = types.Content(
        role="user",
        parts=[types.Part(text="What is BOPIS?")],
    )

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=message,
    ):
        print(event)


if __name__ == "__main__":
    asyncio.run(main())
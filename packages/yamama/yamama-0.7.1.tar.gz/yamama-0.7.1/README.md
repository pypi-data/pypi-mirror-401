# Riyadh Artificial Intelligence Agents SDK

Yamama is RiyadhAI’s Python SDK for building realtime AI agents.

Use it to connect your apps to realtime AI, orchestration, and robotics workflows.

## Version

0.7.1

## Install

```bash
pip install yamama
```

Optional extras:

```bash
pip install "yamama[mcp]"
pip install "yamama[images]"
```

## What You Get

- Realtime agents with LiveKit rooms
- Built-in provider plugins (including Google)
- Session/agent lifecycle management
- Optional MCP and image utilities via extras

## Environment (.env)

Create a `.env` file (keep it private; don’t commit it):

```env
# LiveKit
RIYADHAI_URL="wss://YOUR-RIYADHAI-HOST"
RIYADHAI_API_KEY="YOUR_RIYADHAI_KEY"
RIYADHAI_API_SECRET="YOUR_RIYADHAI_SECRET"

# Google (pick one mode)
# GOOGLE_API_KEY="YOUR_GOOGLE_GEMINI_API_KEY"
# GOOGLE_GENAI_USE_VERTEXAI="1"
# GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
# GOOGLE_CLOUD_PROJECT="your-gcp-project"
# GOOGLE_CLOUD_LOCATION="us-central1"
```

If you want to load `.env` automatically, install `python-dotenv`:

```bash
pip install python-dotenv
```

## Quickstart (Google Realtime)

Create `agent.py`:

```python
from dotenv import load_dotenv

from yamama import agents
from yamama.agents import Agent, AgentServer, AgentSession
from yamama.plugins import google

load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful bot.")


server = AgentServer()


@server.rtc_session()
async def my_agent(ctx: agents.JobContext) -> None:
    session = AgentSession(
        llm=google.realtime.RealtimeModel(
            model="gemini-live-2.5-flash-native-audio",
            voice="Puck",
        )
    )

    await session.start(room=ctx.room, agent=Assistant())
    await session.generate_reply(
        instructions="Greet the user and offer your assistance. You should start by speaking in English."
    )


if __name__ == "__main__":
    agents.cli.run_app(server)
```

Run:

```bash
python agent.py dev
# or
python agent.py start
```

## Notes

- Environment variables: Yamama reads `RIYADHAI_URL/RIYADHAI_API_KEY/RIYADHAI_API_SECRET`.

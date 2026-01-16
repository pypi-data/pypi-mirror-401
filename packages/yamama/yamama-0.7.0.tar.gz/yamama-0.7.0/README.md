# RAIA (Riyadh Artificial Intelligence Agents)

AI connectivity & Robotics 

## Version

0.7.0

## Install

```bash
pip install yamama
```

## Environment (.env)

Create a `.env` file (keep it private; don’t commit it):

```env
# LiveKit
YAMAMA_URL="wss://YOUR-LIVEKIT-HOST"
YAMAMA_API_KEY="YOUR_LIVEKIT_KEY"
YAMAMA_API_SECRET="YOUR_LIVEKIT_SECRET"

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
```

from google.adk import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
import litellm
import os

litellm._turn_on_debug()
from config import Config
groq_model = LiteLlm(model=Config.MODEL_llama3_70b,api_key=os.environ.get("GROQ_API_KEY"))

# Point to the local endpoints the CLI hosts them on
remote_agent_one = RemoteA2aAgent(
    name="remote_agent_one",
    description="Compiles raw data.",
    agent_card=f"http://127.0.0.1:8081/a2a/agent_one_dir{AGENT_CARD_WELL_KNOWN_PATH}"
)

remote_agent_two = RemoteA2aAgent(
    name="remote_agent_two",
    description="Formats into Markdown.",
    agent_card=f"http://127.0.0.1:8082/a2a/agent_two_dir{AGENT_CARD_WELL_KNOWN_PATH}"
   
)

# Convert agents into Pydantic-compliant BaseTools
tool_one = AgentTool(agent=remote_agent_one)
tool_two = AgentTool(agent=remote_agent_two)

root_agent = Agent(
    name="supervisor_hub",
    model=groq_model,
    instruction=(
            "You are a strict sequential coordination pipeline executor. Your only job is to route strings between tools.\n\n"
            "CRITICAL: When calling a tool, always provide your input inside a single structured string argument named 'query' or 'text'. Do not include extra brackets, empty arrays, or custom formatting strings in the tool call structure.\n\n"
            "Execute these steps in order:\n"
            "Step 1: Invoke 'remote_agent_one' by passing the user's initial prompt directly to it.\n"
            "Step 2: Take the text response string returned by 'remote_agent_one', pass it as the direct input argument to 'remote_agent_two', and ask it to format the data into clean Markdown.\n"
            "Step 3: Output the exact finalized text string from 'remote_agent_two' back to the user without adding your own commentary."
    ),
    tools=[tool_one, tool_two]
)
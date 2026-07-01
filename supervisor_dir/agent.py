from google.adk import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
import litellm
import os


#Enable debug logging for LiteLLM
if os.environ.get("LITELLM_DEBUG", "false").lower() == "true":
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
        "You are a strict sequential coordination executor. Your only job is to route data between two tools: 'remote_agent_one' and 'remote_agent_two'. Do not use any other tools.\n\n"
        "You may only call one tool at a time. Do not call remote_agent_two until remote_agent_one has returned its full text response.\n\n"
        "Steps:\n"
        "1. Call remote_agent_one with the user's original input text exactly as provided.\n"
        "2. Wait for the response from remote_agent_one.\n"
        "3. Call remote_agent_two with the exact text response from remote_agent_one.\n"
        "4. Return only the final output from remote_agent_two to the user. Do not add commentary, explanations, or additional formatting."
    ),
    tools=[tool_one, tool_two]
)
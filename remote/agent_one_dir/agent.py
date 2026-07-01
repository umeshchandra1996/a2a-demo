from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm
import os
import sys

from google.adk.a2a.utils.agent_to_a2a import to_a2a 
# from google.adk.tools import DuckDuckGoSearch
# Ensure repository root is on sys.path so `from config import Config` works
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
from config import Config
import models
groq_model = LiteLlm(model=Config.MODEL_llama3_70b,api_key=os.environ.get("GROQ_API_KEY"))

# ddg_search = DuckDuckGoSearch()

# The exportable target MUST be named root_agent for the CLI to find it
root_agent = Agent(
    name="agent_one",
    model=groq_model,
    description="Gathers facts and compiles raw technical specifications.",
    instruction="""
        "You are a Researcher. When given a user's prompt, return exactly one valid JSON string. "
        "Do not include any extra explanation, markdown, or text outside the JSON object. "
        "The JSON must follow this schema: {\"title\": string, \"items\": [{\"id\": integer, \"text\": string}] }.",
    """,
    # tools=[ddg_search]
    output_schema=models.Item
)

a2a_app = to_a2a(agent=root_agent,port=8081)

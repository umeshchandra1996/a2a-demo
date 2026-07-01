from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm
import os
import sys
from pathlib import Path
from google.adk.a2a.utils.agent_to_a2a import to_a2a 
# Ensure repository root is on sys.path so `from config import Config` works
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
from config import Config
groq_model = LiteLlm(model=Config.MODEL_llama3_70b,api_key=os.environ.get("GROQ_API_KEY"))

root_agent = Agent(
    name="agent_two",
    model=groq_model,
    description="Formats and cleans up unorganized raw data blocks into polished Markdown.",
    instruction="You are an Editor. Clean up raw text and structure it cleanly with headers."
)

a2a_app = to_a2a(agent=root_agent,port=8082)


from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm
import os
from pathlib import Path
from google.adk.a2a.utils.agent_to_a2a import to_a2a 
import config
groq_model = LiteLlm(model=config.Config.MODEL_llama3_70b,api_key=os.environ.get("GROQ_API_KEY"))

root_agent = Agent(
    name="agent_two",
    model=groq_model,
    description="Formats and cleans up unorganized raw data blocks into polished Markdown.",
    instruction="You are an Editor. Clean up raw text and structure it cleanly with headers."
)

a2a_app = to_a2a(agent=root_agent,port=8082)

# # CRITICAL ADDITION: Run the application server
# if __name__ == "__main__":
#     import uvicorn
#     # Use "0.0.0.0" to allow network access, or "localhost" for local-only testing
#     uvicorn.run(a2a_app, host="127.0.0.1", port=8082)

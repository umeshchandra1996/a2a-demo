from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm
import os
from google.adk.a2a.utils.agent_to_a2a import to_a2a 
# from google.adk.tools import DuckDuckGoSearch
import config
groq_model = LiteLlm(model=config.Config.MODEL_llama3_70b,api_key=os.environ.get("GROQ_API_KEY"))
# ddg_search = DuckDuckGoSearch()

# The exportable target MUST be named root_agent for the CLI to find it
root_agent = Agent(
    name="agent_one",
    model=groq_model,
    description="Gathers facts and compiles raw technical specifications.",
    instruction="You are a Researcher. Provide raw, factual bullet points.",
    # tools=[ddg_search]
)

a2a_app = to_a2a(agent=root_agent,port=8081)
# if __name__ == "__main__":
#     import uvicorn
#     # Use "0.0.0.0" to allow network access, or "localhost" for local-only testing
#     uvicorn.run(a2a_app, host="127.0.0.1", port=8081)

uv init
uv venv

create requirement.txt with library
uv add -r requirement.txt
uv sync


For RemoteA2Agent setup agent.json should be in correct format as per documention. 

1. adk api_server --a2a --port 8081 .\remote
2. adk api_server --a2a --port 8082 .\remote2
3. adk run supervisor_dir

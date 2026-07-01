uv init
uv venv

create requirement.txt with library
uv add -r requirement.txt
uv sync

For RemoteA2Agent setup agent.json should be in correct format as per documention.
All Remote Agent shloud be in remote/ folder seprate separte.

Quick run (manual):

1. Start agent one (raw data collector):

```powershell
adk api_server --a2a --port 8081 .\remote
```

2. Start agent two (formatter):

```powershell
adk api_server --a2a --port 8082 .\remote2
```

3. Start the supervisor (coordinates agents):

```powershell
adk run supervisor_dir
```

Recommended: Use the provided `Makefile` and startup script which handle ordering, logging, and health checks.

Makefile targets:

```powershell
make start-all       # start agents and supervisor (cross-platform via Python helper)
make start-agents    # start agents (includes health checks)
make start-supervisor# start only the supervisor
make logs            # list log files created in logs/
```

Or run the startup script directly:

```powershell
python scripts/start_agents.py
```

Logs are written to `logs/` in the repository root.


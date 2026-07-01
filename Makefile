.PHONY: start start-agents start-supervisor health logs

start: start-all

start-all: start-agents start-supervisor
	@echo "Started agents and supervisor (see logs/)"

start-agents:
	python scripts/start_agents.py

start-supervisor:
	adk run supervisor_dir &
	@sleep 1
	@echo "Supervisor started"

health:
	@echo "Use the startup script which includes health checks: `make start-agents`"

logs:
	@echo "Log files are in logs/"
	@ls -la logs || dir logs

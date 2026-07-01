"""
Start both remote agents and the supervisor with health checks and simple retries.
Run: python scripts/start_agents.py

This script spawns `adk api_server` processes for remote agents and then starts
`adk run supervisor_dir`. It polls the agents' base URLs to confirm readiness.
"""
import os
import subprocess
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

AGENTS = [
    {"name": "agent_one", "port": 8081, "path": "remote/agent_one_dir"},
    {"name": "agent_two", "port": 8082, "path": "remote2/agent_two_dir"},
]

START_CMDS = [
    f"adk api_server --a2a --port {a['port']} {os.path.join('.', a['path'])}"
    for a in AGENTS
]
SUPERVISOR_CMD = "adk run supervisor_dir"


def check_url(url, timeout=3):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return resp.status < 400
    except Exception:
        return False


def wait_for_agent(name, port, path, timeout=30):
    url = f"http://127.0.0.1:{port}/a2a/{Path(path).name}"
    deadline = time.time() + timeout
    while time.time() < deadline:
        if check_url(url):
            print(f"{name} is healthy at {url}")
            return True
        print(f"Waiting for {name} at {url}...")
        time.sleep(1)
    print(f"Timed out waiting for {name} at {url}")
    return False


def start_process(cmd, logfile):
    f = open(logfile, "a", buffering=1)
    print(f"Starting: {cmd} (logs -> {logfile})")
    proc = subprocess.Popen(cmd, shell=True, cwd=ROOT, stdout=f, stderr=subprocess.STDOUT)
    return proc


def main():
    procs = []

    # Start agents
    for a, cmd in zip(AGENTS, START_CMDS):
        log = LOG_DIR / f"{a['name']}.log"
        proc = start_process(cmd, str(log))
        procs.append((a['name'], proc))

    # Wait for agents to become healthy, with one retry each
    for a in AGENTS:
        ok = wait_for_agent(a['name'], a['port'], a['path'], timeout=25)
        if not ok:
            print(f"Retrying start for {a['name']}...")
            # try restarting once
            cmd = f"adk api_server --a2a --port {a['port']} {os.path.join('.', a['path'])}"
            log = LOG_DIR / f"{a['name']}.log"
            proc = start_process(cmd, str(log))
            procs.append((a['name'] + "-retry", proc))
            ok = wait_for_agent(a['name'], a['port'], a['path'], timeout=20)
            if not ok:
                print(f"ERROR: {a['name']} failed to start after retry. Check logs: {log}")

    # Start supervisor (does not block; started in background)
    sup_log = LOG_DIR / "supervisor.log"
    sup_proc = start_process(SUPERVISOR_CMD, str(sup_log))
    procs.append(("supervisor", sup_proc))

    print("Started processes:")
    for name, p in procs:
        print(f"- {name}: PID {p.pid}")

    print("Logs are in the logs/ directory.")
    print("Press Ctrl+C to exit; processes will continue running in background.")


if __name__ == "__main__":
    main()

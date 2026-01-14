#!/usr/bin/env python3
"""Hook PreToolUse: Log des événements Task, Bash, Edit, Write."""

import json
import sys
from datetime import datetime
from pathlib import Path


def get_log_dir() -> Path:
    """Get the log directory path (cross-platform)."""
    return Path.home() / ".claude" / "logs"


def log_event(message: str) -> None:
    """Log an event to the events.log file."""
    log_dir = get_log_dir()
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "events.log"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


def main() -> int:
    # Read input from stdin
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        print('{"decision": "allow"}')
        return 0

    tool_name = input_data.get("tool_name", "unknown")
    tool_input = input_data.get("tool_input", {})

    if tool_name == "Task":
        agent = tool_input.get("subagent_type", "")
        desc = tool_input.get("description", "")
        log_event(f"[AGENT] {agent} | {desc}")
    elif tool_name == "Bash":
        cmd = tool_input.get("command", "")
        log_event(f"[BASH] {cmd}")
    elif tool_name == "Edit":
        file_path = tool_input.get("file_path", "")
        file_name = Path(file_path).name if file_path else "unknown"
        log_event(f"[EDIT] {file_name}")
    elif tool_name == "Write":
        file_path = tool_input.get("file_path", "")
        file_name = Path(file_path).name if file_path else "unknown"
        log_event(f"[WRITE] {file_name}")

    print('{"decision": "allow"}')
    return 0


if __name__ == "__main__":
    sys.exit(main())

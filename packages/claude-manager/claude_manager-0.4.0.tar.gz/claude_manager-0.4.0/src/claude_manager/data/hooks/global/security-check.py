#!/usr/bin/env python3
"""Hook PreToolUse: Vérification sécurité avant Edit/Write."""

import json
import re
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

    tool_input = input_data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    content = tool_input.get("content", "") or tool_input.get("new_string", "")
    file_name = Path(file_path).name if file_path else "unknown"

    log_event(f"[HOOK] security-check | {file_name}")

    # Exclude hooks directory
    if "/.claude/hooks/" in file_path or "\\.claude\\hooks\\" in file_path:
        print('{"decision": "allow"}')
        return 0

    # Check for GitHub tokens
    if re.search(r"ghp_[a-zA-Z0-9]{36}", content):
        log_event(f"[HOOK] security-check | BLOCKED: {file_name}")
        print('{"decision": "block", "reason": "Secret detected"}')
        return 0

    print('{"decision": "allow"}')
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Hook PostToolUse: Rappel TDD après modification de fichier."""

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

    tool_input = input_data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    file_name = Path(file_path).name if file_path else "unknown"

    log_event(f"[HOOK] tdd-reminder | {file_name}")

    # Skip if it's already a test file
    if ".spec." in file_path or ".test." in file_path:
        print('{"decision": "allow"}')
        return 0

    print('{"decision": "allow"}')
    return 0


if __name__ == "__main__":
    sys.exit(main())

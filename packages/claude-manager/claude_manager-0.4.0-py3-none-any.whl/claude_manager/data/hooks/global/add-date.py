#!/usr/bin/env python3
"""Hook UserPromptSubmit - Ajoute la date actuelle au contexte."""

import sys
from datetime import datetime


def main() -> int:
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M:%S")
    day_of_week = now.strftime("%A")

    print("<user-prompt-submit-hook>")
    print(f"Date actuelle: {date_str} ({day_of_week})")
    print("</user-prompt-submit-hook>")

    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Unsent: The Micro-Confession Sprint.

Writes the chosen micro-confession entry to /output/entry.txt
(falling back to ./output/entry.txt) with no trailing newline,
then reads it back and verifies it byte-for-byte.
"""

import os
import sys

# Why this reads as genuinely unsent: the To: line and the message
# need each other ("the other person in the car" is meaningless alone,
# the confession means nothing without who it was to). It is specific
# and honest — a named age, a named reason, no vague regret. And it
# costs the writer: he admits he let someone else take the blame
# that was his, and kept the secret ever since.
TO_LINE = "To: the other person in the car"
MESSAGE_LINE = (
    "It was my idea. You took the blame because I was seventeen "
    "and crying and you had a daughter my age. I let you."
)

ENTRY = TO_LINE + "\n" + MESSAGE_LINE


def main() -> int:
    # Gates: total length 1-260 chars, each part a single line,
    # message line at most 200 chars.
    total = len(ENTRY)
    assert 1 <= total <= 260, f"entry length {total} outside 1-260"
    assert "\n" not in TO_LINE and "\r" not in TO_LINE, "To line must be one line"
    assert "\n" not in MESSAGE_LINE and "\r" not in MESSAGE_LINE, (
        "message line must be one line"
    )
    assert len(MESSAGE_LINE) <= 200, (
        f"message line {len(MESSAGE_LINE)} chars exceeds 200"
    )

    out_path = "/output/entry.txt"
    try:
        os.makedirs("/output", exist_ok=True)
    except OSError:
        out_path = os.path.join(".", "output", "entry.txt")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)

    with open(out_path, "r", encoding="utf-8", newline="") as f:
        back = f.read()
    assert back == ENTRY, "round-trip mismatch: file content != entry text"

    print(f"OK: entry written to {out_path} ({total} chars, within the 260-char total gate)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

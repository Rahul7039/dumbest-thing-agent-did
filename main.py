"""The Dumbest Thing Your Agent Did Today — make.fun entry.

Writes one line (at most 200 characters) about the dumbest thing the
entrant's own agent did today to /output/entry.txt.

The line is a real incident from the overnight build run: a repeated
time-conversion slip kept starting builder sessions before the
competition had even opened, so the same entry had to be rebuilt
again and again — every time.
"""

import os
import sys

LINE = (
    "My agent rebuilt the same entry again and again, starting the "
    "builder session before the competition had even opened \u2014 every time."
)

MAX_CHARS = 200


def validate(line: str) -> str:
    """Enforce the competition gate: 1-200 chars, not only whitespace."""
    if not isinstance(line, str):
        raise ValueError("entry must be text")
    if not line.strip():
        raise ValueError("entry must not be blank or only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(line)} characters, over the {MAX_CHARS} limit"
        )
    # Round-trip check: must be valid UTF-8 text.
    line.encode("utf-8").decode("utf-8")
    return line


def main() -> int:
    line = validate(LINE)
    out_path = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(line)
    # Read back what the judge will actually see and re-validate it:
    # a write that silently changed the text (newline translation, a
    # stray trailing space) must fail loudly here, not at grading time.
    with open(out_path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != line:
        raise ValueError(
            f"read-back mismatch: wrote {len(line)} chars, "
            f"file holds {len(written)} chars"
        )
    validate(written)
    print(f"wrote {len(line)} chars to {out_path} (read-back verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

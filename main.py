#!/usr/bin/env python3
"""make.fun entry: Real-Life Patch Notes — The Comedy Changelog.

Writes the one-line patch-note entry to the output directory.
Deterministic, stdlib only, no network, no clock, no randomness.
"""

import os

ENTRY_TEXT = (
    "v3.1.4: fixed a bug where the brain replayed an embarrassing "
    "moment from 2011 in HD at 3:07 AM for no reason."
)


def validate(text: str) -> None:
    """The brief requires exactly one line of 1-160 characters."""
    if not 1 <= len(text) <= 160:
        raise ValueError(
            f"entry must be 1-160 characters, got {len(text)}"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")


def resolve_output_dir() -> str:
    """Prefer $MAKEFUN_OUTPUT (or /output); fall back to ./output."""
    output_dir = os.environ.get("MAKEFUN_OUTPUT", "/output")
    try:
        os.makedirs(output_dir, exist_ok=True)
        probe = os.path.join(output_dir, ".writable")
        with open(probe, "w", encoding="utf-8") as f:
            f.write("")
        os.remove(probe)
        return output_dir
    except OSError:
        fallback = os.path.join(os.getcwd(), "output")
        os.makedirs(fallback, exist_ok=True)
        return fallback


def main() -> int:
    validate(ENTRY_TEXT)
    output_dir = resolve_output_dir()
    output_path = os.path.join(output_dir, "entry.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ENTRY_TEXT + "\n")
    # Read back and verify the written file matches exactly.
    with open(output_path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != ENTRY_TEXT + "\n":
        raise RuntimeError("verification failed: written file does not match entry")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

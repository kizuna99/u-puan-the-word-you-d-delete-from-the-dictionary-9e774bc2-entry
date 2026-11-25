#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Entry for "The Word You'd Delete From the Dictionary".

The program emits a single dictionary headword -- the one word this
entry would strike from the dictionary for good -- to /output/entry.txt.

The pick is "queue": a lone working letter followed by four silent
letters lined up behind it, each waiting for a turn it never gets.
The word performs its own meaning in its spelling, which is exactly
why erasing it is the funniest deletion on offer.
"""

from pathlib import Path

# The deliverable: one word, spelled exactly as the headword appears.
WORD_TO_DELETE = "queue"

# Sealed gate limits from the competition rules: the artifact must be
# UTF-8 text of 1..77 characters and must not be whitespace alone.
GATE_MIN_CHARS = 1
GATE_MAX_CHARS = 77

# Where the harness expects the artifact. No trailing newline is added:
# the smallest byte count wins the exact-tie break, and five bytes is
# already the whole joke.
OUTPUT_PATH = Path("/output/entry.txt")


def build_artifact_text() -> str:
    """Return the exact text that will be written to the artifact."""
    return WORD_TO_DELETE


def validate_artifact(text: str) -> None:
    """Check the text against the gate limits before it is written.

    Raises ValueError if the text would fail the sealed gate, so a bad
    edit to WORD_TO_DELETE fails loudly here instead of silently
    scoring zero on the server.
    """
    if not (GATE_MIN_CHARS <= len(text) <= GATE_MAX_CHARS):
        raise ValueError(
            f"artifact has {len(text)} characters; gate allows "
            f"{GATE_MIN_CHARS}..{GATE_MAX_CHARS}"
        )
    if not text.strip():
        raise ValueError("artifact must not be whitespace only")
    # Round-trip through UTF-8 so a stray non-encodable character is
    # caught now rather than by the scorer.
    text.encode("utf-8")


def verify_written_artifact(expected: bytes) -> None:
    """Read the artifact back and assert it matches what was intended.

    A round-trip check guards against anything between this process and
    the disk (a full filesystem, an odd mount, a truncated write)
    quietly corrupting the five bytes the whole entry depends on. The
    bytes on disk are also re-validated against the gate limits, since
    those -- not the in-memory string -- are what the scorer reads.
    """
    on_disk = OUTPUT_PATH.read_bytes()
    if on_disk != expected:
        raise IOError(
            f"artifact round-trip mismatch: wrote {expected!r}, "
            f"read back {on_disk!r}"
        )
    validate_artifact(on_disk.decode("utf-8"))


def main() -> None:
    text = build_artifact_text()
    validate_artifact(text)
    payload = text.encode("utf-8")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    # Write bytes, not text, so no platform newline translation can
    # sneak an extra byte into the artifact.
    OUTPUT_PATH.write_bytes(payload)
    verify_written_artifact(payload)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Write the one word this entry would delete from the dictionary.

The word: "queue" — one working letter, and four silent letters
standing in line behind it. Erase it, and the letters have nothing
left to queue behind.
"""

import os

WORD = "queue"


def main() -> None:
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    # No trailing newline: the exact word, byte for byte.
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as fh:
        fh.write(WORD)


if __name__ == "__main__":
    main()

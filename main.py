"""Write the out-of-office reply entry to ``$MAKEFUN_OUTPUT_DIR/entry.txt``.

Python 3 standard library only. Deterministic, no network, no randomness.
The entry is a single out-of-office auto-reply of at most 160 characters,
written as exact UTF-8 bytes with no trailing newline. Only the output file
is ever chmodded (0644); the output directory itself is never touched,
chmodded, or deleted.
"""

import os
import sys

ENTRY_TEXT = (
    "I am on vacation. My replacement is a CAPTCHA. "
    "Please prove you are human to proceed."
)
MAX_LENGTH = 160
OUTPUT_FILENAME = "entry.txt"
DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_MODE = 0o644
ENCODING = "utf-8"


def validate(text):
    """Reject any entry text that breaks the contest gate.

    Raises ValueError when the text is not a string, is empty or
    whitespace-only, is longer than MAX_LENGTH characters, or contains
    any newline character.
    """
    if not isinstance(text, str):
        raise ValueError("entry text must be a string")
    if not text or not text.strip():
        raise ValueError("entry text must not be empty or whitespace-only")
    if len(text) > MAX_LENGTH:
        raise ValueError(
            "entry text is %d characters, over the %d-character limit"
            % (len(text), MAX_LENGTH)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry text must not contain newlines")


def main():
    validate(ENTRY_TEXT)
    payload = ENTRY_TEXT.encode(ENCODING)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_FILENAME)

    # Binary mode so the bytes on disk are exactly the encoded entry text.
    with open(path, "wb") as f:
        f.write(payload)

    # Chmod only the output file, never the output directory itself.
    os.chmod(path, OUTPUT_MODE)
    return 0


if __name__ == "__main__":
    sys.exit(main())

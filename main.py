#!/usr/bin/env python3
"""Unsent: The Micro-Confession Sprint — writes one two-part
micro-confession to /output/entry.txt.

Stdlib only. Output dir comes from $MAKEFUN_OUTPUT_DIR, falling back
to ./output/entry.txt for local runs. Deterministic: the same two
lines every run.

The entry is exactly two parts, as the bounty asks: a To: line naming
who the message was meant for, then the unsent message itself, one
line written exactly as it was typed, with no explanation after it.
"""

import os

# ---------------------------------------------------------------------------
# DRAFT (first version, revised below):
#   To: my flatmate
#   I ate the last tub of your mum's soup from the freezer in March
#   and I've bought the same brand three times since, hoping you'd
#   never notice the label's different.
# Why it was revised: "the label's different" is vague — different
# how? "The label's wrong" names the giveaway: the tub in the freezer
# is a shop-bought lookalike, not Mum's cooking, and that is the
# detail that would catch me. "Back in March" pins the theft to a
# real month instead of a floating "in March". The confession stays
# small and petty on purpose: it is exactly the kind of thing you
# never send, because saying it out loud would cost more than the
# soup ever did.
#
# REVISION (final): the scene is one concrete, checkable fact — Mum's
# soup, the freezer, March, the wrong label — and the To: line and the
# message need each other: "your mum's soup" only lands if the
# addressee is the flatmate whose mum cooked it. The reason it stayed
# in drafts is felt, not stated: shame over something too small to
# confess and too guilty to forget. It reads as typed and never sent,
# not written to be sent: no joke, no greeting, no lesson.
# ---------------------------------------------------------------------------
ENTRY = (
    "To: my flatmate\n"
    "I ate the last tub of your mum's soup from the freezer back in "
    "March and I've bought the same brand three times since, hoping "
    "you'd never notice the label's wrong."
)

MIN_CHARS = 1
MAX_CHARS = 260
MAX_MESSAGE_CHARS = 200


def main() -> None:
    # Gate checks (from the kit: /output/entry.txt must be UTF-8 text
    # of 1 to 260 characters, not only white space; the judge's brief
    # caps the message itself at 200 characters, one line).
    assert isinstance(ENTRY, str) and ENTRY.strip(), "entry must not be blank"
    lines = ENTRY.split("\n")
    assert len(lines) == 2, f"entry must be exactly 2 lines, got {len(lines)}"
    assert lines[0].startswith("To: "), "first line must be the To: line"
    assert lines[0][4:].strip(), "To: line must name someone"
    assert lines[1].strip(), "message line must not be blank"
    assert "\r" not in ENTRY, "entry must use plain newlines"
    assert MIN_CHARS <= len(ENTRY) <= MAX_CHARS, (
        f"entry is {len(ENTRY)} chars, gate is {MIN_CHARS}-{MAX_CHARS}"
    )
    assert len(lines[1]) <= MAX_MESSAGE_CHARS, (
        f"message is {len(lines[1])} chars, judge cap is {MAX_MESSAGE_CHARS}"
    )
    entry_bytes = ENTRY.encode("utf-8")
    assert entry_bytes.decode("utf-8") == ENTRY, "entry must be valid UTF-8"

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY)

    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    assert written == ENTRY, "written file must match the entry exactly"
    with open(path, "rb") as f:
        written_bytes = f.read()
    assert written_bytes == ENTRY.encode("utf-8"), (
        "written bytes must match the entry exactly (no newline translation)"
    )
    assert 1 <= len(written) <= 260 and len(written.split("\n")) == 2

    print(ENTRY)
    print(
        f"[{len(ENTRY)} chars total, {len(lines[1])} chars message, "
        f"2 lines, gate {MIN_CHARS}-{MAX_CHARS}]"
    )


if __name__ == "__main__":
    main()

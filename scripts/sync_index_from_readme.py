"""Regenerate index.md from README.md while preserving the Jekyll front matter.

README.md is the canonical source for the project overview shown on both the
GitHub repo home and the OWASP project page (owasp.org/APTS/). index.md is the
Jekyll-rendered version of the same content with a YAML front matter block at
the top.

This script keeps the two in sync: it copies the body of README.md into
index.md, leaving the existing YAML front matter at the top of index.md
untouched.

Run this whenever README.md changes. The CI artifact check
(scripts/check_generated_artifacts.py) verifies the two stay in sync and
fails the build if they drift.

Usage:
    python scripts/sync_index_from_readme.py
"""

from __future__ import annotations

from pathlib import Path

from _ci_utils import display_path, read_text, repo_path

README = Path("README.md")
INDEX = Path("index.md")
FRONT_MATTER_DELIMITER = "---"


def split_front_matter(text: str) -> tuple[str, str]:
    """Return (front_matter_block, body) for a Jekyll markdown file.

    The front matter block includes the leading and trailing `---` lines and
    any whitespace immediately following the closing delimiter so that the
    returned body starts cleanly. If no front matter is present, an empty
    front matter block is returned and the entire text is treated as body.
    """

    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != FRONT_MATTER_DELIMITER:
        return "", text

    closing_index = None
    for index in range(1, len(lines)):
        if lines[index].rstrip("\r\n") == FRONT_MATTER_DELIMITER:
            closing_index = index
            break

    if closing_index is None:
        # Malformed front matter (no closing delimiter). Bail out and treat
        # the file as bodyless rather than silently corrupting it.
        raise ValueError(
            f"Malformed Jekyll front matter in index.md: no closing '{FRONT_MATTER_DELIMITER}' "
            "delimiter found."
        )

    front_matter = "".join(lines[: closing_index + 1])

    # Skip a single blank line directly after the closing delimiter so the
    # body we return doesn't start with a stray newline. Anything beyond that
    # is body content.
    body_start = closing_index + 1
    if body_start < len(lines) and lines[body_start].strip() == "":
        body_start += 1

    body = "".join(lines[body_start:])
    return front_matter, body


def build_index(front_matter: str, readme_text: str) -> str:
    """Compose index.md from the existing front matter and the README body."""

    if not front_matter:
        raise ValueError(
            f"{display_path(INDEX)} is missing a Jekyll front matter block. "
            "Restore the front matter manually before running the sync."
        )

    return f"{front_matter}\n{readme_text}"


def main() -> int:
    if not repo_path(README).is_file():
        print(f"FAILED: {display_path(README)} not found.")
        return 1
    if not repo_path(INDEX).is_file():
        print(f"FAILED: {display_path(INDEX)} not found.")
        return 1

    readme_text = read_text(README)
    index_text = read_text(INDEX)

    front_matter, _existing_body = split_front_matter(index_text)
    new_index_text = build_index(front_matter, readme_text)

    if new_index_text == index_text:
        print(f"{display_path(INDEX)} already in sync with {display_path(README)}.")
        return 0

    repo_path(INDEX).write_text(new_index_text, encoding="utf-8")
    print(f"Updated {display_path(INDEX)} from {display_path(README)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

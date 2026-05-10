"""Regenerate tab_acknowledgements.md from ACKNOWLEDGEMENTS.md.

ACKNOWLEDGEMENTS.md is the canonical contributor list rendered on the GitHub
repo home. tab_acknowledgements.md is the Jekyll-rendered version shown on the
OWASP project page (owasp.org/APTS/) under the "Acknowledgements" tab.

The Jekyll tab is a subset of ACKNOWLEDGEMENTS.md:
  * The top-level `# Acknowledgements` heading is dropped because Jekyll
    renders the page title from the front matter `title:` field. Including
    the H1 in the body would duplicate it.
  * The "Influences" and "How to Get Listed" sections (last two H2 sections
    in the source) are intentionally excluded from the public tab.
  * Everything else (disclaimer paragraph, Project Lead, Technical Reviewers,
    Contributors) is mirrored verbatim.

Run this whenever ACKNOWLEDGEMENTS.md changes. The CI artifact check
(scripts/check_generated_artifacts.py) verifies the two stay in sync and
fails the build if they drift.

Usage:
    python scripts/sync_tab_acknowledgements_from_acknowledgements.py
"""

from __future__ import annotations

from pathlib import Path

from _ci_utils import display_path, read_text, repo_path

SOURCE = Path("ACKNOWLEDGEMENTS.md")
TARGET = Path("tab_acknowledgements.md")
FRONT_MATTER_DELIMITER = "---"

# H2 section headings (without the leading "## ") whose content should NOT
# appear on the public Jekyll tab. The script truncates the body at the first
# heading whose text matches any entry below.
EXCLUDED_SECTIONS = ("Influences", "How to Get Listed")


def split_front_matter(text: str) -> tuple[str, str]:
    """Return (front_matter_block, body) for a Jekyll markdown file.

    The front matter block includes the leading and trailing `---` lines and
    a single trailing blank line if present. If no front matter is present,
    an empty front matter block is returned and the entire text is body.
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
        raise ValueError(
            f"Malformed Jekyll front matter in {display_path(TARGET)}: "
            f"no closing '{FRONT_MATTER_DELIMITER}' delimiter found."
        )

    front_matter = "".join(lines[: closing_index + 1])

    body_start = closing_index + 1
    if body_start < len(lines) and lines[body_start].strip() == "":
        body_start += 1

    body = "".join(lines[body_start:])
    return front_matter, body


def process_source_body(source_text: str) -> str:
    """Strip the H1 and excluded H2 sections from the source markdown."""

    lines = source_text.splitlines(keepends=True)

    # Drop the leading H1 line if present, plus a single blank line directly
    # after it. Jekyll renders the page title from the front matter, so an
    # in-body H1 would duplicate it on the rendered page.
    start = 0
    if lines and lines[0].lstrip().startswith("# ") and not lines[0].lstrip().startswith("## "):
        start = 1
        if start < len(lines) and lines[start].strip() == "":
            start += 1

    # Truncate at the first H2 heading that matches an excluded section.
    kept: list[str] = []
    for line in lines[start:]:
        stripped = line.lstrip()
        if stripped.startswith("## "):
            heading_text = stripped[3:].strip()
            if heading_text in EXCLUDED_SECTIONS:
                break
        kept.append(line)

    body = "".join(kept).rstrip() + "\n"
    return body


def build_target(front_matter: str, source_text: str) -> str:
    """Compose the target file from existing front matter and processed source."""

    if not front_matter:
        raise ValueError(
            f"{display_path(TARGET)} is missing a Jekyll front matter block. "
            "Restore the front matter manually before running the sync."
        )

    body = process_source_body(source_text)
    return f"{front_matter}\n{body}"


def main() -> int:
    if not repo_path(SOURCE).is_file():
        print(f"FAILED: {display_path(SOURCE)} not found.")
        return 1
    if not repo_path(TARGET).is_file():
        print(f"FAILED: {display_path(TARGET)} not found.")
        return 1

    source_text = read_text(SOURCE)
    target_text = read_text(TARGET)

    front_matter, _existing_body = split_front_matter(target_text)
    new_target_text = build_target(front_matter, source_text)

    if new_target_text == target_text:
        print(f"{display_path(TARGET)} already in sync with {display_path(SOURCE)}.")
        return 0

    repo_path(TARGET).write_text(new_target_text, encoding="utf-8")
    print(f"Updated {display_path(TARGET)} from {display_path(SOURCE)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

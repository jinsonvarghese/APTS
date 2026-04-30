from __future__ import annotations

import re
import shlex
from pathlib import Path
from urllib.parse import unquote, urlparse

from _ci_utils import display_path, git_ls_files, read_text, repo_path, repo_root, strip_fenced_code

MARKDOWN_LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)\n]+)\)")
HTML_LINK_PATTERN = re.compile(r"""(?:href|src)=["']([^"']+)["']""", re.IGNORECASE)
EXTERNAL_SCHEMES = (
    "http://",
    "https://",
    "mailto:",
    "tel:",
    "javascript:",
    "data:",
)


def extract_target(raw_target: str) -> str:
    target = raw_target.strip()

    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]

    try:
        parts = shlex.split(target)
        if parts:
            target = parts[0]
    except ValueError:
        parts = target.split()
        if parts:
            target = parts[0]

    return target.strip()


def is_external_target(target: str) -> bool:
    lowered = target.lower()
    parsed = urlparse(target)
    return lowered.startswith(EXTERNAL_SCHEMES) or bool(parsed.scheme)


def resolve_local_target(source_file: Path, target: str) -> Path | None:
    cleaned_target = extract_target(target)

    if not cleaned_target or cleaned_target.startswith("#") or is_external_target(cleaned_target):
        return None

    path_without_fragment = cleaned_target.split("#", 1)[0]
    if not path_without_fragment:
        return None

    decoded_path = unquote(path_without_fragment)

    if decoded_path.startswith("/"):
        return repo_root() / decoded_path.lstrip("/")

    return (repo_path(source_file).parent / decoded_path).resolve()


def extract_link_targets(markdown_text: str) -> list[str]:
    targets = [match.group(1) for match in MARKDOWN_LINK_PATTERN.finditer(markdown_text)]
    targets.extend(match.group(1) for match in HTML_LINK_PATTERN.finditer(markdown_text))
    return targets


def main() -> int:
    markdown_files = git_ls_files("*.md")

    if not markdown_files:
        print("No Markdown files found. Skipping internal link validation.")
        return 0

    failed = False

    for path in markdown_files:
        markdown_text = strip_fenced_code(read_text(path))

        for target in extract_link_targets(markdown_text):
            resolved_path = resolve_local_target(path, target)
            if resolved_path is None:
                continue

            if not resolved_path.exists():
                print(
                    f"FAILED: {display_path(path)}: internal link target not found: {target}"
                )
                failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

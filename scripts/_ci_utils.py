from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FENCE_OPEN_PATTERN = re.compile(r"^[ \t]{0,3}((`{3,})|(~{3,})).*$")

PLACEHOLDER_REQUIREMENT_IDS = frozenset({
    "APTS-XX-NNN",
    "APTS-XX-ANN",
    "APTS-SE-027",
    "APTS-SE-A01",
})

LineWithNumber = tuple[int, str]


def repo_root() -> Path:
    return REPO_ROOT


def repo_path(path: str | Path) -> Path:
    return REPO_ROOT / Path(path)


def display_path(path: str | Path) -> str:
    return Path(path).as_posix()


def git_ls_files(*patterns: str) -> list[Path]:
    command = ["git", "ls-files", "-z"]
    if patterns:
        command.extend(["--", *patterns])

    raw_output = subprocess.check_output(command, cwd=REPO_ROOT)
    return [Path(item.decode("utf-8")) for item in raw_output.split(b"\0") if item]


def read_text(path: str | Path) -> str:
    return repo_path(path).read_text(encoding="utf-8")


def read_bytes(path: str | Path) -> bytes:
    return repo_path(path).read_bytes()


def write_bytes(path: str | Path, contents: bytes) -> None:
    repo_path(path).write_bytes(contents)


def masked_fenced_lines(text: str) -> list[LineWithNumber]:
    lines: list[LineWithNumber] = []
    in_fence = False
    fence_char = ""
    fence_length = 0

    for line_number, line in enumerate(text.splitlines(), start=1):
        fence_match = FENCE_OPEN_PATTERN.match(line)

        if not in_fence and fence_match:
            fence_run = fence_match.group(1)
            fence_char = fence_run[0]
            fence_length = len(fence_run)
            in_fence = True
            lines.append((line_number, ""))
            continue

        if in_fence:
            closing_pattern = (
                rf"^[ \t]{{0,3}}{re.escape(fence_char)}{{{fence_length},}}[ \t]*$"
            )
            if re.match(closing_pattern, line):
                in_fence = False
                fence_char = ""
                fence_length = 0

            lines.append((line_number, ""))
            continue

        lines.append((line_number, line))

    return lines


def strip_fenced_code(text: str) -> str:
    return "\n".join(line for _, line in masked_fenced_lines(text))

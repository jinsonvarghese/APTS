from __future__ import annotations

import difflib
import json
import subprocess
import sys
from pathlib import Path

from _ci_utils import display_path, read_bytes, repo_path, repo_root, write_bytes

EXPORT_SCRIPT = Path("scripts/export_requirements.py")
SYNC_INDEX_SCRIPT = Path("scripts/sync_index_from_readme.py")
SYNC_TAB_ACKNOWLEDGEMENTS_SCRIPT = Path("scripts/sync_tab_acknowledgements_from_md.py")
REQUIREMENTS_JSON = Path("standard/apts_requirements.json")
SCHEMA_JSON = Path("standard/apts_requirements_schema.json")
README_MD = Path("README.md")
INDEX_MD = Path("index.md")
ACKNOWLEDGEMENTS_MD = Path("ACKNOWLEDGEMENTS.md")
TAB_ACKNOWLEDGEMENTS_MD = Path("tab_acknowledgements.md")
FIXED_TIMESTAMP = "1970-01-01T00:00:00Z"


def normalized_json_lines(contents: bytes, *, normalize_last_updated: bool) -> list[str]:
    data = json.loads(contents.decode("utf-8"))

    if normalize_last_updated and isinstance(data, dict) and "last_updated" in data:
        data["last_updated"] = FIXED_TIMESTAMP

    return (json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n").splitlines()


def raw_text_lines(contents: bytes) -> list[str]:
    return contents.decode("utf-8").splitlines()


def print_diff(
    message: str,
    *,
    expected_lines: list[str],
    actual_lines: list[str],
    expected_name: str,
    actual_name: str,
) -> None:
    print(message)
    for line in difflib.unified_diff(
        expected_lines,
        actual_lines,
        fromfile=expected_name,
        tofile=actual_name,
        lineterm="",
    ):
        print(line)


def restore_original_files(original_contents: dict[Path, bytes]) -> list[str]:
    restore_errors: list[str] = []

    for path, contents in original_contents.items():
        try:
            write_bytes(path, contents)
        except Exception as exc:
            restore_errors.append(
                f"FAILED: Could not restore {display_path(path)} after artifact check: {exc}"
            )

    return restore_errors


def main() -> int:
    if not repo_path(EXPORT_SCRIPT).is_file():
        print("No export script found. Skipping generated artifact check.")
        return 0

    required_files = (REQUIREMENTS_JSON, SCHEMA_JSON)
    for path in required_files:
        if not repo_path(path).is_file():
            print(f"FAILED: Expected generated artifact is missing: {display_path(path)}")
            return 1

    original_contents = {path: read_bytes(path) for path in required_files}
    exit_code = 0

    try:
        subprocess.run(
            [sys.executable, str(repo_path(EXPORT_SCRIPT))],
            cwd=repo_root(),
            check=True,
        )

        regenerated_requirements = read_bytes(REQUIREMENTS_JSON)
        regenerated_schema = read_bytes(SCHEMA_JSON)

        expected_requirements = normalized_json_lines(
            original_contents[REQUIREMENTS_JSON],
            normalize_last_updated=True,
        )
        actual_requirements = normalized_json_lines(
            regenerated_requirements,
            normalize_last_updated=True,
        )

        if expected_requirements != actual_requirements:
            print_diff(
                "FAILED: Generated requirements JSON is out of date after normalizing last_updated.",
                expected_lines=expected_requirements,
                actual_lines=actual_requirements,
                expected_name="committed requirements",
                actual_name="regenerated requirements",
            )
            exit_code = 1

        expected_schema = raw_text_lines(original_contents[SCHEMA_JSON])
        actual_schema = raw_text_lines(regenerated_schema)

        if expected_schema != actual_schema:
            print_diff(
                "FAILED: Generated schema JSON is out of date.",
                expected_lines=expected_schema,
                actual_lines=actual_schema,
                expected_name="committed schema",
                actual_name="regenerated schema",
            )
            exit_code = 1

    except subprocess.CalledProcessError as exc:
        print(f"FAILED: export_requirements.py exited with status {exc.returncode}.")
        exit_code = 1
    except Exception as exc:
        print(f"FAILED: Generated artifact check could not complete: {exc}")
        exit_code = 1
    finally:
        restore_errors = restore_original_files(original_contents)
        if restore_errors:
            for message in restore_errors:
                print(message)
            exit_code = 1

    index_check_exit_code = check_index_in_sync_with_readme()
    if index_check_exit_code != 0:
        exit_code = index_check_exit_code

    tab_check_exit_code = check_tab_acknowledgements_in_sync()
    if tab_check_exit_code != 0:
        exit_code = tab_check_exit_code

    return exit_code


def check_tab_acknowledgements_in_sync() -> int:
    """Verify tab_acknowledgements.md matches the ACKNOWLEDGEMENTS.md body
    after the H1 and the "Influences" / "How to Get Listed" sections are
    stripped.

    The sync_tab_acknowledgements_from_md.py script regenerates
    tab_acknowledgements.md from ACKNOWLEDGEMENTS.md. This check fails the
    build if the two have drifted.
    """

    if not repo_path(SYNC_TAB_ACKNOWLEDGEMENTS_SCRIPT).is_file():
        print(
            f"No sync script found at {display_path(SYNC_TAB_ACKNOWLEDGEMENTS_SCRIPT)}. "
            "Skipping tab_acknowledgements.md / ACKNOWLEDGEMENTS.md sync check."
        )
        return 0

    if (
        not repo_path(TAB_ACKNOWLEDGEMENTS_MD).is_file()
        or not repo_path(ACKNOWLEDGEMENTS_MD).is_file()
    ):
        print(
            "FAILED: Expected ACKNOWLEDGEMENTS.md and tab_acknowledgements.md "
            "to both exist for the sync check."
        )
        return 1

    original_tab_contents = read_bytes(TAB_ACKNOWLEDGEMENTS_MD)
    exit_code = 0

    try:
        subprocess.run(
            [sys.executable, str(repo_path(SYNC_TAB_ACKNOWLEDGEMENTS_SCRIPT))],
            cwd=repo_root(),
            check=True,
        )

        regenerated_tab = read_bytes(TAB_ACKNOWLEDGEMENTS_MD)
        expected_lines = raw_text_lines(original_tab_contents)
        actual_lines = raw_text_lines(regenerated_tab)

        if expected_lines != actual_lines:
            print_diff(
                "FAILED: tab_acknowledgements.md is out of sync with "
                "ACKNOWLEDGEMENTS.md. Run "
                "scripts/sync_tab_acknowledgements_from_md.py to regenerate it.",
                expected_lines=expected_lines,
                actual_lines=actual_lines,
                expected_name="committed tab_acknowledgements.md",
                actual_name="regenerated tab_acknowledgements.md",
            )
            exit_code = 1
    except subprocess.CalledProcessError as exc:
        print(
            f"FAILED: sync_tab_acknowledgements_from_md.py exited with status {exc.returncode}."
        )
        exit_code = 1
    except Exception as exc:
        print(
            f"FAILED: tab_acknowledgements.md / ACKNOWLEDGEMENTS.md sync check could not complete: {exc}"
        )
        exit_code = 1
    finally:
        restore_errors = restore_original_files(
            {TAB_ACKNOWLEDGEMENTS_MD: original_tab_contents}
        )
        if restore_errors:
            for message in restore_errors:
                print(message)
            exit_code = 1

    return exit_code


def check_index_in_sync_with_readme() -> int:
    """Verify index.md matches the README.md body under the Jekyll front matter.

    README.md is the canonical source for the project overview; index.md
    is the Jekyll-rendered version with a YAML front matter block prepended.
    The sync_index_from_readme.py script regenerates index.md from README.md.
    This check fails the build if the two have drifted.
    """

    if not repo_path(SYNC_INDEX_SCRIPT).is_file():
        print(
            f"No sync script found at {display_path(SYNC_INDEX_SCRIPT)}. "
            "Skipping index.md / README.md sync check."
        )
        return 0

    if not repo_path(INDEX_MD).is_file() or not repo_path(README_MD).is_file():
        print(
            "FAILED: Expected README.md and index.md to both exist for the sync check."
        )
        return 1

    original_index_contents = read_bytes(INDEX_MD)
    exit_code = 0

    try:
        subprocess.run(
            [sys.executable, str(repo_path(SYNC_INDEX_SCRIPT))],
            cwd=repo_root(),
            check=True,
        )

        regenerated_index = read_bytes(INDEX_MD)
        expected_lines = raw_text_lines(original_index_contents)
        actual_lines = raw_text_lines(regenerated_index)

        if expected_lines != actual_lines:
            print_diff(
                "FAILED: index.md is out of sync with README.md. "
                "Run scripts/sync_index_from_readme.py to regenerate it.",
                expected_lines=expected_lines,
                actual_lines=actual_lines,
                expected_name="committed index.md",
                actual_name="regenerated index.md",
            )
            exit_code = 1
    except subprocess.CalledProcessError as exc:
        print(
            f"FAILED: sync_index_from_readme.py exited with status {exc.returncode}."
        )
        exit_code = 1
    except Exception as exc:
        print(f"FAILED: index.md / README.md sync check could not complete: {exc}")
        exit_code = 1
    finally:
        restore_errors = restore_original_files({INDEX_MD: original_index_contents})
        if restore_errors:
            for message in restore_errors:
                print(message)
            exit_code = 1

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())

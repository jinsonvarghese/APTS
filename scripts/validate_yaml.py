from __future__ import annotations

import yaml

from _ci_utils import display_path, git_ls_files, read_text


def main() -> int:
    yaml_files = git_ls_files("*.yml", "*.yaml")

    if not yaml_files:
        print("No YAML files found. Skipping YAML validation.")
        return 0

    failed = False

    for path in yaml_files:
        print(f"Validating YAML: {display_path(path)}")

        try:
            yaml.safe_load(read_text(path))
        except Exception as exc:
            print(f"FAILED: {display_path(path)}: {exc}")
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

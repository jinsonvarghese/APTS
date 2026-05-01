from __future__ import annotations

import re
import sys
from pathlib import Path

from _ci_utils import (
    PLACEHOLDER_REQUIREMENT_IDS,
    display_path,
    git_ls_files,
    read_text,
)

def main() -> int:
    valid_reqs = set()
    req_pattern = re.compile(r"APTS-[A-Z]{2}-[A-Z0-9]{3}")
    
    md_files = git_ls_files("*.md")
    standard_md_files = [f for f in md_files if Path(f).parts[0] == "standard"]
    
    for md_file in standard_md_files:
        content = read_text(md_file)
        
        # Match definitions like "## APTS-RP-001: Title"
        defs = re.findall(r"^#{2,4}\s+(APTS-[A-Z]{2}-[A-Z0-9]{3}):", content, re.MULTILINE)
        valid_reqs.update(defs)
        
        # Match table definitions like "| APTS-RP-001 |"
        table_defs = re.findall(r"\|\s*(APTS-[A-Z]{2}-[A-Z0-9]{3})\s*\|", content)
        valid_reqs.update(table_defs)

    if not valid_reqs:
        print("Error: No requirements found to validate against.", file=sys.stderr)
        return 1

    failed = False
    for md_file in md_files:
        content = read_text(md_file)
        lines = content.splitlines()
        
        for i, line in enumerate(lines):
            refs = req_pattern.findall(line)
            for ref in refs:
                if ref in PLACEHOLDER_REQUIREMENT_IDS:
                    continue
                if ref not in valid_reqs:
                    print(f"Error in {display_path(md_file)}:{i+1}")
                    print(f"  Invalid cross-reference: {ref} is not a known requirement.")
                    failed = True

    if failed:
        print("Cross-reference validation failed.", file=sys.stderr)
        return 1
    
    print(f"Successfully validated cross-references against {len(valid_reqs)} known requirements.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

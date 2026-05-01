import os
import re
import sys
from pathlib import Path

def main():
    root_dir = Path(__file__).resolve().parent.parent
    standard_dir = root_dir / 'standard'
    
    if not standard_dir.exists():
        print(f"Error: {standard_dir} not found.", file=sys.stderr)
        sys.exit(1)

    valid_reqs = set()
    req_pattern = re.compile(r'APTS-[A-Z]{2}-[0-9A-Z]{3}')
    
    for md_file in standard_dir.rglob('*.md'):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Match definitions like "## APTS-RP-001: Title"
            defs = re.findall(r'^#{2,4}\s+(APTS-[A-Z]{2}-[0-9A-Z]{3}):', content, re.MULTILINE)
            valid_reqs.update(defs)
            
            # Match table definitions like "| APTS-RP-001 |"
            table_defs = re.findall(r'\|\s*(APTS-[A-Z]{2}-[0-9A-Z]{3})\s*\|', content)
            valid_reqs.update(table_defs)

    if not valid_reqs:
        print("Error: No requirements found to validate against.", file=sys.stderr)
        sys.exit(1)

    failed = False
    for md_file in standard_dir.rglob('*.md'):
        with open(md_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for i, line in enumerate(lines):
            if '> **See also:**' in line:
                refs = req_pattern.findall(line)
                for ref in refs:
                    if ref not in valid_reqs:
                        print(f"Error in {md_file.relative_to(root_dir)}:{i+1}")
                        print(f"  Invalid cross-reference: {ref} is not a known requirement.")
                        failed = True

    if failed:
        print("Cross-reference validation failed.", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"Successfully validated cross-references against {len(valid_reqs)} known requirements.")
        sys.exit(0)

if __name__ == '__main__':
    main()

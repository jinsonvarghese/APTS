import os
import json
import re
from datetime import datetime, timezone

SCHEMA = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["requirements", "version", "source", "last_updated"],
  "properties": {
    "version": { "type": "string", "enum": ["0.1.0"] },
    "source": { "type": "string" },
    "last_updated": { "type": "string" },
    "requirements": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "id",
          "domain",
          "tier",
          "classification",
          "title"
        ],
        "properties": {
          "id": { "type": "string", "pattern": "^APTS-[A-Z]+-\\d+$" },
          "domain": { 
            "type": "string",
            "enum": [
              "Scope Enforcement",
              "Safety Controls",
              "Human Oversight",
              "Graduated Autonomy",
              "Auditability",
              "Manipulation Resistance",
              "Supply Chain Trust",
              "Reporting"
            ]
          },
          "tier": { 
            "type": "integer",
            "enum": [1, 2, 3]
          },
          "classification": { 
            "type": "string",
            "enum": ["MUST", "SHOULD"]
          },
          "title": { "type": "string" }
        },
        "additionalProperties": False
      }
    }
  }
}

# Constants
STANDARD_DIR = "standard"
OUTPUT_DIR = "standard"
OUTPUT_JSON = os.path.join(OUTPUT_DIR, "apts_requirements.json")
OUTPUT_SCHEMA = os.path.join(OUTPUT_DIR, "apts_requirements_schema.json")
SCHEMA_VERSION = "0.1.0"
SOURCE = "OWASP Autonomous Penetration Testing Standard"

def get_domain_dirs():
    domain_dirs = {}
    if not os.path.exists(STANDARD_DIR):
        return domain_dirs
        
    for item in os.listdir(STANDARD_DIR):
        if os.path.isdir(os.path.join(STANDARD_DIR, item)):
            match = re.match(r'^\d+_(.*)$', item)
            if match:
                domain_name = match.group(1).replace('_', ' ')
                domain_dirs[item] = domain_name
    
    # Sort by the numeric prefix
    return dict(sorted(domain_dirs.items(), key=lambda x: int(x[0].split('_')[0])))


def export_all():
    requirements = []
    
    # | APTS-SC-001 | Impact Classification and CIA Scoring | MUST \| Tier 1 |
    # or with extra columns: | APTS-AL-001 | Single Technique Execution | MUST \| Tier 1 | L1 |
    pattern = re.compile(r'^\|\s*(APTS-[A-Z]+-\d+)\s*\|\s*(.*?)\s*\|\s*(MUST|SHOULD)\s*\\?\|\s*Tier\s*(\d+)\s*\|.*$')
    
    for dir_name, domain_name in get_domain_dirs().items():
        readme_path = os.path.join(STANDARD_DIR, dir_name, "README.md")
        if not os.path.exists(readme_path):
            print(f"Warning: {readme_path} not found.")
            continue
            
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            match = pattern.match(line)
            if match:
                req_id, title, classification, tier = match.groups()
                requirements.append({
                    "id": req_id,
                    "domain": domain_name,
                    "tier": int(tier),
                    "classification": classification,
                    "title": title
                })
                
    output_data = {
        "version": SCHEMA_VERSION,
        "source": SOURCE,
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "requirements": requirements
    }
    
    # Export requirements JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)
        
    print(f"Successfully generated {OUTPUT_JSON} with {len(requirements)} requirements.")

    # Update schema domain enum dynamically
    SCHEMA["properties"]["requirements"]["items"]["properties"]["domain"]["enum"] = list(get_domain_dirs().values())

    # Export schema JSON
    with open(OUTPUT_SCHEMA, "w", encoding="utf-8") as f:
        json.dump(SCHEMA, f, indent=2)
        
    print(f"Successfully generated {OUTPUT_SCHEMA}.")

if __name__ == "__main__":
    export_all()

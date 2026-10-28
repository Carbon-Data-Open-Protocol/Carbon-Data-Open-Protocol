"""
Validate every example in examples/ against its CDOP schema.

Usage:
    python scripts/validate_examples.py

Exits with code 1 if an example is invalid or has no schema mapped below.

Requires:
    pip install jsonschema
"""

import pathlib
import sys

from validate import validate

ROOT = pathlib.Path(__file__).parent.parent
EXAMPLES_DIR = ROOT / "examples"
SCHEMA_DIR = ROOT / "json_schema"

# Example file name -> schema file name
EXAMPLE_SCHEMAS = {
    "co_benefits.json": "Co_Benefits.schema.json",
    "crediting_period.json": "Crediting_Period.schema.json",
    "disclosures.json": "Disclosures.schema.json",
    "durability_permanence.json": "Durability_Permanence.schema.json",
    "estimations.json": "Estimations.schema.json",
    "full_list.json": "Full_List.schema.json",
    "issuances.json": "Issuances.schema.json",
    "location_details.json": "Location_Details.schema.json",
    "project_approach_and_details.json": "Project_Approach_Details.schema.json",
    "project_finance.json": "Project_Finance.schema.json",
    "unit_description.json": "Unit_Description.schema.json",
}


def main() -> None:
    ok = True
    for example in sorted(EXAMPLES_DIR.glob("*.json")):
        schema_name = EXAMPLE_SCHEMAS.get(example.name)
        if schema_name is None:
            print(f"ERROR: No schema mapped for '{example}'. Add it to EXAMPLE_SCHEMAS in {pathlib.Path(__file__).name}.")
            ok = False
            continue
        ok = validate(example, SCHEMA_DIR / schema_name) and ok
        print()

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

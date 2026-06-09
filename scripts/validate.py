"""
Validate a JSON data file against a CDOP schema, or compare a schema file
against the canonical CDOP schema.

Usage:
    python scripts/validate.py <data_file> --schema <schema_file>
    python scripts/validate.py <schema_file> --compare --schema <canonical_schema>

Examples:
    # Validate data against a schema
    python scripts/validate.py my_data.json --schema json_schema/Issuances.schema.json

    # Compare a custom schema against the canonical CDOP schema
    python scripts/validate.py my_schema.json --compare --schema json_schema/Disclosures.schema.json

Requires:
    pip install jsonschema
"""

import argparse
import json
import pathlib
import sys

SCHEMA_DIR = pathlib.Path(__file__).parent.parent / "json_schema"

# Fields considered cosmetic — ignored during structural comparison
_COSMETIC_KEYS = {"description", "$id", "$schema", "title", "examples", "x-cdop-field-id"}


def load_json(path: pathlib.Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: '{path}' is not valid JSON — {exc}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# Data validation
# ---------------------------------------------------------------------------

def validate(data_path: pathlib.Path, schema_path: pathlib.Path) -> bool:
    try:
        import jsonschema
        from jsonschema import Draft202012Validator
    except ImportError:
        print("ERROR: 'jsonschema' package is not installed.")
        print("       Run:  pip install jsonschema")
        sys.exit(1)

    data = load_json(data_path)
    schema = load_json(schema_path)

    # Build a registry so $ref paths inside the schema directory resolve correctly
    try:
        from referencing import Registry, Resource
        from referencing.jsonschema import DRAFT202012

        from urllib.parse import unquote, urlparse
        from urllib.request import url2pathname

        def _load_resource(uri: str):
            parsed = urlparse(uri)
            if parsed.scheme == "file":
                path = pathlib.Path(url2pathname(unquote(parsed.path)))
            else:
                path = (schema_path.parent / uri).resolve()

            if path.exists():
                return Resource.from_contents(load_json(path), default_specification=DRAFT202012)
            raise FileNotFoundError(f"Cannot resolve: {uri} (resolved to {path})")
        registry = Registry(retrieve=_load_resource)
        validator = Draft202012Validator(schema, registry=registry)
    except ImportError:
        base_uri = schema_path.resolve().as_uri()
        resolver = jsonschema.RefResolver(base_uri=base_uri, referrer=schema)
        validator = Draft202012Validator(schema, resolver=resolver)

    errors = sorted(
        validator.iter_errors(data),
        key=lambda e: "/".join(str(p) for p in e.absolute_path),
    )

    if not errors:
        print(f"OK  '{data_path}' is valid against '{schema_path.name}'.")
        return True

    print(f"FAIL  '{data_path}' has {len(errors)} validation error(s) against '{schema_path.name}':\n")
    for i, error in enumerate(errors, 1):
        path = " → ".join(str(p) for p in error.absolute_path) or "(root)"
        print(f"  [{i}] {path}")
        print(f"       {error.message}\n")
    return False


# ---------------------------------------------------------------------------
# Schema comparison
# ---------------------------------------------------------------------------

def _structural_keys(schema_node: dict) -> dict:
    """Return a copy of a schema node with cosmetic keys removed."""
    return {
        k: v
        for k, v in schema_node.items()
        if k not in _COSMETIC_KEYS and not k.startswith("x-cdop-")
    }


def _diff_schemas(user: object, canonical: object, path: str, diffs: list[str]) -> None:
    """Recursively compare two schema nodes and append human-readable differences."""
    if isinstance(canonical, dict) and isinstance(user, dict):
        c = _structural_keys(canonical)
        u = _structural_keys(user)

        for key in sorted(c.keys() - u.keys()):
            diffs.append(f"MISSING   {path}.{key}  (present in canonical schema)")

        for key in sorted(u.keys() - c.keys()):
            diffs.append(f"EXTRA     {path}.{key}  (not in canonical schema)")

        for key in sorted(c.keys() & u.keys()):
            _diff_schemas(u[key], c[key], f"{path}.{key}", diffs)

    elif isinstance(canonical, list) and isinstance(user, list):
        # For 'required' arrays: compare as sets (order doesn't matter)
        if all(isinstance(x, str) for x in canonical + user):
            missing = sorted(set(canonical) - set(user))
            extra = sorted(set(user) - set(canonical))
            if missing:
                diffs.append(f"MISSING   {path}  values: {missing}")
            if extra:
                diffs.append(f"EXTRA     {path}  values: {extra}")
        else:
            if user != canonical:
                diffs.append(f"CHANGED   {path}  expected {canonical!r}, got {user!r}")

    else:
        if user != canonical:
            diffs.append(f"CHANGED   {path}  expected {canonical!r}, got {user!r}")


def compare(user_schema_path: pathlib.Path, canonical_path: pathlib.Path) -> bool:
    user_schema = load_json(user_schema_path)
    canonical = load_json(canonical_path)

    if not isinstance(user_schema, dict) or not isinstance(canonical, dict):
        print("ERROR: Both files must be JSON objects.")
        return False

    diffs: list[str] = []
    _diff_schemas(user_schema, canonical, "(root)", diffs)

    if not diffs:
        print(f"OK  '{user_schema_path}' matches the canonical '{canonical_path.name}' structurally.")
        return True

    print(
        f"DIFF  '{user_schema_path}' differs from canonical '{canonical_path.name}'"
        f" — {len(diffs)} structural difference(s):\n"
    )
    for d in diffs:
        print(f"  {d}")
    print()
    return False


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Validate a JSON data file against a CDOP schema, "
            "or compare a schema file against the canonical CDOP schema."
        )
    )
    parser.add_argument("data_file", help="Path to the JSON data or schema file")
    parser.add_argument(
        "--schema",
        required=True,
        help="Path to a CDOP schema file.",
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help=(
            "Compare the given file as a schema against the canonical CDOP schema "
            "instead of validating it as data."
        ),
    )
    args = parser.parse_args()

    input_path = pathlib.Path(args.data_file)
    if not input_path.exists():
        print(f"ERROR: File not found: '{input_path}'")
        sys.exit(1)

    schema_path = pathlib.Path(args.schema)
    if not schema_path.exists():
        print(f"ERROR: Schema file not found: '{schema_path}'")
        print(f"       Available schemas in '{SCHEMA_DIR}':")
        for s in sorted(SCHEMA_DIR.glob("*.schema.json")):
            print(f"         {s}")
        sys.exit(1)

    if args.compare:
        ok = compare(input_path, schema_path)
    else:
        ok = validate(input_path, schema_path)

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

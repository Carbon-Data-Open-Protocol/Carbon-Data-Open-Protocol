from pathlib import Path
import json
import re
from openpyxl import load_workbook


# Current Mapping
'''
associated_entity → object
field_name → property
definition → description
datatype → type
cardinality → scalar vs array
required_optional → required fields

'''


INPUT_FILE = "docs/CDOP_SCHEMA.xlsx"
OUTPUT_DIR = "json_schema"

JSON_SCHEMA_VERSION = "https://json-schema.org/draft/2020-12/schema"


TYPE_MAP = {
    "string": "string",
    "str": "string",
    "text": "string",
    "enum": "string",
    "integer": "integer",
    "int": "integer",
    "number": "number",
    "float": "number",
    "decimal": "number",
    "boolean": "boolean",
    "bool": "boolean",
    "date": "string",
    "datetime": "string",
}


FORMAT_MAP = {
    "date": "date",
    "datetime": "date-time",
}


def normalize_header(value):
    if value is None:
        return ""
    value = str(value).strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def clean_value(value):
    if value is None:
        return None

    if isinstance(value, str):
        value = value.strip()
        return value or None

    return value


def safe_filename(value):
    value = str(value).strip()
    value = re.sub(r"[^A-Za-z0-9_-]+", "_", value)
    return value.strip("_") or "schema"


def normalize_schema_key(value):
    if value is None:
        return ""

    value = str(value).strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def map_type(datatype):
    if datatype is None:
        return "string"

    key = str(datatype).strip().lower()
    return TYPE_MAP.get(key, "string")


def map_format(datatype):
    if datatype is None:
        return None

    key = str(datatype).strip().lower()
    return FORMAT_MAP.get(key)


def parse_enum_values(value):
    """
    Optional hook for a future Excel column named enum_values.

    Supports:
    - USA|CAN|MEX
    - USA, CAN, MEX
    - USA; CAN; MEX
    """
    if not value:
        return None

    raw = str(value).strip()

    if "|" in raw:
        parts = raw.split("|")
    elif ";" in raw:
        parts = raw.split(";")
    else:
        parts = raw.split(",")

    values = [part.strip() for part in parts if part.strip()]
    return values or None


def parse_cardinality(cardinality):
    """
    Converts cardinality values into array/scalar behavior.

    Examples:
    1      → scalar, required handled separately
    0..1   → scalar, optional handled separately
    1..*   → array, minItems 1
    0..*   → array
    2..*   → array, minItems 2
    1..5   → array, minItems 1, maxItems 5
    """
    if cardinality is None:
        return {
            "is_array": False,
            "min_items": None,
            "max_items": None,
        }

    value = str(cardinality).strip()

    if ".." not in value:
        return {
            "is_array": False,
            "min_items": None,
            "max_items": None,
        }

    lower, upper = [part.strip() for part in value.split("..", 1)]

    min_items = int(lower) if lower.isdigit() else None
    max_items = None if upper == "*" else int(upper) if upper.isdigit() else None

    is_array = upper == "*" or upper.isdigit() and int(upper) > 1

    return {
        "is_array": is_array,
        "min_items": min_items,
        "max_items": max_items,
    }


def is_required(value):
    if value is None:
        return False

    return str(value).strip().lower() in {
        "required",
        "yes",
        "y",
        "true",
        "1",
    }


def add_custom_annotations(field_schema, record):
    """
    Preserve governance metadata as non-validation annotations.

    JSON Schema allows extension keywords. Prefixing with x-cdop-
    makes it clear these are custom project-specific annotations.
    """
    annotation_fields = {
        "field_id": "x-cdop-field-id",
        "pre_issuance_inclusion": "x-cdop-pre-issuance-inclusion",
        "cardinality": "x-cdop-cardinality",
        "data_source": "x-cdop-data-source",
        "mutability": "x-cdop-mutability",
        "public_private": "x-cdop-public-private",
        "schema": "x-cdop-schema",
    }

    for source_key, target_key in annotation_fields.items():
        value = record.get(source_key)
        if value is not None:
            field_schema[target_key] = value


def build_base_field_schema(record):
    datatype = record.get("datatype")
    definition = record.get("definition")

    field_schema = {
        "type": map_type(datatype)
    }

    json_format = map_format(datatype)
    if json_format:
        field_schema["format"] = json_format

    if definition:
        field_schema["description"] = definition

    datatype_key = str(datatype).strip().lower() if datatype else None

    if datatype_key == "enum":
        field_schema["type"] = "string"

        enum_values = parse_enum_values(record.get("enum_values"))
        if enum_values:
            field_schema["enum"] = enum_values

    add_custom_annotations(field_schema, record)

    return field_schema


def build_field_schema(record):
    base_schema = build_base_field_schema(record)

    cardinality_info = parse_cardinality(record.get("cardinality"))

    if cardinality_info["is_array"]:
        array_schema = {
            "type": "array",
            "items": base_schema,
        }

        if cardinality_info["min_items"] is not None:
            array_schema["minItems"] = cardinality_info["min_items"]

        if cardinality_info["max_items"] is not None:
            array_schema["maxItems"] = cardinality_info["max_items"]

        return array_schema

    return base_schema


def register_normalized_key(seen_keys, normalized_key, original_value):
    existing_value = seen_keys.get(normalized_key)

    if existing_value is None:
        seen_keys[normalized_key] = original_value
    return existing_value


def worksheet_to_json_schema(ws):
    rows = list(ws.iter_rows(values_only=True))

    if not rows:
        return None

    headers = [normalize_header(header) for header in rows[0]]

    required_columns = {
        "associated_entity",
        "field_name",
        "datatype",
    }

    missing = required_columns - set(headers)
    if missing:
        raise ValueError(
            f"Sheet '{ws.title}' is missing required columns: {sorted(missing)}"
        )

    schema = {
        "$schema": JSON_SCHEMA_VERSION,
        "$id": f"{safe_filename(ws.title)}.schema.json",
        "title": ws.title,
        "type": "object",
        "additionalProperties": False,
        "properties": {},
        "required": [],
    }

    required_by_entity = {}
    entity_name_map = {}
    field_name_maps_by_entity = {}

    for row in rows[1:]:
        record = {
            headers[i]: clean_value(row[i])
            for i in range(min(len(headers), len(row)))
            if headers[i]
        }

        associated_entity = record.get("associated_entity")
        field_name = record.get("field_name")

        if not associated_entity or not field_name:
            continue

        associated_entity = str(associated_entity).strip()
        field_name = str(field_name).strip()

        entity_key = normalize_schema_key(associated_entity)
        field_key = normalize_schema_key(field_name)

        if not entity_key:
            raise ValueError(
                f"Sheet '{ws.title}' has an associated_entity value that cannot be "
                f"normalized into a JSON property name: '{associated_entity}'."
            )

        if not field_key:
            raise ValueError(
                f"Sheet '{ws.title}' has a field_name value that cannot be "
                f"normalized into a JSON property name: '{field_name}'."
            )

        register_normalized_key(
            entity_name_map,
            entity_key,
            associated_entity,
        )

        if entity_key not in schema["properties"]:
            schema["properties"][entity_key] = {
                "type": "object",
                "additionalProperties": False,
                "properties": {},
                "required": [],
            }
            required_by_entity[entity_key] = set()
            field_name_maps_by_entity[entity_key] = {}

        register_normalized_key(
            field_name_maps_by_entity[entity_key],
            field_key,
            field_name,
        )

        schema["properties"][entity_key]["properties"][field_key] = build_field_schema(record)

        if is_required(record.get("required_optional")):
            required_by_entity[entity_key].add(field_key)

    for entity_key, required_fields in required_by_entity.items():
        schema["properties"][entity_key]["required"] = sorted(required_fields)

    schema["required"] = sorted(schema["properties"].keys())

    return schema


def convert_workbook(input_file=INPUT_FILE, output_dir=OUTPUT_DIR):
    input_path = Path(input_file)
    output_path = Path(output_dir)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    output_path.mkdir(parents=True, exist_ok=True)

    wb = load_workbook(input_path, data_only=True)

    for ws in wb.worksheets:
        schema = worksheet_to_json_schema(ws)

        if schema is None:
            continue

        output_file = output_path / f"{safe_filename(ws.title)}.schema.json"

        with output_file.open("w", encoding="utf-8") as f:
            json.dump(schema, f, indent=2, ensure_ascii=False)

        print(f"Wrote {output_file}")


if __name__ == "__main__":
    convert_workbook()

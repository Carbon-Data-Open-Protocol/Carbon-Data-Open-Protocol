# CDOP JSON Schema Migration Guide

## Purpose

As of May 26, 2026, the supported CDOP JSON Schema files are the generated schemas under `json_schema/`:

- `Location_Details.schema.json`
- `Project_Approach_Details.schema.json`
- `Issuances.schema.json`
- `Disclosures.schema.json`
- `Unit_Description.schema.json`
- `Crediting_Period.schema.json`
- `Estimations.schema.json`
- `Co-Benefits.schema.json`
- `Durability_Permanence.schema.json`
- `Project_Finance.schema.json`
- `Full_List.schema.json`

Only `Location_Details`, `Project_Approach_Details`, `Issuances`, and `Disclosures` have a legacy counterpart under `json_schema_legacy/`; the remaining generated schemas (`Unit_Description`, `Crediting_Period`, `Estimations`, `Co-Benefits`, `Durability_Permanence`, `Project_Finance`) are new additions with no legacy equivalent, and `Full_List` is the union of all supported schemas.

Legacy schemas remain under `json_schema_legacy/` for reference, but end users should update validation and submission workflows to align with the standardized schemas in `json_schema/`.

This guide focuses on what existing users need to change in:

- payload shape and field naming
- schema-based validation
- generated API models and DTOs
- submission and ingestion pipelines

Please note, use cases are variable and may fall outside of those covered here.

## What Changed Across All New Schemas

### 1. File names and canonical references changed

The new supported files use standardized names and the `.schema.json` suffix. Update any code, configuration, or API documentation that still points to legacy files such as:

- `json_schema_legacy/location_details.json`
- `json_schema_legacy/project_approach_and_details.json`
- `json_schema_legacy/issuances.json`
- `json_schema_legacy/disclosures.json`

### 2. Nested entity objects are now the standard contract

The new schemas are organized by entity sections such as:

- `project`
- `project_stakeholder`
- `facility`
- `geolocation_file`
- `crediting_program`
- `methodology`
- `registry`
- `validation`
- `issuance`

If your current API or validation flow flattens fields into a single object, you will need a transformation layer that groups fields into the required entity object.

### 3. `additionalProperties: true` is set broadly — additional properties are permitted

The generated schemas allow undeclared properties at the top level and inside each entity object. API frameworks and validators will accept pass-through fields without errors.

Recommended action:

- additional fields in your payload will not cause validation failures
- a prefix may be useful for your own documentation, but is not required
- you may still want to document or constrain extra fields in your own application logic if stricter control is needed

### 4. Required top-level objects are now enforced

A top-level entity object is marked `required` in the generated schema when at least one field is required anywhere within it — including fields nested inside its arrays (e.g. `project.location[].country_code`), not just fields directly on the entity itself. Sections with no required fields anywhere in their subtree are not enforced as required top-level objects.

Examples:

- `Location_Details.schema.json` requires `project`, `project_stakeholder`, and `geolocation_file` (each has required fields nested inside its `location[]` array items); `facility` is not required
- `Project_Approach_Details.schema.json` requires `project` (for `project_name`, `project_description`) and `project_stakeholder` (for `project_developer_name`)
- `Issuances.schema.json` requires `project` (for nested audit fields); its `issuance` object is not required
- `Disclosures.schema.json` requires `project` (for its attestation and governance fields) and `project_stakeholder`


### 5. Validation is more structural and less opinionated

Compared with some legacy schemas, the standardized generated schemas place more emphasis on:

- stable field names
- consistent nesting
- scalar vs array handling from CDOP cardinality
- required vs optional fields

They place less emphasis on advanced constraints such as:

- URI/email/phone formats
- custom extension patterns such as `x_*`
- rich object pairing rules between related arrays

Fields whose CDOP datatype is `enum` are generated with a real `enum` constraint, sourced from `docs/CDOP Enumerated Values Lists.xlsx`. If a field is marked `enum` in the source workbook but has no matching entry in the enumerated values list, `scripts/generate_json_schemas.py` leaves it as an unconstrained string and records it in `json_schema/unmatched_enum_fields.csv` — check that file if a field you expect to be restricted isn't.

Recommended action:

- use the new schema as the canonical contract for submission compatibility, including its enum constraints
- keep supplemental business-rule validation if your process still depends on stricter checks such as URI validation or cross-field consistency

### 6. CDOP metadata is embedded as annotations

The new field definitions include non-validation metadata such as:

- `x-cdop-field-id`
- `x-cdop-cardinality`
- `x-cdop-pre-issuance-inclusion`
- `x-cdop-data-source`
- `x-cdop-mutability`
- `x-cdop-public-private`

These are useful for documentation, UI generation, and governance-aware ingestion, but they are not validation requirements by themselves unless your tooling explicitly uses them.

Recommended action:

- continue validating against standard JSON Schema keywords
- optionally consume `x-cdop-*` annotations in forms, workflow rules, or field catalogs

## Recommended Migration Approach

### 1. Split migration into two layers

For most stakeholders, the safest approach is:

1. transform your existing payload into the new CDOP payload shape
2. validate the transformed payload against the new schema

This avoids rewriting all upstream systems at once.

### 2. Regenerate typed models from the new schemas

If you generate DTOs, OpenAPI components, or form models from schema files, regenerate them from `json_schema/*.schema.json` instead of reusing legacy generated classes.

Pay special attention to:

- fields that changed names
- arrays that replaced object collections
- objects that replaced top-level arrays
- newly required section objects

### 3. Add a normalization/pre-submit step

A pre-submit adapter should typically:

- rename legacy keys to the new field names
- move fields into the correct entity object
- convert legacy arrays of objects into parallel CDOP arrays where needed
- remove unsupported custom fields
- ensure missing required sections are created only when valid values exist

### 4. Keep legacy-only validations only if you still need them

If your current process relies on legacy constraints not present in the new generated schemas, keep them as a second validation layer after schema validation.

Note that allowed registry names (`registry.current_registry`, `registry.origin_registry`, `crediting_program.crediting_program[].crediting_program_name`) and allowed project status values (`project.status[].project_status`) are now enforced directly by the generated schema's `enum` lists — you likely no longer need a separate business-rule check for those specific fields.

Examples of constraints still worth keeping as a second layer:

- URI/email/phone formatting
- one-to-one pairing rules across related arrays

## Schema-By-Schema Guidance

### Location Details

### Migration impact

`Location_Details.schema.json` is structurally very close to the legacy location schema. For most users, migration is mainly:

- switching to the new file name
- honoring required top-level objects
- consuming the `x-cdop-*` annotations if useful

### Required top-level objects

The new schema requires `project`, `project_stakeholder`, and `geolocation_file` at the top level — each has required fields nested inside its `location[]` array items (e.g. `country_code`, `country_name`). `facility` is the only optional top-level object; none of its nested fields are marked required.

### Payload guidance

If you already submit nested location payloads with:

- `project`
- `project_stakeholder`
- optional `facility`
- `geolocation_file`

then only minor changes should be required.

### API/validator guidance

- Note that `additionalProperties: true` means your deserializer will accept undeclared fields inside each entity object; enforce a stricter contract in your own validation layer if needed.

### Project Approach & Details

### Migration impact

This schema has the most significant structural change from the legacy version.

The legacy schema used richer nested collections such as:

- `crediting_program` as an array of objects
- `methodology` as an array of objects
- `project.identifiers` as an array of `{ identifier_type, value }`
- `project.crediting_periods` as an array of objects
- `project.documents` as an array of `{ document_type, link }`
- `project_stakeholder.primary_developer` as an object
- `project_stakeholder.stakeholders` as an array of objects
- `registry.current_registry` as an object
- `registry.previous_registries` as an array of objects

The new schema standardizes these into CDOP entity objects with separate scalar and array fields.

### Key field and shape changes

Legacy to new examples:

| Legacy shape | New shape |
| --- | --- |
| `project.name` | `project.project_name` |
| `project.design_document_link` | `project.project_design_document_link` |
| `project.registry_link` | `project.current_registry_project_link` |
| `project.status` | `project.status[].project_status` |
| `project.status_updated_at` | removed; use `project.status[].is_current` to identify the current record instead of a timestamp |
| `project.sector` | `project.project_sector` |
| `project.identifiers[].identifier_type` | `project.project_id_type` (single scalar, not an array — only one identifier type/value pair is carried in `Project_Approach_Details`) |
| `project.identifiers[].value` | `project.project_id` (single scalar) |
| `project.crediting_periods[].length_years` | moved out of this schema; see `Crediting_Period.schema.json` (`project.crediting_period[].current_crediting_period_duration`) |
| `project.registration_date` | `project.project_registration_date` |
| `project.list_date` | `project.project_list_date` |
| `project.documents[].document_type` | `project.documents[].other_project_documentation_type` (array of objects, not a parallel array) |
| `project.documents[].link` | `project.documents[].other_project_documentation_link` (array of objects, not a parallel array) |
| `project_stakeholder.primary_developer.name` | `project_stakeholder.project_developer_name` |
| `project_stakeholder.primary_developer.contact.website` | `project_stakeholder.project_developer_website` |
| `project_stakeholder.primary_developer.contact.email` | `project_stakeholder.project_developer_email` |
| `project_stakeholder.primary_developer.contact.phone` | `project_stakeholder.project_developer_phone` |
| `project_stakeholder.stakeholders[].stakeholder_type` | `project_stakeholder.stakeholders[].project_stakeholder_type` (still an array of objects) |
| `project_stakeholder.stakeholders[].name` | `project_stakeholder.stakeholders[].project_stakeholder_name` |
| `project_stakeholder.stakeholders[].contact.website` | `project_stakeholder.stakeholders[].project_stakeholder_website` |
| `project_stakeholder.stakeholders[].contact.email` | `project_stakeholder.stakeholders[].project_stakeholder_email` |
| `project_stakeholder.stakeholders[].contact.phone` | `project_stakeholder.stakeholders[].project_stakeholder_phone` |
| `registry.current_registry.name` | `registry.current_registry` |
| prior registry history | review and condense as needed into `registry.origin_registry` |

### Important modeling change: identifiers collapsed to a single scalar pair

`project.identifiers[]` (an array of `{ identifier_type, value }` records) becomes a single scalar pair, `project.project_id_type` and `project.project_id` — only one identifier is carried per submission, not a list. If you track multiple identifier types (internal ID, registry ID, global unique ID) per project, pick the one you want to submit under this schema, or use `Full_List.schema.json` if you need to carry more context elsewhere.

`project.documents[]` and `project_stakeholder.stakeholders[]` remain arrays of objects in the new schema (not parallel arrays) — only field names inside each object changed.

Recommended action:

- decide which single identifier type/value to submit for `project.project_id_type` / `project.project_id`
- keep your internal richer object model if it is already working
- decide explicitly how to handle legacy registry listing dates and prior-registry history, because the new schema does not preserve the same registry-history object structure

### Required fields changed

The new schema requires:

- `project.project_name`
- `project.project_description`
- `project_stakeholder.project_developer_name`

`project.project_status` is not currently required, and it is no longer a flat scalar field — it now lives under `project.status[]`, an array of `{ project_status, project_status_reason, is_current }` records, allowing status history to be tracked over time rather than a single current value.

Notably, the legacy requirement for `project.identifiers` is no longer present in the generated schema.

### Validation behavior changed

The legacy schema included enum-like controls and custom extension support in some places. The new standardized schema enforces real `enum` constraints for fields whose CDOP datatype is `enum` (e.g., `crediting_program_name`, `standard_name`, `methodology_name`, `mitigation_type`, `project_sector`, `project_type`, `project_stakeholder_type`, `project_status`), sourced from `docs/CDOP Enumerated Values Lists.xlsx`. 

Recommended action:

- use the values in each field's generated `enum` list rather than free text for statuses, registries, sectors, and stakeholder types



### Issuances

### Migration impact

`Issuances.schema.json` changed substantially from the legacy issuance schema.

The legacy schema used a mixed top-level model with:

- `project_identifier`
- `crediting_period`
- `audits[]`
- `issuance_forecast[]`
- `forecast_total_issuance[]`
- `issuances[]`
- `cumulative_issued_volume`

The new schema consolidates this into two entity objects:

- `project` — holds `project_identifier` and an `audits[]` array
- `issuance` — holds a nested `issuance.issuance[]` array of actual issuance batch records

Forecast-related fields (`issuance_forecast[]`, `forecast_total_issuance[]`, and estimated crediting-period dates) are **not** part of `Issuances.schema.json` in the current generated schema. That information now belongs to the separate `Estimations.schema.json` (see the `estimations.vintage_mitigation[]`, `estimations.monitoring[]`, and `estimations.estimation_event[]` sections there). If your legacy payload combined actual issuances and forecasts in one document, split it across `Issuances` and `Estimations` when migrating.

### Key field and shape changes

Legacy to new examples:

| Legacy shape | New shape |
| --- | --- |
| `project_identifier` | `project.project_identifier` |
| `audits[].auditor_name` | `project.audits[].auditor_name` (array of objects, not a parallel array) |
| `audits[].site_visit_start_date` | `project.audits[].auditor_site_visit_start_date` |
| `audits[].site_visit_end_date` | `project.audits[].auditor_site_visit_end_date` |
| legacy verification report data | `project.audits[].verification_report_url` and `project.audits[].verification_report_date` |
| `crediting_period.estimated_start` / `.estimated_end` | moved to `Estimations.schema.json` |
| `issuance_forecast[]`, `forecast_total_issuance[]` | moved to `Estimations.schema.json` |
| `issuances[].batch_identifier` | `issuance.issuance[].batch_identifier` |
| `issuances[].issuance_url` | `issuance.issuance[].issuance_url` |
| `issuances[].date_of_issuance` | `issuance.issuance[].date_of_issuance` |
| `issuances[].date_of_verification` | `issuance.issuance[].date_of_verification` |
| `issuances[].verification_period_start` | `issuance.issuance[].verification_period_start` |
| `issuances[].verification_period_end` | `issuance.issuance[].verification_period_end` |
| `issuances[].batch_issued_volume` | `issuance.issuance[].batch_issued_volume` |
| `cumulative_issued_volume` | `issuance.issuance[].cumulative_issued_volume` (now per-batch, alongside a new `issuance_status` field) |

### Important modeling change: records stay as arrays of objects, not parallel arrays

Unlike some other schemas, `project.audits[]` and `issuance.issuance[]` remain arrays of objects — each record's fields are nested together, matching the legacy shape more closely. There is no flattening into parallel top-level arrays here.

Recommended action:

- keep your internal issuance-batch and audit record models if you already have them; map each record directly into the corresponding array item
- route forecast/estimate data to `Estimations.schema.json` instead of `Issuances.schema.json`

### Required fields changed

`Issuances.schema.json` requires the top-level `project` object, because a field nested inside `project.audits[]` is required; `issuance` is not required.

### API/validator guidance

- Update request models so `project_identifier` is nested under `project.project_identifier`, not top-level.
- Route forecast/estimate submissions to the `Estimations` schema instead of expecting them here.
- Treat `project` as required and `issuance` as optional per the schema, but include `issuance` whenever actual issuance batch data is available.

### Disclosures

### Migration impact

`Disclosures.schema.json` is mostly similar to the legacy structure, but a few fields moved between entity sections and top-level object requirements are now enforced.

### Key field changes

Legacy to new examples:

| Legacy shape | New shape |
| --- | --- |
| `project.list_of_landowners` | `project_stakeholder.list_of_landowners[]` |
| `registry.previous_project_crediting_program` | `project.previous_project_crediting_program` |
| `project.project_status` | removed from this schema |

### Required fields changed

The new schema requires top-level presence of both `project` and `project_stakeholder` — `project_stakeholder` is required because a field nested inside its `organization[]` array is required.

Within `project`, the following remain required:

- `carbon_credit_ownership_attestation`
- `carbon_credit_ownership_documentation`
- `legal_compliance_attestation`
- `legal_compliance_documentation`
- `project_governance_structure`

`project_status` is no longer required in the disclosures schema.

### API/validator guidance

- Move `list_of_landowners` into `project_stakeholder` and convert it from a legacy string into the new array form if needed.
- Move the boolean flag about other crediting programs from `registry` to `project`.
- Do not expect `project_status` to be present in disclosures payloads; it now belongs in other submission contexts such as Project Approach & Details.

### Full List

### When to use it

`Full_List.schema.json` combines the standardized fields from the supported schemas into one large submission contract.

This is useful if your process validates or exchanges a single comprehensive CDOP document instead of schema-by-schema submissions.

### Migration guidance

If you already plan to migrate to:

- `Location_Details.schema.json`
- `Project_Approach_Details.schema.json`
- `Issuances.schema.json`
- `Disclosures.schema.json`

then the `Full_List.schema.json` migration is mostly the union of those same changes.

Recommended action:

- first make each domain-specific payload valid on its own
- then combine them into a full-list payload if your integration requires a single document

## Practical Adapter Patterns

### Pattern 1: Keep your internal model, export CDOP separately

This is the recommended approach for most existing stakeholders.

- Keep your current internal domain objects and relational model.
- Build a dedicated CDOP export mapper.
- Validate only the export payload against the new schema.


### Pattern 2: Add a pre-validation normalization step

Before schema validation:

- rename fields
- move values into the correct entity object
- split record collections into aligned arrays
- remove unsupported extras

This lets upstream systems change more gradually.

### Pattern 3: Layer schema validation with business validation

Use:

1. schema validation for CDOP contract compliance
2. business validation for organizational rules and data quality

Business validation is still useful for:

- enum/value list enforcement for the fields listed in `json_schema/unmatched_enum_fields.csv` (fields marked `enum` in the source workbook with no matching entry in the enumerated values list, so the generated schema leaves them unconstrained)
- URI/email/phone format checks
- duplicate detection
- cross-array alignment checks
- date sequencing logic

## Migration Checklist

- Update schema file references to `json_schema/*.schema.json`.
- Regenerate typed models or DTOs from the new schema files.
- Add or update a transformation layer from legacy payload shape to new CDOP payload shape.
- Note that `additionalProperties: true` is set — extra fields in payloads will not cause schema validation failures.
- Move renamed and relocated fields to their new entity sections.
- Collapse `project.identifiers[]` into the single scalar pair `project.project_id_type` / `project.project_id`; other legacy arrays of objects (`documents[]`, `stakeholders[]`, `audits[]`, `issuances[]`) remain arrays of objects with renamed fields.
- Use each field's generated `enum` list instead of free text.
- Preserve any legacy-only business rules in a second validation layer if still needed.
- Test sample submissions against the new schema before switching production submission flows.

## Final Recommendation

For most stakeholders, the lowest-risk migration path is not to remodel internal systems around the new JSON shape immediately. Instead:

1. keep existing internal structures
2. create a deterministic CDOP export adapter
3. validate the export payload against the new schema
4. keep supplemental validation rules where the generated schema is intentionally less restrictive than prior implementations

That approach will align with the standardized CDOP schema while minimizing disruption to existing APIs and validation workflows.

# CDOP JSON Schema Migration Guide

## Purpose

As of May 26, 2026, the supported CDOP JSON Schema files are the generated schemas under `json_schema/`:

- `Location_Details.schema.json`
- `Project_Approach_Details.schema.json`
- `Issuances.schema.json`
- `Disclosures.schema.json`
- `Full_List.schema.json`

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

### 3. `additionalProperties: false` is enforced broadly

The generated schemas disallow undeclared properties at the top level and inside each entity object. This is important for API frameworks that previously accepted pass-through fields.

Recommended action:

- reject unknown fields before submission, or
- strip unknown fields in a preprocessing step, or
- map internal-only fields to a separate non-CDOP payload

### 4. Required top-level objects are now enforced

Several legacy schemas had few or no top-level `required` entries. The new schemas require whole sections to be present when those sections contain required fields.

Examples:

- `Location_Details.schema.json` requires `project`, `project_stakeholder`, and `geolocation_file`
- `Project_Approach_Details.schema.json` requires `project` and `project_stakeholder`
- `Issuances.schema.json` requires `issuance`
- `Disclosures.schema.json` requires `project` and `project_stakeholder`

Even if some fields inside a section are optional, the section itself may still need to exist.

### 5. Validation is more structural and less opinionated

Compared with some legacy schemas, the standardized generated schemas place more emphasis on:

- stable field names
- consistent nesting
- scalar vs array handling from CDOP cardinality
- required vs optional fields

They place less emphasis on advanced constraints such as:

- enumerated values
- URI/email/phone formats
- custom extension patterns such as `x_*`
- rich object pairing rules between related arrays

Recommended action:

- use the new schema as the canonical contract for submission compatibility
- keep supplemental business-rule validation if your process still depends on stricter checks such as enum lists, URI validation, or cross-field consistency

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

Examples:

- allowed registry names
- allowed project status values
- URI/email/phone formatting
- one-to-one pairing rules across related arrays

## Schema-By-Schema Guidance

### Location Details

### Migration impact

`Location_Details.schema.json` is structurally very close to the legacy location schema. For most users, migration is mainly:

- switching to the new file name
- honoring required top-level objects
- honoring `additionalProperties: false`
- consuming the `x-cdop-*` annotations if useful

### Required top-level objects

The new schema requires:

- `project`
- `project_stakeholder`
- `geolocation_file`

The legacy file did not enforce these top-level objects as strictly.

### Payload guidance

If you already submit nested location payloads with:

- `project`
- `project_stakeholder`
- optional `facility`
- `geolocation_file`

then only minor changes should be required.

### API/validator guidance

- Ensure your deserializer rejects undeclared fields inside each entity object.
- Ensure `project` and `project_stakeholder` are always present when validating location submissions.
- Do not assume `facility` is required.

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
| `project.status` | `project.project_status` |
| `project.status_updated_at` | `project.project_status_updated_at` |
| `project.sector` | `project.project_sector` |
| `project.identifiers[].identifier_type` | `project.project_id_type[]` |
| `project.identifiers[].value` | `project.project_id[]` |
| `project.crediting_periods[].length_years` | `project.crediting_period_length[]` |
| `project.registration_date` | `project.project_registration_date` |
| `project.list_date` | `project.project_list_date` |
| `project.documents[].document_type` | `project.other_project_documentation_type[]` |
| `project.documents[].link` | `project.other_project_documentation_link[]` |
| `project_stakeholder.primary_developer.name` | `project_stakeholder.project_developer_name` |
| `project_stakeholder.primary_developer.contact.website` | `project_stakeholder.project_developer_website` |
| `project_stakeholder.primary_developer.contact.email` | `project_stakeholder.project_developer_email` |
| `project_stakeholder.primary_developer.contact.phone` | `project_stakeholder.project_developer_phone` |
| `project_stakeholder.stakeholders[].stakeholder_type` | `project_stakeholder.project_stakeholder_type[]` |
| `project_stakeholder.stakeholders[].name` | `project_stakeholder.project_stakeholder_name[]` |
| `project_stakeholder.stakeholders[].contact.website` | `project_stakeholder.project_stakeholder_website[]` |
| `project_stakeholder.stakeholders[].contact.email` | `project_stakeholder.project_stakeholder_email[]` |
| `project_stakeholder.stakeholders[].contact.phone` | `project_stakeholder.project_stakeholder_phone[]` |
| `registry.current_registry.name` | `registry.current_registry` |
| prior registry history | review and condense as needed into `registry.origin_registry` |

### Important modeling change: arrays of objects to parallel arrays

Several legacy structures preserved relationships inside each object record. The new schema often represents those values as parallel arrays instead.

Examples:

- `project.identifiers[]` becomes `project.project_id_type[]` plus `project.project_id[]`
- `project.documents[]` becomes `project.other_project_documentation_type[]` plus `project.other_project_documentation_link[]`
- `project_stakeholder.stakeholders[]` becomes several parallel arrays

Recommended action:

- maintain ordering consistency across related arrays in your transform layer
- keep your internal richer object model if it is already working
- flatten into the CDOP parallel-array model only at export/validation time
- decide explicitly how to handle legacy registry listing dates and prior-registry history, because the new schema does not preserve the same registry-history object structure

### Required fields changed

The new schema requires:

- `project.project_name`
- `project.project_description`
- `project.project_status`
- `project.project_status_updated_at`
- `project_stakeholder.project_developer_name`

Notably, the legacy requirement for `project.identifiers` is no longer present in the generated schema.

### Validation behavior changed

The legacy schema included enum-like controls and custom extension support in some places. The new standardized schema does not currently enforce those same constraints.

Recommended action:

- if you still need controlled lists for statuses, registries, or stakeholder types, enforce them in your application logic
- if you previously used `x_*` custom extension keys in submissions, move that data outside the validated CDOP payload unless and until the standard schema explicitly supports it

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

- `project`
- `issuance`

### Key field and shape changes

Legacy to new examples:

| Legacy shape | New shape |
| --- | --- |
| `project_identifier` | `project.project_identifier` |
| `audits[].auditor_name` | `project.auditor_name[]` |
| `audits[].site_visit_start_date` | `project.auditor_site_visit_start_date[]` |
| `audits[].site_visit_end_date` | `project.auditor_site_visit_end_date[]` |
| legacy verification report data | review and map into `project.verification_report_url[]` and `project.verification_report_date[]` when those values can be derived cleanly |
| `crediting_period.estimated_start` | `issuance.estimated_crediting_period_start` |
| `crediting_period.estimated_end` | `issuance.estimated_crediting_period_end` |
| `issuance_forecast[].forecast_year` | `issuance.forecast_year[]` |
| `issuance_forecast[].forecast_annual_issuance` | `issuance.forecast_annual_issuance[]` |
| `forecast_total_issuance[]` | `issuance.forecast_total_issuance[]` |
| `issuances[].batch_identifier` | `issuance.batch_identifier[]` |
| `issuances[].issuance_url` | `issuance.issuance_url[]` |
| `issuances[].date_of_issuance` | `issuance.date_of_issuance[]` |
| `issuances[].date_of_verification` | `issuance.date_of_verification[]` |
| `issuances[].verification_period_start` | `issuance.verification_period_start[]` |
| `issuances[].verification_period_end` | `issuance.verification_period_end[]` |
| `issuances[].batch_issued_volume` | `issuance.batch_issued_volume[]` |
| `cumulative_issued_volume` | `issuance.cumulative_issued_volume` |

### Important modeling change: issuance records become parallel arrays

Like Project Approach & Details, the legacy `issuances[]` array of records becomes multiple related arrays under `issuance`.

Recommended action:

- keep your internal issuance-batch record model if you already have one
- generate CDOP export arrays from those records in a deterministic order
- validate that all related issuance arrays have matching lengths before submission

Example checks worth keeping in your application even if they are not enforced by schema:

- `batch_identifier[]`, `date_of_issuance[]`, and `batch_issued_volume[]` should align by index
- `forecast_year[]` and `forecast_annual_issuance[]` should align by index

### Required fields changed

The new schema requires:

- `issuance.forecast_annual_issuance`
- `issuance.forecast_year`
- `issuance.forecast_total_issuance`

The legacy top-level requirement for `audits` no longer exists.

### API/validator guidance

- Update request models so `project_identifier` is no longer top-level.
- Treat `project` as optional in schema terms, but include it whenever project-level audit or report information is available.
- Treat `issuance` as the required submission section.

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

The new schema requires top-level presence of:

- `project`
- `project_stakeholder`

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

This is especially helpful where the new schemas use parallel arrays instead of arrays of objects.

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

- enum/value list enforcement
- URI/email/phone format checks
- duplicate detection
- cross-array alignment checks
- date sequencing logic

## Migration Checklist

- Update schema file references to `json_schema/*.schema.json`.
- Regenerate typed models or DTOs from the new schema files.
- Add or update a transformation layer from legacy payload shape to new CDOP payload shape.
- Enforce `additionalProperties: false` handling.
- Ensure required top-level entity objects are present.
- Move renamed and relocated fields to their new entity sections.
- Convert legacy arrays of objects into aligned CDOP arrays where required.
- Preserve any legacy-only business rules in a second validation layer if still needed.
- Test sample submissions against the new schema before switching production submission flows.

## Final Recommendation

For most stakeholders, the lowest-risk migration path is not to remodel internal systems around the new JSON shape immediately. Instead:

1. keep existing internal structures
2. create a deterministic CDOP export adapter
3. validate the export payload against the new schema
4. keep supplemental validation rules where the generated schema is intentionally less restrictive than prior implementations

That approach will align submissions with the standardized CDOP schema while minimizing disruption to existing APIs and validation workflows.

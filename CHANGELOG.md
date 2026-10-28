# Changelog

All notable changes to the CDOP JSON schemas are in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
The versions follow [Semantic Versioning](https://semver.org/) from `2.0.1`.

## [Unreleased]

The first release that uses this release process.

### Added

- A versioned `$id` in each schema.
- The `VERSION` file and a release workflow.
- `scripts/validate_examples.py` and a workflow that validates the examples on each pull request.
- A link to the latest release in the README.

### Fixed

- `scripts/generate_json_schemas.py` handles typos and letter case in field paths (#44). This changes two schemas:
  - `Co_Benefits` and `Full_List`: `overview_of_the_projects_approach_to_ track_and_quantify` (with a space) is now `overview_of_the_projects_approach_to_track_and_quantify`.
  - `Full_List`: the array `crediting period` is merged into `crediting_period`.
  - `Full_List`: the required field `unit.credit_blockblock_start` is now `unit.credit_block[].block_start`, the same as in `Unit_Description`.
    If you validate against `Full_List`, put `block_start` in each `credit_block[]` item.
- The README link to the Co-Benefits schema points to `Co_Benefits.schema.json`.
- The migration guide says that legacy arrays of objects stay arrays of objects.

### Changed

The migration guide moved to `docs/MIGRATION-v1-to-v2.md`.

### Removed

The `json_schema_legacy/` and `examples_legacy/` folders are removed from `main`.
The legacy files are available from the `v1.0.0` release.

## [2.0.0] - 2026-09-17

Version 2, announced at Climate Week NYC 2026.
This release has breaking changes.
Read the [migration guide](https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/blob/main/docs/MIGRATION-v1-to-v2.md) before you update.

The `v2.0.0` tag was made later, from commit `eff6ca3` (2026-09-16), the last schema update before the announcement.
The `$id` of each schema in this release does not contain a version.

### Added

- Schemas that `scripts/generate_json_schemas.py` makes from `docs/CDOP_SCHEMA.xlsx`.
- New schemas:
  `Unit_Description`, `Crediting_Period`, `Estimations`, `Co_Benefits`,
  `Durability_Permanence`, `Project_Finance`, `Labels_Certifications`, and `Full_List`.
- `enum` constraints from `docs/CDOP Enumerated Values Lists.xlsx`.
- `x-cdop-*` annotations with CDOP metadata for each field.

### Changed

- New file names with the `.schema.json` suffix.
- Fields are in entity objects, for example `project`, `project_stakeholder`, and `issuance`.
- Many fields have new names, for example `project.name` is now `project.project_name`.
- Top-level entity objects that contain required fields are required.
- `additionalProperties` is `true`.
- Forecast data moved from `Issuances` to `Estimations`.

## [1.0.0] - 2025-09-23

Version 1, announced at Climate Week NYC 2025.
These legacy schemas are deprecated. Use `2.0.0` or later.

The `v1.0.0` tag was made later, from commit `1b61e58`.
The schemas are in the root folder of this release.

### Added

Schemas `location_details`, `project_approach_and_details`, `issuances`, and `disclosures` and an example for each schema.

[Unreleased]: https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/releases/tag/v2.0.0
[1.0.0]: https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/releases/tag/v1.0.0

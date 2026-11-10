# Carbon-Data-Open-Protocol
Repository storing technical specification and documentation for the CDOP schema.

Latest release: [releases/latest](https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/releases/latest). The current schema files linked below can include changes that are not released yet.

<span style="color:orange">As of May 26, 2026, the supported versions of the CDOP JSON schema files are available under `json_schema/` (Version 2, release `v2.0.0` and later). Legacy schema files (Version 1) are available in the [`v1.0.0` release](https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/releases/tag/v1.0.0). The supported version of the CDOP JSON schema files reflect breaking changes compared to the legacy schema files. Internal systems will need to be recalibrated to reflect these changes. For those who have adopted the legacy schema files, please refer to the [migration guide](/docs/MIGRATION-v1-to-v2.md) for guidance on migrating over the new supported versions.</span>


# CDOP Overview	
The growth of carbon markets and their elevation into a mature, fully investable asset class are both inhibited by a lack of data standardization and fungibility. For example, any comparison between two projects from different registries currently requires a bespoke translation of a series of misaligned data fields. A common carbon data open protocol would create the basis for standardization, transparency and fungibility needed to improve integrity and dramatically scale the carbon market	
	
Through an open, multi-stakeholder process, our mission is to propose a Carbon Data Open Protocol (CDOP) that includes (1) a set of principles to inform the purpose, use, and development of (2) a common data schema, with definitions and rules that standardize data describing carbon crediting projects and carbon credits across markets, geographies and activity types (including applicable methodologies, project descriptions, and digital MRV formats), and (3) governance framework for maintaining and updating the protocol.	
	
## CDOP Schemas

CDOP's Technical Working Group (TWG) began the schema development process by collecting schemas from 15+ member organizations willing to share their schemas. Once these schemas were received, the TWG developed an organization system (hereafter known as the Mapping Tool) to map all the schemas against relevant metadata fields in preparation to compare and contrast these schemas, so that harmonization could occur effectively.

Schemas are actively developed to ensure scalable data sharing across the industry. Contribution is actively encouraged through the contribution guidelines highlighted below. 

The CDOP Schema can be found as an Excel file [HERE](/docs/CDOP_SCHEMA.xlsx).

The enumerated values lists for the schema can be found [HERE](/docs/CDOP%20Enumerated%20Values%20Lists.xlsx).

The descriptions of all the currently published schemas can be found [HERE](https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/blob/main/docs/SCHEMA_DESCRIPTIONS.md)

Any other supporting documents and information can be found in the Wiki page of the repository, located [HERE](https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/wiki).

### Versions

The CDOP JSON schemas use [Semantic Versioning](https://semver.org/). The `VERSION` file holds the version of the latest release, or of the next release when it is in preparation. Each release is a Git tag `vMAJOR.MINOR.PATCH` with a [GitHub release](https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/releases). The [change log](/CHANGELOG.md) lists the changes in each release.

- **MAJOR**: a payload that was valid can become invalid. Examples: a field is removed or renamed, a field becomes required, a type changes, or an enum value is removed.
- **MINOR**: a change that is backward compatible. Examples: a new optional field, a new schema file, or a new enum value.
- **PATCH**: no change to validation. Examples: descriptions, documentation, or script fixes that give the same schemas.

The `$id` of each schema contains its release, for example `https://raw.githubusercontent.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/v2.1.0/json_schema/Issuances.schema.json`. Use a release URL like this one in your systems. Files on the `main` branch can change before the next release. Releases `v1.0.0` and `v2.0.0` were made after their announcements, and their `$id` values do not contain a version.

## Adoption

Adoption of the tool lends to greater collaboration and data sharing across the industry. Some of the key areas for adoption are;

- **Registries and data platforms**:​ Making data available in CDOP format ensures partners can obtain and process data with greater efficiency​.
- **Project developers​**: Submitting data in CDOP format allows for more standardisation and less bespoke work for publishing project information.
- **Ratings agencies and data providers​**: Adopt CDOP schemas for data ingestion of data can improve efficiency of data sharing and publishing.

## Validating Your Data

CDOP provides two lightweight options for validating a JSON payload against the schemas locally.

### Option 1 — Command-line tools

Several off-the-shelf CLI validators support JSON Schema draft 2020-12. The examples below use [`check-jsonschema`](https://check-jsonschema.readthedocs.io/), which can be installed with pip:

```bash
pip install check-jsonschema
```

**Validate a single file:**
```bash
check-jsonschema --schemafile json_schema/Disclosures.schema.json my_disclosures.json
```

### Option 2 — Python validation script

A helper script is included at `scripts/validate.py`. It requires Python 3.10+ and the `jsonschema` package:

```bash
pip install jsonschema
```

**Validate a data file:**
```bash
python scripts/validate.py my_data.json --schema json_schema/Issuances.schema.json
```

**Compare your own schema against the canonical CDOP schema:**
```bash
python scripts/validate.py my_schema.json --compare --schema json_schema/Disclosures.schema.json
```

The `--compare` flag treats the input file as a schema and checks it structurally against the canonical CDOP schema — same properties, types, and required fields. Cosmetic differences (descriptions, `$id`, `title`) are ignored. This is useful for confirming that a custom schema implementation stays in sync with the official CDOP definition.

The script exits with code `0` on success and `1` on failure, making it easy to integrate into CI pipelines. Differences are printed with the JSON path and a description of each issue.

**Validate all examples in `examples/`:**
```bash
python scripts/validate_examples.py
```

The "Validate CDOP Examples" workflow runs this check on each pull request.

### Legacy Schema Validation

CDOP recommends following the canonical schemas and validation approaches above. However, if using legacy schemas, [this tool](https://cdop-schema-validator.lovable.app/) can be used to validate a payload.

# Contributing Guidelines

We welcome contributions to this project! To ensure a smooth process, please follow the guidelines below.

## Maintainers  
This repository is maintained by members of the **CDOP Technical Working Group**.  
If you would like to become a maintainer, please contact us at **contact@cdop** (TBD).

### Raising Issues & Feature Requests  
- Use [GitHub Issues](../../issues) to report bugs, propose features, or suggest improvements.  
- When creating an issue, please apply one of the following labels (if possible):  
  - `bug` – unexpected or broken behaviour  
  - `enhancement` – new feature or functionality request  
  - `documentation` – changes or additions to documentation  
  - `discussion` – ideas or open questions for maintainers/community input  

All issues and requests are reviewed during **fortnightly maintainer sessions** for consideration.

### Pull Requests  
We encourage contributions via pull requests (PRs).  
- Fork the repository and create a feature branch.  
- Reference any related issues in your PR description.  
- Be clear and concise in commit messages.  

PRs will be reviewed by maintainers during the regular review cycle. Please be patient and open to feedback.

### General Contribution Guidelines  
- Be respectful and collaborative.  
- Add/update documentation when relevant.  
- When in doubt, open an issue to discuss before submitting a large change.  
- Please ensure that any schema changes are reflected in the examples provided.


	
# Frequently Asked Questions (FAQs)	
- Can more than one value be reported for a particular field?	

Depends. This is where the "cardinality" metadata column is a useful guide (full definition in the 'Metadata Fields Definition' tab). The first number in the cardinality number indicates whether a value is required or optional with the use of a 1 and 0 respectively. the second number or asterisk indicates where multiple values can be assigned for a particular field. If a 1 is present, then only one value can be entered. If an * is present then multiple values can be present. Some examples: 1..1 = a required field with only one input, 1..* = a required field that must have one or more values, 0..1 = an optional field with only one input, 0..* = an optional field that can have no values or one or more values. Fields that are nested together within the same field path have a cardinality of 1..1 or 0..1. In this instance, 1..1 cardinality indicates it is a required field whereas 0..1 indicates it is an optional field. In both instances, however, multiples values can be recorded due to the nested structure of the arrays.	
	
- How should an organization using the schema store multiple values for a particular field?	

In this current versioning of the CDOP Schema, CDOP is NOT RECOMMENDING how an organization stores multiple values for any particular field or data storage of any sort for that matter. Please keep in mind data integrity best practices, such as first normal form, when developing your own organization’s internal solutions	
	
- Why hasn't CDOP developed a unique location ID system as part of this schema?	

The technical requirements to develop a unique location ID system are too complex for this version of the CDOP Location Details Schema. Future versions may include this type of system.	

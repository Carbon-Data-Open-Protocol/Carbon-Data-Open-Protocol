# Carbon-Data-Open-Protocol
Repository storing technical specification and documentation for the CDOP schema.

# CDOP Overview	
The growth of carbon markets and their elevation into a mature, fully investable asset class are both inhibited by a lack of data standardization and fungibility. For example, any comparison between two projects from different registries currently requires a bespoke translation of a series of misaligned data fields. A common carbon data open protocol would create the basis for standardization, transparency and fungibility needed to improve integrity and dramatically scale the carbon market	
	
Through an open, multi-stakeholder process, our mission is to propose a Carbon Data Open Protocol (CDOP) that includes (1) a set of principles to inform the purpose, use, and development of (2) a common data schema, with definitions and rules that standardize data describing carbon crediting projects and carbon credits across markets, geographies and activity types (including applicable methodologies, project descriptions, and digital MRV formats), and (3) governance framework for maintaining and updating the protocol.	
	
## CDOP Schemas

CDOP's Technical Working Group (TWG) began the schema development process by collecting schemas from 15+ member organizations willing to share their schemas. Once these schemas were received, the TWG developed an organization system (hereafter known as the Mapping Tool) to map all the schemas against relevant metadata fields in preparation to compare and contrast these schemas, so that harmonization could occur effectively.

Schemas are actively developed to ensure scalable data sharing across the industry. Contribution is actively encouraged through the contribution guidelines highlighted above. 

A summary of the status of the TWG work plan can be found [HERE](https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/blob/main/CDOP_TWG_WORK_STATUS.pdf).

A visual diagram of the CDOP Schema can be found [HERE](https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/blob/main/CDOP%20Schema%20Visual%20Diagram.pdf).

Any other supporting documents and information can be found in the Wiki page of the repository, located [HERE](https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/wiki).



## Location

 The schema aims to capture all relevant information related to the location of the project and its stakeholders (e.g., the project developer). Aside from standard mailing addresses and ISO country codes, the schema also allows for GIS file inputs. 

If it is technically feasible by an organization using this schema, the country code field can automatically inform a number of other fields relevant in this schema. It also would ideally be used to inform address format so that address formats are standardized using ISO 19160 Standard.	

In the event that any of the associated entities (project, project stakeholder, and/or facility) do not have a conventional address, use the 'alternative address' field as a means of capturing unconventional, partial, etc. aspects of a relevant address.

The Location JSON can be found [HERE](https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/blob/main/location_details.json).

## Project Approach and Details (PAD)

The PAD schema aims to capture all relevant information related to the project’s approach and details, including its crediting program, registry, status, design, project type, methodology, project developer information, validation, and name. The majority of this information would be that which is already included in a project’s design document. 

The PAD JSON can be found [HERE](https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/blob/main/project_approach_and_details.json).

## Disclosures 

The Disclosures schema aims to capture all relevant information related to project disclosures, including attestations (e.g., child labor and land rights), carbon ownership, project developer organization experience and details, public comment, and (if applicable) previous crediting program history. All fields are marked as Public.

The Disclosures JSON can be found [HERE](https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/blob/main/disclosures.json).

## Issuance

The Issuance schema aims to capture all relevant information related to the project’s issuances, including its forecasted issuance volumes, estimated crediting period, date of issuance, and verification.

The Issuance JSON can be found [HERE](https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/blob/main/issuances.json).

## Adoption

Adoption of the tool lends to greater collaboration and data sharing across the industry. Some of the key areas for adoption are;

- **Registries and data platforms**:​ Making data available in CDOP format ensures partners can obtain and process data with greater efficiency​.
- **Project developers​**: Submitting data in CDOP format allows for more standardisation and less bespoke work for publishing project information.
- **Ratings agencies and data providers​**: Adopt CDOP schemas for data ingestion of data can improve efficiency of data sharing and publishing.

To allow for adoption, [this tool](https://cdop-schema-validator.lovable.app/) can be used to validate a payload against the various cdop schemas. This allows users to ensure their api interfaces are compatible. 

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

Depends. This is where the "cardinality" metadata column is a useful guide (full definition in the 'Metadata Fields Definition' tab). The first number in the cardinality number indicates whether a value is required or optional with the use of a 1 and 0 respectively. the second number or asterisk indicates where multiple values can be assigned for a particular field. If a 1 is present, then only one value can be entered. If an * is present then multiple values can be present. Some examples: 1..1 = a required field with only one input, 1..* = a required field that must have one or more values, 0..1 = an optional field with only one input, 0..* = an optional field that can have no values or one or more values.	
	
- How should an organization using the schema store multiple values for a particular field?	

In this current versioning of the CDOP Schema, CDOP is NOT RECOMMENDING how an organization stores multiple values for any particular field or data storage of any sort for that matter. Please keep in mind data integrity best practices, such as first normal form, when developing your own organization’s internal solutions	
	
- Why hasn't CDOP developed a unique location ID system as part of this schema?	

The technical requirements to develop a unique location ID system are too complex for this version of the CDOP Location Details Schema. Future versions may include this type of system.	

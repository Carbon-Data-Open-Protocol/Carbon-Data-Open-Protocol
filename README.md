# Carbon-Data-Open-Protocol
Repository storing technical specification and documentation for the CDOP schema.
# CDOP Overview	
The growth of carbon markets and their elevation into a mature, fully investable asset class are both inhibited by a lack of data standardization and fungibility. For example, any comparison between two projects from different registries currently requires a bespoke translation of a series of misaligned data fields. A common carbon data open protocol would create the basis for standardization, transparency and fungibility needed to improve integrity and dramatically scale the carbon market	
	
Through an open, multi-stakeholder process, our mission is to propose a Carbon Data Open Protocol (CDOP) that includes (1) a set of principles to inform the purpose, use, and development of (2) a common data schema, with definitions and rules that standardize data describing carbon crediting projects and carbon credits across markets, geographies and activity types (including applicable methodologies, project descriptions, and digital MRV formats), and (3) governance framework for maintaining and updating the protocol.	
	
## Location Details Schema	
The contents of this file encompass CDOP's Location Details Schema and associated materials and reosurces	
	
## Location Details Schema Related Links	
[Link to CDOP website]	
[Link to downloadable version of this Excel file]	
[Link to downloadable version of csv file]	
[Link to downloadable version of JSON file]	
[Link to GitHub/Hosting site]	
[Link to CDOP Principles]	
	
## Location Details Schema Development Process	
CDOP's Technical Working Group (TWG) began the schema development process by collecting schemas from 15+ member organizations willing to share their schemas. Once these schemas were received, the TWG developed an organization system (hereafter known as the Mapping Tool) to map all the schemas against relevant metadata fields in preparation to compare and contrast these schemas, so that harmonization could occur effectively.	
The next phase of the development process involved mapping and harmonization, which simply put, is the process by which the TWG used the Mapping Tool to unify the disparate schemas that were received and mapped the fields within them against relevant metadata fields into a unified CDOP schema - with Location Details being the first category to be harmonized and published. In order to organize all the submitted schemas, the TWG developed metadata fields to create an intuitive and clear structure in which each metadata field has a specific definition associated with it so that it is understood what information is required. Part of the harmonization process is striking a balance between having a robust set of fields that capture relevant and material information of and related to a carbon crediting project, without being overly exhaustive (i.e. including every single unique field we received in all the schemas).	
Once an initial iteration was developed, we presented that iteration to the TWG membership in hopes of receiving feedback from our members. Twelve members stepped up and provided valuable feedback to improve the first iteration of the Location Details schema. The TWG then reviewed, analyzed, and ultimately incorporated all relevant feedback to develop a second iteration of the Location Details schema. This second iteration was then presented to membership for a final feedback round before publication.	
	
## Contents of Spreadsheet	
This spreadsheet has 7 tabs in addition to this READ FIRST sheet: CDOP Location Data Schema, Visual Data Model, Metadata Fields Definitions, Entity Definitions, geo_location_file details, Enumerated Values List, ISO 3166-1 Table	
	
### CDOP Location Data Schema Tab	
This tab contains all the fields included in CDOP's Location Details Schema 	
	
If it is technically feasible by an organization using this schema, the country code field can automatically inform a number of other fields relevant in this schema. It also would ideally be used to inform address format so that address formats are standardized using ISO 19160 Standard.	
In the event that any of the associated entities (project, project developer, and/or facility) do not have a conventional address, use the 'alternative address' field as a means of capturing unconventional, partial, etc. aspects of an address	
	
### Visual Data Model Tab	
This is visual model that highlights the relationships between different fields and associated entities	
	
### Metadata Fields Definitions Tab	
This tab defines all the metadata columns present in the CDOP Location Data Schema tab	
	
### Entity Definitions Tab	
This tab defines the associated entities used in the CDOP Location Data Schema tab	
	
### geo_location_file details Tab	
This tab provides greater context around geolocation related fields in the CDOP Location Data Schema tab	
	
### Enumeratd Values List Tab	
This tab provides a list of all the enumerated values for all the fields with an enum datatype in the CDOP Location Data Schema tab [STILL UNDER CONSTRUCTION]	
	
### ISO 3166-1 Table Tab	
This tab provides a full table of the ISO 3166-1 standard country codes [STILL UNDER CONSTRUCTION]	

## Adoption

Adoption of the tool lends to greater collaboration and data sharing across the industry. Some of the key areas for adoption are;

- **Registries and data platforms:**​ Making data available in CDOP format ensures partners can obtain and process data with greater efficiency​.
- **Project developers​**: Submitting data in CDOP format allows for more standardisation and less bespoke work for publishing project information.
- **Ratings agencies and data providers​**: Adopt CDOP schemas for data ingestion of data can improve efficiency of data sharing and publishing.

To allow for adoption, [this tool](https://cdop-schema-validator.lovable.app/) can be used to validate a payload against the various cdop schemas. This allows users to ensure their api interfaces are compatible. 
	
# Frequently Asked Questions (FAQs)	
- Can more than one value be reported for a particular field?	

Depends. This is where the "cardinality" metadata column is a useful guide (full definition in the 'Metadata Fields Definition' tab). The first number in the cardinality number indicates whether a value is required or optional with the use of a 1 and 0 respectively. the second number or asterisk indicates where multiple values can be assigned for a particular field. If a 1 is present, then only one value can be entered. If an * is present then multiple values can be present. Some examples: 1..1 = a required field with only one input, 1..* = a required field that must have one or more values, 0..1 = an optional field with only one input, 0..* = an optional field that can have no values or one or more values.	
	
- How should an organization using the schema store multiple values for a particular field?	

In this current versioning of the CDOP Schema, CDOP is NOT RECOMMENDING how an organization stores multiple values for any particular field or data storage of any sort for that matter. Please keep in mind data integrity best practices, such as first normal form, when developing your own organization’s internal solutions	
	
- Why hasn't CDOP developed a unique location ID system as part of this schema?	

The technical requirements to develop a unique location ID system are too complex for this version of the CDOP Location Details Schema. Future versions may include this type of system.	

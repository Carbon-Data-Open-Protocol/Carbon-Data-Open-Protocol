# Overview
Below is a list of all the different schemas within this repository. Each is highlighted individually providing a short summary and a link to the JSON schema within the repo.

## Full List

The Full List schema is the combination of all schemas currently published in this repo in one JSON file.

The current **Full List JSON** can be found [HERE](https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/blob/main/json_schema/Full_List.schema.json)

## Location

 The schema aims to capture all relevant information related to the location of the project and its stakeholders (e.g., the project developer). Aside from standard mailing addresses and ISO country codes, the schema also allows for GIS file inputs. 

If it is technically feasible by an organization using this schema, the country code field can automatically inform a number of other fields relevant in this schema. It also would ideally be used to inform address format so that address formats are standardized using ISO 19160 Standard.	

In the event that any of the associated entities (project, project stakeholder, and/or facility) do not have a conventional address, use the 'alternative address' field as a means of capturing unconventional, partial, etc. aspects of a relevant address.

The current **Location JSON** can be found [HERE](https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/blob/main/json_schema/Location_Details.schema.json).

## Project Approach and Details (PAD)

The PAD schema aims to capture all relevant information related to the project’s approach and details, including its crediting program, registry, status, design, project type, methodology, project developer information, validation, and name. The majority of this information would be that which is already included in a project’s design document. 

The current **PAD JSON** can be found [HERE](https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/blob/main/json_schema/Project_Approach_Details.schema.json).

## Disclosures 

The Disclosures schema aims to capture all relevant information related to project disclosures, including attestations (e.g., child labor and land rights), carbon ownership, project developer organization experience and details, public comment, and (if applicable) previous crediting program history. All fields are marked as Public.

The current **Disclosures JSON** can be found [HERE](https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/blob/main/json_schema/Disclosures.schema.json).

## Issuance

The Issuance schema aims to capture all relevant information related to the project’s issuances, including its forecasted issuance volumes, estimated crediting period, date of issuance, and verification.

The current **Issuance JSON** can be found [HERE](https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/blob/main/json_schema/Issuances.schema.json).

## Unit Description

The Unit Description schema aims to capture all relevant information associated with the unit of any particular project. This includes its serial number, status, type, quantity, vintage, and metric among other properties.

The current **Unit Description JSON** can be found [HERE](https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/blob/main/json_schema/Unit_Description.schema.json).

## Crediting Period

The Crediting Period schema aims to capture all relevant information related to the project's crediting period including the crediting period type, current crediting period duration, maximum cumulative crediting duration, and maximum number of crediting periods.

The current **Crediting Period JSON** can be found [HERE](https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/blob/main/json_schema/Crediting_Period.schema.json).

## Estimations

The Estimations schema aims to capture all relevant information related to estimations around emissions mitigation per vintage, monitoring period, issuance, and status. It also captures information relevant to estimated annual and total emissions mitigation along with the estimated total years for the project. 

The current **Estimations JSON** can be found [HERE](https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/blob/main/json_schema/Estimations.schema.json).

## Co-Benefits

The Co-Benefits schema aims to capture all relevant information related to a project's contribution to the UN Sustainable Development Goals (SDGs) and other co-benefits, including the assessment methods used, targeted and achieved co-benefit indicators, baseline and target values, and supporting evidence.

The current **Co-Benefits JSON** can be found [HERE](https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/blob/main/json_schema/Co_Benefits.schema.json).

## Durability & Permanence

The Durability & Permanence schema aims to capture all relevant information related to a project's non-permanence risk mitigation, including buffer pool deposits, releases, and reversal coverage, along with the project's overall risk profile.

The current **Durability & Permanence JSON** can be found [HERE](https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/blob/main/json_schema/Durability_Permanence.schema.json).

## Project Finance

The Project Finance schema aims to capture all relevant information related to a project's financing, including financing options, expected and realized costs/revenue, funding requirements, offtake and insurance agreements, and other transactional details between the project and its counterparties.

The current **Project Finance JSON** can be found [HERE](https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/blob/main/json_schema/Project_Finance.schema.json).

## Labels & Certifications

The Labels & Certifications schema aims to capture labels and certifications at the standard, project, and unit levels. Greater granularity is reserved for the project and unit level with distinctions made based on the respective object. 

The current **Labels & Certifications JSON** can be found [HERE](https://github.com/Carbon-Data-Open-Protocol/Carbon-Data-Open-Protocol/blob/main/json_schema/Labels_Certifications.schema.json).


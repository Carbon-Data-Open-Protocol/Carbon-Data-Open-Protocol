# Governance Outline

## Areas of work

This document provides guidance on effective interaction with data schema content stored in this GitHub repository. It is organised around three primary areas of work: schema development, documentation and thought leadership, and interaction with the public. By detailing the processes and best practices relevant to each of these areas, we aim to support users in maintaining high standards of quality, transparency, and collaboration throughout the lifecycle of schema management.

### Schema development

The main objective within schema development is to design and refine the carbon market schema, ensuring that all relevant data structures are accurately represented and maintained. The outputs of this work are primarily stored as Excel files, JSON files, and may include other formats as needed to support interoperability and user requirements.

The development workflow follows a collaborative version control process. Team members typically create dedicated branches for specific tasks or features, allowing work to progress in isolation from the main codebase. Files are checked out from the repository, updated or extended as appropriate, and then checked back in once edits are complete. Changes are proposed via pull requests, which enable peer review and quality assurance before merging updates into the main branch. This approach supports robust change tracking, encourages collaborative review, and ensures the integrity of the schema across its lifecycle.

### Documentation and thought leadership

Within the realm of documentation and thought leadership, it is essential to produce comprehensive records that articulate the rationale behind each element of the carbon market data schema, including detailed explanations for entities, fields, and other relevant concepts. Every modification to the schema should be accompanied by updated documentation, ensuring continuity and enabling other community members to easily understand and build upon previous work. Additionally, publishing articles and blog posts on specific topics not only enriches the repository but also provides valuable context for users, fostering a culture of transparency and shared expertise.

### Interaction with the public

We plan to utilise GitHub’s Issues and Discussions facilities to enable interaction with the community. GitHub Issues are designed to track tasks, report bugs, or suggest enhancements related to the data schema and its associated resources. Community members or contributors can create new issues to raise questions, flag errors, or request new features. Each issue can be discussed through comments, assigned to team members, labelled for categorisation, and tracked until resolution, providing a transparent and organised workflow for managing feedback and improvements.

GitHub Discussions, on the other hand, serve as a forum for broader conversations that may not fit within the scope of a specific issue. They provide a space for open-ended dialogue, including Q&A, sharing ideas, or seeking advice from other users and contributors. Discussions can be categorised, searched, and referenced in documentation, making them an effective tool for building knowledge and fostering a collaborative community spirit. To participate, users simply navigate to the 'Discussions' tab, start a new topic, or join an existing thread to contribute their thoughts.

By leveraging both Issues and Discussions, we aim to ensure that feedback, support, and collaborative thinking are easily accessible, well-documented, and integrated into our ongoing schema development and documentation efforts.

## Roles

In the context of maintaining the carbon market schema project on GitHub, the following four roles are essential for ensuring effective collaboration, quality assurance, and transparent development:

Administrator: Administrators oversee the overall management of the carbon market schema project on GitHub, ensuring that collaboration and operations run smoothly. They are responsible for configuring repository settings, managing permissions for other roles, and maintaining the integrity and security of the project. Administrators may also coordinate releases, resolve conflicts, and enforce compliance with workflow and documentation standards, providing essential leadership and support to the contributor community.

Reviewer: Reviewers are responsible for assessing proposed changes, typically via pull requests, to ensure they meet the project's standards for accuracy, completeness, and style. They provide constructive feedback, request clarifications or improvements, and ultimately approve or reject changes before they are merged into the main branch. Reviewers play a key role in maintaining the integrity of the schema and ensuring that all updates are well-documented and thoroughly vetted.

Contributor: Contributors actively participate in developing the schema by creating new features, fixing bugs, or refining documentation. They work on dedicated branches, submit pull requests for their changes, and engage in discussions to address feedback from reviewers and other team members. Contributors are instrumental in driving the project forward and are expected to follow collaborative workflows, version control practices, and documentation standards.

Viewer: Viewers primarily observe the project's progress, access documentation, and stay informed about ongoing developments. While they do not directly contribute code or documentation, viewers may participate in GitHub Issues and Discussions by asking questions, reporting problems, or suggesting ideas. Their engagement helps ensure the project remains accessible and responsive to broader community needs.

It's worth noting, that Contributor and Reviewer roles can be assigned to one and the same user but Contributors should not be reviewing their own work.

Together, these roles support a collaborative and well-structured approach to project maintenance, ensuring that the carbon market schema evolves in line with user requirements and best practices.

## Workflow

### Carbon Market Schema Change Workflow

The following workflow outlines the collaborative process for making changes to the carbon market schema, updating documentation, and merging approved updates into the main branch. Each role—Administrator, Reviewer, Contributor, and Viewer—has distinct responsibilities that ensure the project remains robust, transparent, and responsive to community needs.

- Branch Creation and File Checkout
The Contributor begins by creating a new branch from the main repository, ensuring their work remains isolated and traceable. The Administrator may assist in configuring branch permissions and verifying that the Contributor has access to necessary files and tools.
- Schema and Documentation Updates
On the new branch, the Contributor makes targeted changes to the schema and updates accompanying documentation to reflect any modifications. This step includes refining features, resolving bugs, and ensuring all changes are accurately documented for future reference.
- Committing and Pushing Changes
Upon completion, the Contributor commits their updates with clear messages and pushes the branch to the remote repository. Adherence to version control standards and descriptive commit logs is essential for maintaining transparency.
- Pull Request Submission
The Contributor initiates a pull request (PR), summarising the proposed changes and referencing updated documentation. This formal request signals readiness for review and invites feedback from the project team.
- Review of Changes
The Reviewer examines the pull request, assessing both code and documentation for accuracy, completeness, and alignment with project standards. Constructive feedback may be provided, and the Contributor addresses any requested revisions. The Reviewer ensures that Contributors do not review their own submissions, upholding impartiality.
- Merging Approved Changes
Once the Reviewer is satisfied, they approve the pull request. The Administrator then finalises the merge into the main branch, updating repository settings as needed and coordinating any necessary releases or notifications.
- Viewer Engagement and Feedback
Viewers observe the progress through GitHub Issues or Discussions, offering feedback, reporting potential problems, and suggesting future improvements. Their participation keeps the project accessible and ensures that updates are responsive to the wider community.

In summary, this workflow fosters a collaborative environment where each role contributes to the quality and transparency of the carbon market schema. By following these structured steps, the project team ensures that updates are well-managed, thoroughly reviewed, and openly communicated to all stakeholders.

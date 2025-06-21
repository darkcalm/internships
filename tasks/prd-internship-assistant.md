# Product Requirements Document: AI-Powered Internship Assistant v2.0

## 1. Overview

This document outlines the requirements for the AI-Powered Internship Assistant, a tool designed to help users generate highly personalized motivation letters by intelligently mapping their personal experience to job descriptions. This version (2.0) is a complete re-architecture focused on a modular, iterative, and AI-centric workflow, providing maximum flexibility and power to the user.

The system is built on a four-stage pipeline. The user can execute these stages independently and iteratively, refining the data at each step until a satisfactory result is achieved.

## 2. Core Stages

### Stage 1: Applicant Profile Generation
-   **Input:** Raw user data (e.g., HTML export from a job portal, PDF resume, Markdown file).
-   **Process:**
    1.  **Sanitization & Expansion (Scripted/User):** Converts various input formats (HTML, PDF) into clean Markdown. Provides a hook for the user to manually add or edit information.
    2.  **Structured Transformation (AI):** Uses an LLM to parse the clean text and transform it into a structured `personal_data.json` file, guided by a predefined schema.
-   **Output:** A validated `personal_data.json` file.

### Stage 2: Job Description Generation
-   **Input:** A job description (e.g., Markdown file, URL, raw text).
-   **Process:**
    1.  **Sanitization & Expansion (AI/User):** Sanitizes the input. Critically, it uses an AI-powered step to research and expand upon the provided description, gathering more context about the company, the role, and required skills. The user can also manually add details.
    2.  **Structured Transformation (AI):** Uses an LLM to parse the augmented text and transform it into a structured `job_data.json` file, guided by a schema.
-   **Output:** A validated `job_data.json` file.

### Stage 3: Interactive Mapping
-   **Input:** `personal_data.json` and `job_data.json`.
-   **Process:**
    1.  **AI-Powered Mapping:** Performs a semantic comparison between the applicant's profile and the job description to identify relevant connections. The AI provides reasoning for each connection.
    2.  **Interactive Refinement (User):** Presents the proposed mappings to the user in a clear terminal UI. The user can accept, reject, or request regeneration. If the user finds the mappings weak, they can loop back to Stage 1 or 2 to provide more data.
-   **Output:** A user-confirmed `mappings.json` file.

### Stage 4: Composition
-   **Input:** `mappings.json`.
-   **Process:**
    1.  **Letter Synthesis (Scripted):** Uses the confirmed mappings and a templating engine (e.g., Jinja2) to compose the final motivation letter.
    2.  **Final Review (User):** Presents the generated letter to the user for final approval before saving.
-   **Output:** A `motivation_letter.md` file.

## 3. Key Features
-   **Iterative Workflow:** The user is not locked into a linear process. They can re-run stages with expanded data until the mapping is perfect.
-   **Modular Architecture:** Each stage is a self-contained unit with clear inputs and outputs, making the system easy to maintain and extend.
-   **Human-in-the-Loop:** The user has final say at critical junctures (data expansion, mapping confirmation, final letter approval).
-   **AI-Driven Expansion:** The system goes beyond simple parsing by actively augmenting the available data to create richer, more meaningful connections.
-   **Schema-Guided Transformation:** LLM outputs are constrained by schemas, ensuring data integrity and reliability.

## 4. Goals
- To automate the writing of application documents tailored to specific internship positions.
- To create a reusable and adaptable pipeline that can be used for different individuals and roles by simply updating the input data.
- The core output will be the generated written materials, ready for review and use.

## 5. User Stories
- **As a user, I want to** provide my personal data (e.g., CV, skills, experiences) so the system can generate a personalized motivation letter.
- **As a user, I want to** input a specific job description so the system can tailor the generated documents to the requirements of the role.
- **As a user, I want to** receive a well-formatted text document that I can easily review, edit, and finalize.

## 6. Functional Requirements
- The system must ingest personal data from a user-provided source.
- The system must ingest external job data from sources like PDF (`Internship Roster.pdf`) and HTML (`Job Submission - Internship Roster (Job Number- 25001-INT).html`).
- The system must generate a motivation letter by synthesizing information from both the personal and external data sources.
- The process must be designed to be modular, allowing for easy updates to personal or job-related data for new applications.

## 7. Non-Goals (Out of Scope)
- The project will **not** automatically submit applications to job portals.
- The project is **not** responsible for searching or finding job opportunities.
- The scope is strictly limited to the document writing process. Other aspects of the job application, such as online form-filling or interview preparation, are not included.

## 8. Design Considerations
- A clear separation should be maintained between data input, the processing/generation engine, and the final output to ensure modularity and ease of maintenance.

## 9. Technical Considerations
- A Python virtual environment will be used for dependency management.
- The system will need components to parse PDF, HTML, and the user's personal data format.
- A robust templating engine could be used to structure the generated motivation letter.

## 10. Success Metrics
- The generated motivation letter is coherent, personalized, and highly relevant to the target job description.
- The time required to draft a custom motivation letter is significantly reduced.
- The pipeline can be successfully reapplied to a different job application with minimal friction.

## 11. Open Questions
- What is the expected format for the user's personal data (e.g., JSON, YAML, Markdown)?
- What logic will be used to map the user's skills and experiences to the requirements listed in a job description?
- Will this tool be operated via a command-line interface, or is a graphical user interface planned for the future? 
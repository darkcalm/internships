# Task List: AI-Powered Internship Assistant v2.0

[x] 1.0 Parent Task: Foundational Setup
- [x] 1.1 Create the main controller (`main.py`) with a menu-driven interface to select and execute different stages (e.g., "Process Personal Info", "Process Job Data", "Run Mapping", "Generate Letter").
- [x] 1.2 Establish the project's data schema definitions by creating a `data/schemas/` directory.
- [x] 1.3 Create the initial `data/schemas/personal_data_schema.json` and `data/schemas/job_data_schema.json` files. These will serve as the ground truth for our AI transformations.

[x] 2.0 Parent Task: Stage 1 - Sanitization (HTML/PDF -> MD)
- [x] 2.1 Create a `util/sanitizer.py` module with functions to convert both HTML and PDF files into clean Markdown.
- [x] 2.2 In `main.py`, implement the full sanitization logic in the `run_sanitization()` function.
    - [x] 2.2.1 Process the selected personal info file and save it to `data/temp/personal.md`.
    - [x] 2.2.2 Process the selected job description file and save it to `data/temp/job.md`.
    - [x] 2.2.3 After sanitization, present the paths to the user and prompt for an optional manual review/edit loop for each file.

[ ] 3.0 Parent Task: Stage 2 - Transformation (MD -> JSON)
- [ ] 3.1 Create a `util/transformer.py` module with a function `transform_to_json(source_text, schema)`.
- [ ] 3.2 In `util/transformer.py`, create an AI-powered `expand_job_description(text)` function that researches and augments the job text.
- [ ] 3.3 In `main.py`, implement the `run_transformation()` flow.
    - [ ] 3.3.1 Load the sanitized `personal.md`.
    - [ ] 3.3.2 Use the transformer to produce `data/personal_data.json`.
    - [ ] 3.3.3 Load the sanitized `job.md`.
    - [ ] 3.3.4 Use the `expand_job_description` function.
    - [ ] 3.3.5 Use the transformer to produce `data/job_data.json`.
    - [ ] 3.3.6 Implement a review/refine loop for the generated JSON files.

[ ] 4.0 Parent Task: Stage 3 - Interactive Mapping
- [ ] 4.1 Create a `util/mapper.py` module.
- [ ] 4.2 In `util/mapper.py`, implement `generate_mappings(personal_data, job_data)` which uses semantic search to compare the two JSON files and output a `data/mappings.json` file.
- [ ] 4.3 Create a `util/ui.py` module for the interactive terminal UI.
- [ ] 4.4 In `util/ui.py`, implement `display_mappings` and `confirm_mappings` to create the interactive review loop.
- [ ] 4.5 In `main.py`, implement the "Run Mapping" flow that calls the mapper and then enters the UI review loop.

[ ] 5.0 Parent Task: Stage 4 - Composition & Finalization
- [ ] 5.1 Create a `util/composer.py` module.
- [ ] 5.2 In `util/composer.py`, implement `generate_letter(mappings)` which uses a Jinja2 template to create the letter.
- [ ] 5.3 Create a `templates/letter_template.md` file with placeholders.
- [ ] 5.4 In `main.py`, implement the "Generate Letter" flow that uses the composer and presents the final text for approval before saving to `deliverables/`.
- [ ] 5.5 Finalize project documentation (`README.md`, docstrings) and perform a full end-to-end test.

## Deliverables

- `deliverables/motivation_letter_25001-INT.md` - The final, generated motivation letter for the specified job.
- `data/personal_data.json` - A file containing the user's structured personal information, *generated* from the HTML source.
- `data/mappings.json` - A user-editable file to refine the connections between personal data and job requirements.
- `util/data_parser.py` - A Python module for parsing the job roster Markdown file.
- `util/transformer.py` - A Python module to transform the raw job submission HTML into structured personal data using an LLM.
- `util/letter_generator.py` - A Python module containing the core logic for generating the letter content.
- `main.py` - The main script to execute the entire interactive pipeline.
- `README.md`
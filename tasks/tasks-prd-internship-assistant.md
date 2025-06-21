# Task List: AI-Powered Internship Assistant v2.0

## 1.0 Parent Task: Foundational Setup
- [x] 1.1 Create the main controller (`main.py`) with a menu that separates System Actions from User Agency.
- [x] 1.2 Establish the project's data schema definitions by creating a `data/schemas/` directory.
- [x] 1.3 Create the initial `data/schemas/personal_data_schema.json` and `data/schemas/job_data_schema.json` files.

[x] 2.0 Parent Task: Stage 1 - Sanitization (System Action)
- [x] 2.1 Create a `util/sanitizer.py` module with functions to convert both HTML and PDF files into clean Markdown.
- [x] 2.2 In `main.py`, implement the `run_sanitization()` function.

[x] 3.0 Parent Task: Stage 2 - Expansion (System Action)
- [x] 3.1 Create a `prompts/expand_prompt.txt` file.
- [x] 3.2 In `util/transformer.py`, create an `expand_job_description()` function.
- [x] 3.3 In `main.py`, implement the `run_expansion()` flow.

[x] 4.0 Parent Task: Stage 3 - Transformation (System Action)
- [x] 4.1 Create a `util/transformer.py` module and a `prompts/transform_prompt.txt` file.
- [x] 4.2 In `main.py`, implement the `run_transformation()` flow.

[x] 5.0 Parent Task: User Agency - Manual Overrides
- [x] 5.1 In `main.py`, implement the dynamic menu that lists editable files.
- [x] 5.2 Implement the controller logic to handle user selections for editing files.

[ ] 6.0 Parent Task: Stage 4 - Mapping (Discovery)
- [x] 6.1 Update `util/mapper.py` to remove the similarity threshold, ensuring all potential mappings are discovered.
- [x] 6.2 Create `prompts/reasoning_prompt.txt` with instructions for the AI to act as a career coach and explain the causal link between an experience and a requirement.
- [x] 6.3 Update `generate_mappings()` to use a second LLM call, guided by the new prompt, to generate a 'reasoning' string for each potential match.
- [x] 6.4 In `main.py`, update the "Generate Mappings" flow to reflect the new mapper logic.

[x] 7.0 Parent Task: Stage 5 - Composition & Finalization
- [x] 7.1 Create a `util/composer.py` module and a `templates/letter_template.md` file.
- [x] 7.2 In `main.py`, implement the "Compose Letter" flow.
- [x] 7.3 Finalize project documentation and perform end-to-end testing.

## Deliverables

- `deliverables/motivation_letter_25001-INT.md` - The final, generated motivation letter for the specified job.
- `data/personal_data.json` - A file containing the user's structured personal information, *generated* from the HTML source.
- `data/mappings.json` - A user-editable file to refine the connections between personal data and job requirements.
- `util/data_parser.py` - A Python module for parsing the job roster Markdown file.
- `util/transformer.py` - A Python module to transform the raw job submission HTML into structured personal data using an LLM.
- `util/letter_generator.py` - A Python module containing the core logic for generating the letter content.
- `main.py` - The main script to execute the entire interactive pipeline.
- `README.md`
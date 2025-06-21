# main.py
# This file is the main controller for the AI-Powered Internship Assistant.
# It provides a menu-driven interface to orchestrate the different stages of the process.

import os
from dotenv import load_dotenv

# Load environment variables from .env file at the very beginning
load_dotenv()

from util.sanitizer import sanitize_html_to_markdown, sanitize_pdf_to_markdown
from util.transformer import transform_to_json, expand_job_description
import json

# --- Helper Functions ---

def get_files_in_dir(directory: str, extensions: tuple = ('.html', '.pdf', '.md')) -> list[str]:
    """Scans a directory and returns a list of files with given extensions."""
    try:
        return [f for f in os.listdir(directory) if f.lower().endswith(extensions)]
    except FileNotFoundError:
        return []

def get_data_status(raw_dir: str, temp_path: str, final_path: str) -> str:
    """Determines the processing status of a data pipeline."""
    if os.path.exists(final_path):
        return "Transformed"
    elif os.path.exists(temp_path):
        return "Sanitized"
    elif get_files_in_dir(raw_dir):
        return "Raw"
    else:
        return "Missing"

def select_file_from_dir(directory: str, prompt_message: str, extensions: tuple) -> str | None:
    """Scans a directory for specific file types, lists them, and asks the user to select one."""
    files = get_files_in_dir(directory, extensions)
    if not files:
        print(f"No compatible files {extensions} found in '{directory}'.")
        return None
    if len(files) == 1:
        return os.path.join(directory, files[0])

    print(prompt_message)
    for i, filename in enumerate(files):
        print(f"{i + 1}. {filename}")
    while True:
        try:
            choice = int(input(f"Enter your choice (1-{len(files)}): ")) - 1
            if 0 <= choice < len(files):
                return os.path.join(directory, files[choice])
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# --- Stage-Specific Logic ---

def run_sanitization():
    """Handles Stage 1a & 2a: Sanitizing raw data to Markdown."""
    print("\n--- Running Sanitization ---")
    
    # --- Sanitize Personal Info ---
    personal_dir = "external/personal info"
    personal_temp_path = "data/temp/personal.md"
    personal_raw_path = select_file_from_dir(personal_dir, "Select a personal info file to sanitize:", ('.html', '.pdf'))
    
    if personal_raw_path:
        print(f"Sanitizing '{os.path.basename(personal_raw_path)}'...")
        try:
            if personal_raw_path.lower().endswith('.html'):
                content = sanitize_html_to_markdown(personal_raw_path)
            else: # .pdf
                content = sanitize_pdf_to_markdown(personal_raw_path)
            
            with open(personal_temp_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Successfully sanitized to '{personal_temp_path}'")
        except Exception as e:
            print(f"Error sanitizing personal info: {e}")

    # --- Sanitize Job Description ---
    job_dir = "external/job description"
    job_temp_path = "data/temp/job.md"
    job_raw_path = select_file_from_dir(job_dir, "Select a job description file to sanitize:", ('.html', '.pdf', '.md'))
    
    if job_raw_path:
        print(f"Sanitizing '{os.path.basename(job_raw_path)}'...")
        try:
            if job_raw_path.lower().endswith('.html'):
                content = sanitize_html_to_markdown(job_raw_path)
            elif job_raw_path.lower().endswith('.pdf'):
                content = sanitize_pdf_to_markdown(job_raw_path)
            else: # .md
                # If it's already a markdown file, just copy it
                import shutil
                shutil.copy(job_raw_path, job_temp_path)
                content = "Copied existing markdown file."

            if not job_raw_path.lower().endswith('.md'):
                 with open(job_temp_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            print(f"Successfully sanitized to '{job_temp_path}'")
        except Exception as e:
            print(f"Error sanitizing job description: {e}")

    print("\n--- Sanitization Complete ---")
    print("You can now review the generated markdown files in 'data/temp/'.")


def run_transformation():
    """Handles Stage 1b & 2b: Transforming sanitized Markdown to structured JSON."""
    print("\n--- Running Transformation (MD -> JSON) ---")
    
    # Define paths
    personal_md_path = "data/temp/personal.md"
    job_md_path = "data/temp/job_expanded.md"
    personal_schema_path = "data/schemas/personal_data_schema.json"
    job_schema_path = "data/schemas/job_data_schema.json"
    personal_json_path = "data/personal_data.json"
    job_json_path = "data/job_data.json"
    transform_prompt_file = "prompts/transform_prompt.txt"

    # --- Transform Personal Data ---
    if os.path.exists(personal_md_path):
        print(f"Found sanitized personal data at '{personal_md_path}'.")
        try:
            with open(personal_md_path, 'r', encoding='utf-8') as f:
                personal_text = f.read()
            with open(personal_schema_path, 'r', encoding='utf-8') as f:
                personal_schema = json.load(f)
            
            print("Transforming personal data with LLM...")
            personal_json = transform_to_json(personal_text, personal_schema, transform_prompt_file)

            with open(personal_json_path, 'w', encoding='utf-8') as f:
                json.dump(personal_json, f, indent=4)
            print(f"Successfully transformed personal data to '{personal_json_path}'.")

        except Exception as e:
            print(f"An error occurred during personal data transformation: {e}")
    else:
        print("No sanitized personal data found to transform. Please run Sanitization first.")

    # --- Transform Job Data ---
    if os.path.exists(job_md_path):
        print(f"Found expanded job data at '{job_md_path}'.")
        try:
            with open(job_md_path, 'r', encoding='utf-8') as f:
                job_text = f.read()
            with open(job_schema_path, 'r', encoding='utf-8') as f:
                job_schema = json.load(f)

            print("Transforming job data with LLM...")
            job_json = transform_to_json(job_text, job_schema, transform_prompt_file)

            with open(job_json_path, 'w', encoding='utf-8') as f:
                json.dump(job_json, f, indent=4)
            print(f"Successfully transformed job data to '{job_json_path}'.")
            
        except Exception as e:
            print(f"An error occurred during job data transformation: {e}")
    else:
        print("No expanded job description found to transform. Please run Expansion first.")

    print("\n--- Transformation Complete ---")
    print("You can now review the generated JSON files in 'data/'.")


def run_expansion():
    """Handles the AI-powered expansion of job descriptions."""
    print("\n--- Running Expansion (MD -> Augmented MD) ---")
    
    # Define paths
    job_md_path = "data/temp/job.md"
    expanded_job_md_path = "data/temp/job_expanded.md"
    expand_prompt_file = "prompts/expand_prompt.txt"

    if not os.path.exists(job_md_path):
        print(f"Sanitized job description not found at '{job_md_path}'. Please run Sanitization first.")
        return

    try:
        with open(job_md_path, 'r', encoding='utf-8') as f:
            job_text = f.read()

        print("Expanding job description with LLM...")
        expanded_text = expand_job_description(job_text, expand_prompt_file)

        with open(expanded_job_md_path, 'w', encoding='utf-8') as f:
            f.write(expanded_text)
        print(f"Successfully saved expanded job description to '{expanded_job_md_path}'.")

        print("\n--- Expansion Complete ---")
        print("You can now review the expanded markdown file in 'data/temp/'.")

    except Exception as e:
        print(f"An error occurred during job description expansion: {e}")


# --- Main Controller ---

def display_menu():
    """Prints a dynamic, state-aware menu to the console."""
    print("\n--- AI-Powered Internship Assistant ---")
    
    personal_status = get_data_status("external/personal info", "data/temp/personal.md", "data/personal_data.json")
    job_status = get_data_status("external/job description", "data/temp/job.md", "data/job_data.json")
    job_expansion_status = "Expanded" if os.path.exists("data/temp/job_expanded.md") else "Not Expanded"

    print(f"Personal Data: {personal_status} | Job Data: {job_status} ({job_expansion_status})\n")
    
    print("--- System Actions ---")
    print("1. Run Sanitization (Raw -> MD)")
    print("2. Run Expansion (Job MD -> Augmented MD)")
    print("3. Run Transformation (MD -> JSON)")
    print("4. Generate Mappings")
    print("5. Compose Letter")
    print("---------------------------------------")

    # User Agency Menu
    print("--- Manual Overrides ---")
    edit_options = {}
    if os.path.exists("data/temp/personal.md"):
        edit_options['e1'] = ("Edit Sanitized Personal Data", "data/temp/personal.md")
    if os.path.exists("data/temp/job_expanded.md"):
        edit_options['e2'] = ("Edit Expanded Job Data", "data/temp/job_expanded.md")
    else:
        if os.path.exists("data/temp/job.md"):
            edit_options['e2'] = ("Edit Sanitized Job Data", "data/temp/job.md")
    if os.path.exists("data/personal_data.json"):
        edit_options['e3'] = ("Edit Transformed Personal Data", "data/personal_data.json")
    if os.path.exists("data/job_data.json"):
        edit_options['e4'] = ("Edit Transformed Job Data", "data/job_data.json")
    
    if not edit_options:
        print("No editable files generated yet. Run a system action first.")
    else:
        for key, (text, _) in edit_options.items():
            print(f"{key}. {text}")

    print("exit - Exit the application")
    print("---------------------------------------")
    return edit_options

def main():
    """Main function to run the menu-driven application."""
    while True:
        edit_options = display_menu()
        choice = input("Enter your choice: ").strip().lower()

        if choice == '1':
            run_sanitization()
        elif choice == '2':
            run_expansion()
        elif choice == '3':
            run_transformation()
        elif choice == '4':
            print("\nExecuting: Generate Mappings...")
            print("Stage 4 not yet implemented.")
        elif choice == '5':
            print("\nExecuting: Compose Letter...")
            print("Stage 5 not yet implemented.")
        elif choice in edit_options:
            file_to_edit = edit_options[choice][1]
            print(f"\nOpening '{file_to_edit}' for manual review.")
            input("The system will now pause. Please open and edit the file directly.\nPress Enter when you are done to return to the menu...")
        elif choice == 'exit':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main() 
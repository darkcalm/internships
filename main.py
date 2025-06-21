# main.py
# This file is the main controller for the AI-Powered Internship Assistant.
# It provides a menu-driven interface to orchestrate the different stages of the process.

import os
from util.sanitizer import sanitize_html_to_markdown, sanitize_pdf_to_markdown

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

def prompt_for_edit(file_path: str):
    """Asks the user if they want to manually edit a file."""
    while True:
        edit_choice = input(f"Would you like to manually edit the sanitized file at '{file_path}'? (y/n): ").lower().strip()
        if edit_choice in ['y', 'yes']:
            input("Please open the file, make your edits, and save it. Press Enter when you are done...")
            print(f"Continuing with the potentially edited '{file_path}'.")
            break
        elif edit_choice in ['n', 'no']:
            print(f"Proceeding with '{file_path}' as is.")
            break
        else:
            print("Invalid choice. Please enter 'y' or 'n'.")

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

    print("\n--- Sanitization Complete: Review Optional ---")
    if os.path.exists(personal_temp_path):
        prompt_for_edit(personal_temp_path)
    if os.path.exists(job_temp_path):
        prompt_for_edit(job_temp_path)


def run_transformation():
    """Handles Stage 1b & 2b: Transforming sanitized Markdown to structured JSON."""
    print("\n--- Running Transformation (MD -> JSON) ---")
    print("This stage is not yet implemented.")


# --- Main Controller ---

def display_menu():
    """Prints a dynamic, state-aware menu to the console."""
    print("\n--- AI-Powered Internship Assistant ---")
    
    personal_status = get_data_status("external/personal info", "data/temp/personal.md", "data/personal_data.json")
    job_status = get_data_status("external/job description", "data/temp/job.md", "data/job_data.json")

    print(f"Personal Data Status: {personal_status} | Job Data Status: {job_status}\n")

    print("1. Sanitize Raw Data (HTML/PDF -> MD)")
    print("2. Transform Sanitized Data (MD -> JSON)")
    print("3. Generate & Review Mappings")
    print("4. Compose Letter")
    print("---------------------------------------")
    print("exit - Exit the application")
    print("---------------------------------------")

def main():
    """Main function to run the menu-driven application."""
    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            run_sanitization()
        elif choice == '2':
            run_transformation()
        elif choice == '3':
            print("\nExecuting Stage 3: Generate & Review Mappings...")
            print("Stage 3 not yet implemented.")
        elif choice == '4':
            print("\nExecuting Stage 4: Compose Motivation Letter...")
            print("Stage 4 not yet implemented.")
        elif choice.lower() == 'exit':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")

if __name__ == "__main__":
    main() 
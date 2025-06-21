# util/composer.py
# This module composes the final motivation letter using the generated data and a template.

import json
from jinja2 import Environment, FileSystemLoader
import os

def generate_letter(template_path: str, mappings_path: str, personal_data_path: str, job_data_path: str) -> str:
    """
    Generates a motivation letter from a template and structured data.

    Args:
        template_path: The path to the Jinja2 template file.
        mappings_path: The path to the mappings.json file.
        personal_data_path: The path to the personal_data.json file.
        job_data_path: The path to the job_data.json file.

    Returns:
        A string containing the composed motivation letter.
    """
    try:
        with open(mappings_path, 'r', encoding='utf-8') as f:
            mappings = json.load(f)
        with open(personal_data_path, 'r', encoding='utf-8') as f:
            personal_data = json.load(f)
        with open(job_data_path, 'r', encoding='utf-8') as f:
            job_data = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: Could not find a required data file. {e.filename}")

    # Set up the Jinja2 environment
    template_dir = os.path.dirname(template_path)
    template_filename = os.path.basename(template_path)
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_filename)

    # Render the template with the loaded data
    composed_letter = template.render(
        personal_data=personal_data,
        job_details=job_data.get("jobDetails", {}),
        mappings=mappings
    )

    return composed_letter 
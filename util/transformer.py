# util/transformer.py
# This module uses an LLM to transform sanitized text into a structured JSON object.

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check for the API key at import time to fail early
if not os.getenv("OPENAI_API_KEY"):
    raise EnvironmentError("OPENAI_API_KEY environment variable not found.")

client = OpenAI()

def load_prompt_from_file(prompt_file_path: str) -> str:
    """Loads a prompt from a text file."""
    try:
        with open(prompt_file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt file not found at: {prompt_file_path}")

def transform_to_json(source_text: str, schema: dict, prompt_file: str) -> dict:
    """
    Transforms unstructured text into a structured JSON object using an LLM,
    guided by a schema and an external prompt file.

    Args:
        source_text: The sanitized text content to be transformed.
        schema: The JSON schema to guide the transformation.
        prompt_file: The path to the file containing the system prompt.

    Returns:
        A dictionary containing the structured data.
    """
    print(f"Loading system prompt from {prompt_file}...")
    system_prompt_template = load_prompt_from_file(prompt_file)
    system_prompt = system_prompt_template + f"\n\nJSON Schema:\n{json.dumps(schema, indent=2)}"

    user_prompt = f"""
    Please parse the following text and convert it into a JSON object according to the schema and rules I provided.

    Text to parse:
    ---
    {source_text}
    ---
    """

    print("Requesting transformation from OpenAI API...")
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        response_content = completion.choices[0].message.content
        print("Successfully received and parsed response from API.")
        return json.loads(response_content)

    except Exception as e:
        print(f"An error occurred while communicating with the OpenAI API: {e}")
        raise

def expand_job_description(source_text: str, prompt_file: str) -> str:
    """
    Expands a job description using an LLM to add more context and detail.

    Args:
        source_text: The sanitized text of the job description.
        prompt_file: The path to the file containing the system prompt for expansion.

    Returns:
        A string containing the augmented Markdown text.
    """
    print(f"Loading expansion prompt from {prompt_file}...")
    system_prompt = load_prompt_from_file(prompt_file)

    user_prompt = f"""
    Please expand the following job description based on the rules I provided.

    Job Description to expand:
    ---
    {source_text}
    ---
    """

    print("Requesting expansion from OpenAI API...")
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        expanded_text = completion.choices[0].message.content
        print("Successfully received expansion from API.")
        return expanded_text

    except Exception as e:
        print(f"An error occurred while communicating with the OpenAI API: {e}")
        raise 
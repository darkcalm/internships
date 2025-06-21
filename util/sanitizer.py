# util/sanitizer.py
# This module contains functions for converting different file formats into clean Markdown.

import html2text
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
import asyncio

def sanitize_html_to_markdown(html_file_path: str) -> str:
    """
    Reads an HTML file and converts its content to Markdown.

    Args:
        html_file_path: The path to the input HTML file.

    Returns:
        A string containing the Markdown content.
    """
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        markdown_content = h.handle(html_content)
        return markdown_content
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file at {html_file_path} was not found.")
    except Exception as e:
        raise RuntimeError(f"An error occurred during HTML to Markdown conversion: {e}")

def sanitize_pdf_to_markdown(pdf_file_path: str) -> str:
    """
    Reads a PDF file and converts its content to Markdown using the marker library.
    This function uses the new class-based approach.

    Args:
        pdf_file_path: The path to the input PDF file.

    Returns:
        A string containing the Markdown content.
    """
    try:
        # The marker library is async, so we need to run it in an event loop.
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        converter = PdfConverter(
            artifact_dict=create_model_dict(),
        )
        rendered = converter(pdf_file_path)
        text, _, _ = text_from_rendered(rendered)
        
        return text
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file at {pdf_file_path} was not found.")
    except Exception as e:
        raise RuntimeError(f"An error occurred during PDF to Markdown conversion: {e}")

if __name__ == '__main__':
    # Example usage for testing purposes
    # Note: These tests require the example files to exist in the specified paths.
    
    # Test HTML conversion
    try:
        html_path = 'external/JobSubmission.html'
        print(f"--- Testing HTML Sanitization on {html_path} ---")
        md_from_html = sanitize_html_to_markdown(html_path)
        print(md_from_html[:500] + "...") # Print first 500 chars
        print("\nHTML conversion successful.\n")
    except (FileNotFoundError, RuntimeError) as e:
        print(e)

    # Test PDF conversion
    try:
        pdf_path = 'external/Internship Roster.pdf'
        print(f"--- Testing PDF Sanitization on {pdf_path} ---")
        md_from_pdf = sanitize_pdf_to_markdown(pdf_path)
        print(md_from_pdf[:500] + "...") # Print first 500 chars
        print("\nPDF conversion successful.\n")
    except (FileNotFoundError, RuntimeError) as e:
        print(e) 
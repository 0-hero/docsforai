"""
Converter for Jupyter Notebook to Markdown.
"""

import logging
import json
from nbconvert import MarkdownExporter
import nbformat

logger = logging.getLogger(__name__)

def ipynb_to_md(ipynb_content: str) -> str:
    """
    Convert Jupyter Notebook to Markdown.

    Args:
        ipynb_content (str): Jupyter Notebook content as JSON string.

    Returns:
        str: Converted Markdown content.

    Raises:
        ValueError: If conversion fails.
    """
    try:
        notebook = nbformat.reads(ipynb_content, as_version=4)
        exporter = MarkdownExporter()
        markdown, _ = exporter.from_notebook_node(notebook)
        return markdown
    except json.JSONDecodeError as e:
        logger.error(f"Invalid Jupyter Notebook JSON: {str(e)}")
        raise ValueError("Invalid Jupyter Notebook format") from e
    except Exception as e:
        logger.error(f"Error converting Jupyter Notebook to Markdown: {str(e)}")
        raise ValueError("Failed to convert Jupyter Notebook to Markdown") from e
"""
Converter for AsciiDoc to Markdown.
"""

import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

def adoc_to_md(adoc_content: str) -> str:
    """
    Convert AsciiDoc to Markdown.

    Args:
        adoc_content (str): AsciiDoc content.

    Returns:
        str: Converted Markdown content.

    Raises:
        ValueError: If conversion fails.
    """
    try:
        # Use Pandoc for conversion
        result = subprocess.run(
            ['pandoc', '-f', 'asciidoc', '-t', 'markdown'],
            input=adoc_content,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Error converting AsciiDoc to Markdown: {e.stderr}")
        raise ValueError("Failed to convert AsciiDoc to Markdown") from e
    except FileNotFoundError:
        logger.error("Pandoc is not installed or not in PATH")
        raise ValueError("Pandoc is required for AsciiDoc to Markdown conversion")
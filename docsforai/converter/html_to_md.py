"""
Converter for HTML to Markdown.
"""

import logging
from bs4 import BeautifulSoup
import html2text

logger = logging.getLogger(__name__)

def html_to_md(html_content: str) -> str:
    """
    Convert HTML to Markdown. Args:
        html_content (str): HTML content.

    Returns:
        str: Converted Markdown content.

    Raises:
        ValueError: If conversion fails.
    """
    try:
        # Clean the HTML using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        clean_html = soup.prettify()

        # Convert to Markdown using html2text
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        h.ignore_tables = False
        markdown = h.handle(clean_html)

        return markdown.strip()
    except Exception as e:
        logger.error(f"Error converting HTML to Markdown: {str(e)}")
        raise ValueError("Failed to convert HTML to Markdown") from e
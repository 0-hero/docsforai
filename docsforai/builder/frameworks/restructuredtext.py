"""
reStructuredText documentation parser for DocsForAI.

Requires:
- docutils
"""

import logging
from pathlib import Path
from typing import List, Dict, Any
from docutils.core import publish_parts
from docutils.writers.html4css1 import Writer

logger = logging.getLogger(__name__)

def parse_restructuredtext(docs_path: Path) -> List[Dict[str, Any]]:
    """
    Parse reStructuredText documentation.

    Args:
        docs_path (Path): Path to the directory containing reStructuredText files.

    Returns:
        List[Dict[str, Any]]: Parsed reStructuredText documentation.
    """
    logger.info(f"Parsing reStructuredText documentation at {docs_path}")

    parsed_docs = []
    for rst_file in docs_path.rglob('*.rst'):
        try:
            content = rst_file.read_text(encoding='utf-8')
            html_parts = publish_parts(
                source=content,
                writer=Writer(),
                settings_overrides={'output_encoding': 'unicode'}
            )
            parsed_docs.append({
                'type': 'restructuredtext',
                'filename': rst_file.relative_to(docs_path).with_suffix('.html').as_posix(),
                'content': html_parts['whole']
            })
        except Exception as e:
            logger.error(f"Error parsing reStructuredText file {rst_file}: {str(e)}")

    return parsed_docs
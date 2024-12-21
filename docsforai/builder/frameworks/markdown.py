"""
Markdown documentation parser for DocsForAI.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def parse_markdown(docs_path: Path) -> List[Dict[str, Any]]:
    """
    Parse Markdown documentation.

    Args:
        docs_path (Path): Path to the directory containing Markdown files.

    Returns:
        List[Dict[str, Any]]: Parsed Markdown documentation.
    """
    logger.info(f"Parsing Markdown documentation at {docs_path}")

    parsed_docs = []

    for md_file in docs_path.rglob('*.md'):
        try:
            with md_file.open('r', encoding='utf-8') as f:
                content = f.read()

            parsed_docs.append({
                'type': 'markdown',
                'filename': md_file.relative_to(docs_path).as_posix(),
                'content': content
            })

        except Exception as e:
            logger.error(f"Error parsing Markdown file {md_file}: {str(e)}")

    return parsed_docs
"""
GitBook documentation parser for DocsForAI.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any
import json

logger = logging.getLogger(__name__)

def parse_gitbook(docs_path: Path) -> List[Dict[str, Any]]:
    """
    Parse GitBook documentation.

    Args:
        docs_path (Path): Path to the GitBook documentation source.

    Returns:
        List[Dict[str, Any]]: Parsed GitBook documentation.

    Raises:
        FileNotFoundError: If book.json is not found.
        json.JSONDecodeError: If book.json is invalid.
    """
    logger.info(f"Parsing GitBook documentation at {docs_path}")

    book_json_path = docs_path / 'book.json'
    if not book_json_path.exists():
        logger.error("book.json not found")
        raise FileNotFoundError("book.json not found")

    parsed_docs = []

    # Parse book.json
    try:
        with book_json_path.open('r', encoding='utf-8') as f:
            book_config = json.load(f)
            parsed_docs.append({
                'type': 'gitbook_config',
                'filename': 'book.json',
                'content': json.dumps(book_config, indent=2)
            })
    except json.JSONDecodeError as e:
        logger.error(f"Invalid book.json: {str(e)}")
        raise

    # Parse SUMMARY.md for structure
    summary_path = docs_path / 'SUMMARY.md'
    if summary_path.exists():
        with summary_path.open('r', encoding='utf-8') as f:
            content = f.read()
            parsed_docs.append({
                'type': 'gitbook_summary',
                'filename': 'SUMMARY.md',
                'content': content
            })

    # Parse markdown files
    for md_file in docs_path.rglob('*.md'):
        if md_file.name != 'SUMMARY.md':
            with md_file.open('r', encoding='utf-8') as f:
                content = f.read()
                parsed_docs.append({
                    'type': 'gitbook',
                    'filename': md_file.relative_to(docs_path).as_posix(),
                    'content': content
                })

    # Parse README.md if it exists
    readme_path = docs_path / 'README.md'
    if readme_path.exists():
        with readme_path.open('r', encoding='utf-8') as f:
            content = f.read()
            parsed_docs.append({
                'type': 'gitbook_readme',
                'filename': 'README.md',
                'content': content
            })

    return parsed_docs
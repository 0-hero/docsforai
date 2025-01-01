"""
GitBook documentation parser for DocsForAI.

Requires:
- Typically `gitbook-cli` or a GitBook 2.0 environment. 
"""

import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import json

logger = logging.getLogger(__name__)

def parse_gitbook(docs_path: Path, config_file: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Parse GitBook documentation.

    Args:
        docs_path (Path): Path to the GitBook documentation source.
        config_file (Optional[str]): Custom configuration file name (default: book.json).

    Returns:
        List[Dict[str, Any]]: Parsed GitBook documentation.

    Raises:
        FileNotFoundError: If configuration file is not found.
        json.JSONDecodeError: If configuration file is invalid.
    """
    logger.info(f"Parsing GitBook documentation at {docs_path}")
    logger.debug(f"Using config file: {config_file or 'book.json'}")

    # Use custom config file if provided, otherwise default to book.json
    config_file = config_file or 'book.json'
    config_path = docs_path / config_file
    if not config_path.exists():
        logger.error(f"Configuration file {config_file} not found")
        raise FileNotFoundError(f"Configuration file {config_file} not found")

    parsed_docs = []

    # Parse configuration file
    try:
        with config_path.open('r', encoding='utf-8') as f:
            book_config = json.load(f)
            parsed_docs.append({
                'type': 'gitbook_config',
                'filename': config_file,
                'content': json.dumps(book_config, indent=2)
            })
    except json.JSONDecodeError as e:
        logger.error(f"Invalid configuration file {config_file}: {str(e)}")
        raise

    # SUMMARY.md
    summary_path = docs_path / 'SUMMARY.md'
    if summary_path.exists():
        with summary_path.open('r', encoding='utf-8') as f:
            content = f.read()
            parsed_docs.append({
                'type': 'gitbook_summary',
                'filename': 'SUMMARY.md',
                'content': content
            })

    # Parse all markdown
    for md_file in docs_path.rglob('*.md'):
        if md_file.name != 'SUMMARY.md':
            with md_file.open('r', encoding='utf-8') as f:
                content = f.read()
                parsed_docs.append({
                    'type': 'gitbook',
                    'filename': md_file.relative_to(docs_path).as_posix(),
                    'content': content
                })

    # README.md if present
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
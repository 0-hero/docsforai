"""
Docsify documentation parser for DocsForAI.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any
import json

logger = logging.getLogger(__name__)

def parse_docsify(docs_path: Path) -> List[Dict[str, Any]]:
    """
    Parse Docsify documentation.

    Args:
        docs_path (Path): Path to the Docsify documentation source.

    Returns:
        List[Dict[str, Any]]: Parsed Docsify documentation.

    Raises:
        FileNotFoundError: If index.html is not found.
    """
    logger.info(f"Parsing Docsify documentation at {docs_path}")

    index_path = docs_path / 'index.html'
    if not index_path.exists():
        logger.error("index.html not found")
        raise FileNotFoundError("index.html not found")

    parsed_docs = []

    # Parse index.html for Docsify configuration
    with index_path.open('r', encoding='utf-8') as f:
        content = f.read()
        parsed_docs.append({
            'type': 'docsify_config',
            'filename': 'index.html',
            'content': _extract_docsify_config(content)
        })

    # Parse markdown files
    for md_file in docs_path.rglob('*.md'):
        with md_file.open('r', encoding='utf-8') as f:
            content = f.read()
            parsed_docs.append({
                'type': 'docsify',
                'filename': md_file.relative_to(docs_path).as_posix(),
                'content': content
            })

    # Parse sidebar if it exists
    sidebar_path = docs_path / '_sidebar.md'
    if sidebar_path.exists():
        with sidebar_path.open('r', encoding='utf-8') as f:
            content = f.read()
            parsed_docs.append({
                'type': 'docsify_sidebar',
                'filename': '_sidebar.md',
                'content': content
            })

    return parsed_docs

def _extract_docsify_config(html_content: str) -> str:
    """
    Extract Docsify configuration from index.html.

    Args:
        html_content (str): Content of index.html.

    Returns:
        str: Extracted Docsify configuration as JSON string.
    """
    start_marker = 'window.$docsify = {'
    end_marker = '};'
    start_index = html_content.find(start_marker)
    if start_index != -1:
        end_index = html_content.find(end_marker, start_index)
        if end_index != -1:
            config_str = html_content[start_index + len(start_marker):end_index]
            # Clean up the config string and convert to valid JSON
            config_str = config_str.replace("'", '"').replace(',]', ']').replace(',}', '}')
            try:
                config_dict = json.loads('{' + config_str + '}')
                return json.dumps(config_dict, indent=2)
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse Docsify config: {str(e)}")
    return "{}"
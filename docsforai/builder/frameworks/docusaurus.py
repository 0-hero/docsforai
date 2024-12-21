"""
Docusaurus documentation parser for DocsForAI.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any
import json
import subprocess

logger = logging.getLogger(__name__)

def parse_docusaurus(docs_path: Path) -> List[Dict[str, Any]]:
    """
    Parse Docusaurus documentation.

    Args:
        docs_path (Path): Path to the Docusaurus documentation source.

    Returns:
        List[Dict[str, Any]]: Parsed Docusaurus documentation.

    Raises:
        FileNotFoundError: If docusaurus.config.js is not found.
        json.JSONDecodeError: If sidebar.json is invalid.
        subprocess.CalledProcessError: If Docusaurus build fails.
    """
    logger.info(f"Parsing Docusaurus documentation at {docs_path}")

    config_path = docs_path / 'docusaurus.config.js'
    if not config_path.exists():
        logger.error("docusaurus.config.js not found")
        raise FileNotFoundError("docusaurus.config.js not found")

    parsed_docs = []

    # Parse sidebar.json for structure
    sidebar_path = docs_path / 'sidebars.json'
    if sidebar_path.exists():
        try:
            with sidebar_path.open('r') as f:
                sidebar = json.load(f)
                parsed_docs.append({
                    'type': 'docusaurus_sidebar',
                    'filename': 'sidebars.json',
                    'content': json.dumps(sidebar, indent=2)
                })
        except json.JSONDecodeError as e:
            logger.error(f"Invalid sidebars.json: {str(e)}")
            raise

    # Parse documentation files
    docs_dir = docs_path / 'docs'
    if docs_dir.exists():
        for md_file in docs_dir.rglob('*.md'):
            with md_file.open('r', encoding='utf-8') as f:
                content = f.read()
                parsed_docs.append({
                    'type': 'docusaurus',
                    'filename': md_file.relative_to(docs_dir).as_posix(),
                    'content': content
                })

    # Build Docusaurus site to capture any additional files
    build_dir = docs_path / 'build'
    try:
        subprocess.run(['npm', 'install'], cwd=str(docs_path), check=True)
        subprocess.run(['npm', 'run', 'build'], cwd=str(docs_path), check=True)

        # Parse any additional files in the build directory
        for html_file in build_dir.rglob('*.html'):
            with html_file.open('r', encoding='utf-8') as f:
                content = f.read()
                parsed_docs.append({
                    'type': 'docusaurus_built',
                    'filename': html_file.relative_to(build_dir).as_posix(),
                    'content': _html_to_markdown(content)
                })

    except subprocess.CalledProcessError as e:
        logger.error(f"Docusaurus build failed: {str(e)}")
        raise
    finally:
        # Clean up build directory
        import shutil
        shutil.rmtree(build_dir, ignore_errors=True)

    return parsed_docs

def _html_to_markdown(html_content: str) -> str:
    """
    Convert HTML content to Markdown.

    This is a placeholder function. In a real implementation, you would use
    a library like html2text or beautifulsoup to convert HTML to Markdown.
    """
    # Placeholder implementation
    return f"Converted Markdown: {html_content[:100]}..."
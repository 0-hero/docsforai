"""
Hugo documentation parser for DocsForAI.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any
import toml
import subprocess

logger = logging.getLogger(__name__)

def parse_hugo(docs_path: Path) -> List[Dict[str, Any]]:
    """
    Parse Hugo documentation.

    Args:
        docs_path (Path): Path to the Hugo documentation source.

    Returns:
        List[Dict[str, Any]]: Parsed Hugo documentation.

    Raises:
        FileNotFoundError: If config.toml is not found.
        toml.TomlDecodeError: If config.toml is invalid.
        subprocess.CalledProcessError: If Hugo build fails.
    """
    logger.info(f"Parsing Hugo documentation at {docs_path}")

    config_path = docs_path / 'config.toml'
    if not config_path.exists():
        logger.error("config.toml not found")
        raise FileNotFoundError("config.toml not found")

    try:
        with config_path.open('r') as f:
            config = toml.load(f)
    except toml.TomlDecodeError as e:
        logger.error(f"Invalid config.toml: {str(e)}")
        raise

    parsed_docs = []

    # Parse markdown files in content directory
    content_dir = docs_path / 'content'
    for md_file in content_dir.rglob('*.md'):
        with md_file.open('r', encoding='utf-8') as f:
            content = f.read()
            parsed_docs.append({
                'type': 'hugo',
                'filename': md_file.relative_to(content_dir).as_posix(),
                'content': content
            })

    # Build Hugo site
    build_dir = docs_path / 'public'
    try:
        subprocess.run(['hugo'], cwd=str(docs_path), check=True)

        # Parse built HTML files
        for html_file in build_dir.rglob('*.html'):
            with html_file.open('r', encoding='utf-8') as f:
                content = f.read()
                parsed_docs.append({
                    'type': 'hugo_built',
                    'filename': html_file.relative_to(build_dir).as_posix(),
                    'content': _html_to_markdown(content)
                })

    except subprocess.CalledProcessError as e:
        logger.error(f"Hugo build failed: {str(e)}")
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
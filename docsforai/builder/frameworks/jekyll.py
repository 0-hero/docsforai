"""
Jekyll documentation parser for DocsForAI.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any
import yaml
import subprocess

logger = logging.getLogger(__name__)

def parse_jekyll(docs_path: Path) -> List[Dict[str, Any]]:
    """
    Parse Jekyll documentation.

    Args:
        docs_path (Path): Path to the Jekyll documentation source.

    Returns:
        List[Dict[str, Any]]: Parsed Jekyll documentation.

    Raises:
        FileNotFoundError: If _config.yml is not found.
        yaml.YAMLError: If _config.yml is invalid.
        subprocess.CalledProcessError: If Jekyll build fails.
    """
    logger.info(f"Parsing Jekyll documentation at {docs_path}")

    config_path = docs_path / '_config.yml'
    if not config_path.exists():
        logger.error("_config.yml not found")
        raise FileNotFoundError("_config.yml not found")

    try:
        with config_path.open('r') as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        logger.error(f"Invalid _config.yml: {str(e)}")
        raise

    parsed_docs = []

    # Parse markdown files
    for md_file in docs_path.rglob('*.md'):
        with md_file.open('r', encoding='utf-8') as f:
            content = f.read()
            parsed_docs.append({
                'type': 'jekyll',
                'filename': md_file.relative_to(docs_path).as_posix(),
                'content': content
            })

    # Build Jekyll site
    build_dir = docs_path / '_site'
    try:
        subprocess.run(['bundle', 'install'], cwd=str(docs_path), check=True)
        subprocess.run(['bundle', 'exec', 'jekyll', 'build'], cwd=str(docs_path), check=True)

        # Parse built HTML files
        for html_file in build_dir.rglob('*.html'):
            with html_file.open('r', encoding='utf-8') as f:
                content = f.read()
                parsed_docs.append({
                    'type': 'jekyll_built',
                    'filename': html_file.relative_to(build_dir).as_posix(),
                    'content': _html_to_markdown(content)
                })

    except subprocess.CalledProcessError as e:
        logger.error(f"Jekyll build failed: {str(e)}")
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
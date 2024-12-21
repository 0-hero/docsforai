"""
Sphinx documentation parser for DocsForAI.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any
import subprocess
import shutil
import yaml

logger = logging.getLogger(__name__)

def parse_sphinx(docs_path: Path) -> List[Dict[str, Any]]:
    """
    Parse Sphinx documentation.

    Args:
        docs_path (Path): Path to the Sphinx documentation source.

    Returns:
        List[Dict[str, Any]]: Parsed Sphinx documentation.

    Raises:
        subprocess.CalledProcessError: If Sphinx build fails.
        FileNotFoundError: If required files are missing.
    """
    logger.info(f"Parsing Sphinx documentation at {docs_path}")

    # Check for conf.py
    conf_path = docs_path / 'conf.py'
    if not conf_path.exists():
        logger.error("conf.py not found in Sphinx docs directory")
        raise FileNotFoundError("conf.py not found in Sphinx docs directory")

    # Create a temporary build directory
    build_dir = docs_path / '_build'
    build_dir.mkdir(exist_ok=True)

    try:
        # Run Sphinx build
        subprocess.run(['sphinx-build', '-b', 'html', str(docs_path), str(build_dir)], check=True)

        # Parse the generated HTML files
        parsed_docs = []
        for html_file in build_dir.rglob('*.html'):
            with html_file.open('r', encoding='utf-8') as f:
                content = f.read()
                parsed_docs.append({
                    'type': 'sphinx',
                    'filename': html_file.relative_to(build_dir).as_posix(),
                    'content': _html_to_markdown(content)
                })

        # Parse index.rst for structure
        index_path = docs_path / 'index.rst'
        if index_path.exists():
            with index_path.open('r', encoding='utf-8') as f:
                index_content = f.read()
                parsed_docs.append({
                    'type': 'sphinx_index',
                    'filename': 'index.rst',
                    'content': index_content
                })

        return parsed_docs

    except subprocess.CalledProcessError as e:
        logger.error(f"Sphinx build failed: {str(e)}")
        raise
    finally:
        # Clean up build directory
        shutil.rmtree(build_dir, ignore_errors=True)

def _html_to_markdown(html_content: str) -> str:
    """
    Convert HTML content to Markdown.

    This is a placeholder function. In a real implementation, you would use
    a library like html2text or beautifulsoup to convert HTML to Markdown.
    """
    # Placeholder implementation
    return f"Converted Markdown: {html_content[:100]}..."
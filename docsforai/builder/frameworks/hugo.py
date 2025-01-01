"""
Hugo documentation parser for DocsForAI.

Requires:
- `hugo` CLI in PATH
- A standard Hugo config (config.toml or config.yaml)
"""

import logging
from pathlib import Path
import shutil
from typing import List, Dict, Any, Optional
import toml
import subprocess
from docsforai.converter.html_to_md import html_to_md
from docsforai.utils import run_subprocess_with_logging

logger = logging.getLogger(__name__)

def parse_hugo(docs_path: Path, hugo_args: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Parse Hugo documentation.

    Args:
        docs_path (Path): Path to the Hugo documentation source.
        hugo_args (Optional[List[str]]): Additional arguments for hugo command.

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

    # Markdown files in content/
    content_dir = docs_path / 'content'
    for md_file in content_dir.rglob('*.md'):
        with md_file.open('r', encoding='utf-8') as f:
            content = f.read()
            parsed_docs.append({
                'type': 'hugo',
                'filename': md_file.relative_to(content_dir).as_posix(),
                'content': content
            })

    build_dir = docs_path / 'public'
    try:
        run_subprocess_with_logging(['hugo'], cwd=docs_path, additional_args=hugo_args)

        # Convert built HTML to MD
        for html_file in build_dir.rglob('*.html'):
            with html_file.open('r', encoding='utf-8') as f:
                content = f.read()
                parsed_docs.append({
                    'type': 'hugo_built',
                    'filename': html_file.relative_to(build_dir).as_posix(),
                    'content': html_to_md(content)
                })

    except subprocess.CalledProcessError as e:
        logger.error(f"Hugo build process failed")
        raise
    finally:
        # Cleanup build if you don't need it
        shutil.rmtree(build_dir, ignore_errors=True)

    return parsed_docs

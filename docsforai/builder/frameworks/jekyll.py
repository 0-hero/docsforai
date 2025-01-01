"""
Jekyll documentation parser for DocsForAI.

Requires:
- Ruby, bundler, and jekyll in PATH
"""

import logging
from pathlib import Path
import shutil
from typing import List, Dict, Any, Optional
import yaml
import subprocess
from docsforai.converter.html_to_md import html_to_md
from docsforai.utils import run_subprocess_with_logging

logger = logging.getLogger(__name__)

def parse_jekyll(docs_path: Path, bundle_install_args: Optional[List[str]] = None, bundle_build_args: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Parse Jekyll documentation.

    Args:
        docs_path (Path): Path to the Jekyll documentation source.
        bundle_install_args (Optional[List[str]]): Additional arguments for bundle install command.
        bundle_build_args (Optional[List[str]]): Additional arguments for bundle exec jekyll build command.

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
    # Parse .md
    for md_file in docs_path.rglob('*.md'):
        with md_file.open('r', encoding='utf-8') as f:
            content = f.read()
            parsed_docs.append({
                'type': 'jekyll',
                'filename': md_file.relative_to(docs_path).as_posix(),
                'content': content
            })

    build_dir = docs_path / '_site'
    try:
        run_subprocess_with_logging(['bundle', 'install'], cwd=docs_path, additional_args=bundle_install_args)
        run_subprocess_with_logging(['bundle', 'exec', 'jekyll', 'build'], cwd=docs_path, additional_args=bundle_build_args)

        for html_file in build_dir.rglob('*.html'):
            with html_file.open('r', encoding='utf-8') as f:
                content = f.read()
                parsed_docs.append({
                    'type': 'jekyll_built',
                    'filename': html_file.relative_to(build_dir).as_posix(),
                    'content': html_to_md(content)
                })

    except subprocess.CalledProcessError as e:
        logger.error(f"Jekyll build process failed")
        raise
    finally:
        shutil.rmtree(build_dir, ignore_errors=True)

    return parsed_docs

"""
MkDocs documentation parser for DocsForAI.

Requires:
- mkdocs installed (Python-based)
"""

import logging
from pathlib import Path
from typing import List, Dict, Any, Union
import yaml
from yaml.nodes import ScalarNode
import subprocess
import shutil
import os
from docsforai.converter.html_to_md import html_to_md

logger = logging.getLogger(__name__)

class MkDocsLoader(yaml.SafeLoader):
    """Custom YAML loader for MkDocs configuration."""

def _construct_python_name(loader, suffix, node):
    """
    For advanced tags like !python/name:some.module.func
    We'll just return the node’s value or a simple placeholder.
    """
    value = loader.construct_scalar(node)
    logger.warning(f"Ignoring advanced Python name tag: {value}")
    return value

MkDocsLoader.add_multi_constructor(
    'tag:yaml.org,2002:python/name:',
    _construct_python_name
)

def parse_mkdocs(docs_path: Path) -> List[Dict[str, Any]]:
    """
    Parse MkDocs documentation.

    Args:
        docs_path (Path): Path to the MkDocs documentation source.

    Returns:
        List[Dict[str, Any]]: Parsed MkDocs documentation.

    Raises:
        FileNotFoundError: If mkdocs.yml is not found.
        yaml.YAMLError: If mkdocs.yml is invalid.
        subprocess.CalledProcessError: If MkDocs build fails.
    """
    logger.info(f"Parsing MkDocs documentation at {docs_path}")

    mkdocs_yaml = docs_path / 'mkdocs.yml'
    if not mkdocs_yaml.exists():
        # check for mkdocs.yml in subdirs
        for subdir in docs_path.rglob('mkdocs.yml'):
            mkdocs_yaml = subdir
            docs_path = subdir.parent
            break
        if not mkdocs_yaml.exists():
            logger.error("mkdocs.yml not found")
            raise FileNotFoundError("mkdocs.yml not found")

    try:
        with mkdocs_yaml.open('r') as f:
            config = yaml.load(f, Loader=MkDocsLoader)
    except yaml.YAMLError as e:
        logger.error(f"Invalid mkdocs.yml: {str(e)}")
        raise

    nav = config.get('nav', [])
    docs_dir = config.get('docs_dir', 'docs')
    if os.path.isabs(docs_dir):
        docs_path = Path(docs_dir)
    else:
        docs_path = docs_path / docs_dir

    parsed_docs = []
    # If nav is not empty, parse the items
    _parse_nav_items(nav, docs_path, parsed_docs)

    if not parsed_docs:
        logger.info("No files found in nav, searching for markdown files directly.")
        for md_file in docs_path.rglob('*.md'):
            relative_path = md_file.relative_to(docs_path)
            _parse_markdown_file(md_file, str(relative_path), parsed_docs)

    build_dir = docs_path / 'site'
    try:
        subprocess.run(['mkdocs', 'build', '-f', str(mkdocs_yaml.absolute())], 
                       cwd=str(mkdocs_yaml.parent), check=True)

        for md_file in build_dir.rglob('*.md'):
            relative_path = md_file.relative_to(build_dir)
            if not any(doc['filename'] == str(relative_path) for doc in parsed_docs):
                _parse_markdown_file(md_file, str(relative_path), parsed_docs)

        # Convert .html in site/ to Markdown
        for html_file in build_dir.rglob('*.html'):
            relative_path = html_file.relative_to(build_dir)
            parsed_docs.append({
                'type': 'mkdocs_built',
                'filename': str(relative_path),
                'content': html_to_md(html_file.read_text(encoding='utf-8'))
            })

    except subprocess.CalledProcessError as e:
        logger.error(f"MkDocs build failed: {str(e)}")
        raise
    finally:
        shutil.rmtree(build_dir, ignore_errors=True)

    return parsed_docs

def _parse_nav_items(nav: List[Any], docs_path: Path, parsed_docs: List[Dict[str, Any]], prefix: str = ''):
    """Recursively parse navigation items."""
    for item in nav:
        if isinstance(item, dict):
            for title, content in item.items():
                if isinstance(content, str):
                    file_path = docs_path / content
                    if file_path.exists():
                        _parse_markdown_file(file_path, content, parsed_docs, title)
                    else:
                        logger.warning(f"File not found in nav: {file_path}")
                elif isinstance(content, list):
                    new_prefix = f"{prefix}/{title}" if prefix else title
                    _parse_nav_items(content, docs_path, parsed_docs, new_prefix)
        elif isinstance(item, str):
            file_path = docs_path / item
            if file_path.exists():
                _parse_markdown_file(file_path, item, parsed_docs)
            else:
                logger.warning(f"File not found in nav: {file_path}")


def _parse_markdown_file(file_path: Path, relative_path: str, parsed_docs: List[Dict[str, Any]], title: str = None):
    """Parse a single markdown file."""
    try:
        content = file_path.read_text(encoding='utf-8')
        doc = {
            'type': 'mkdocs',
            'filename': relative_path,
            'content': content
        }
        if title:
            doc['title'] = title
        parsed_docs.append(doc)
    except Exception as e:
        logger.warning(f"Error parsing file {file_path}: {str(e)}")
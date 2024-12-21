"""
MkDocs documentation parser for DocsForAI.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any, Union
import yaml
from yaml.nodes import ScalarNode
import subprocess
import shutil
import os

logger = logging.getLogger(__name__)

class MkDocsLoader(yaml.SafeLoader):
    """Custom YAML loader for MkDocs configuration."""
    def construct_python_name(self, suffix, node):
        if isinstance(node, ScalarNode):
            # Extract the module path, whether it comes from a tag or direct value
            if ':' in node.tag:
                # Handle tag:yaml.org,2002:python/name:path.to.function format
                module_path = node.tag.split('name:')[-1]
            else:
                # Handle direct module path
                module_path = node.value
            return module_path
        return None

# Register constructor for any python/name tags
MkDocsLoader.add_multi_constructor(
    'tag:yaml.org,2002:python/name:',
    MkDocsLoader.construct_python_name
)

def install_mkdocs_extensions():
    """Install required MkDocs extensions."""
    extensions = [
        'mdx-include',
        'markdown-include',
        'pymdown-extensions',  # This package contains all pymdownx extensions
    ]
    
    for ext in extensions:
        try:
            subprocess.run(['pip', 'install', ext], check=True)
        except subprocess.CalledProcessError as e:
            logger.warning(f"Failed to install {ext}: {str(e)}")

def create_temp_mkdocs_config(original_config: dict, mkdocs_yaml_path: Path) -> Path:
    """Create a temporary mkdocs.yml with simplified configuration."""
    temp_config = original_config.copy()
    
    # Simplify markdown extensions to avoid compatibility issues
    basic_extensions = [
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        'markdown.extensions.tables',
        'mdx_include',
        'pymdownx.highlight',
        'pymdownx.superfences',
        'pymdownx.snippets'
    ]
    
    # Keep essential configuration but remove problematic parts
    temp_config['markdown_extensions'] = basic_extensions
    
    # Remove potentially problematic keys
    keys_to_remove = ['hooks', 'plugins']
    for key in keys_to_remove:
        temp_config.pop(key, None)
    
    # Ensure site_dir is properly set
    temp_config['site_dir'] = 'site'
    
    # Create temporary config file next to the original
    temp_yaml_path = mkdocs_yaml_path.parent / 'temp_mkdocs.yml'
    with temp_yaml_path.open('w') as f:
        yaml.dump(temp_config, f)
    
    return temp_yaml_path

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

    # First try to find mkdocs.yml in the root
    mkdocs_yaml = docs_path / 'mkdocs.yml'
    if not mkdocs_yaml.exists():
        # Check if it's in a subdirectory structure like FastAPI (docs/en/mkdocs.yml)
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

    # Extract documentation structure from mkdocs.yml
    nav = config.get('nav', [])
    docs_dir = config.get('docs_dir', 'docs')  # Default to 'docs' if not specified
    
    # Handle both absolute and relative docs_dir paths
    if os.path.isabs(docs_dir):
        docs_path = Path(docs_dir)
    else:
        docs_path = docs_path / docs_dir

    parsed_docs = []

    # Parse the navigation structure
    _parse_nav_items(nav, docs_path, parsed_docs)

    # If no files were found in nav, try to find markdown files directly
    if not parsed_docs:
        logger.info("No files found in nav, searching for markdown files directly")
        for md_file in docs_path.rglob('*.md'):
            relative_path = md_file.relative_to(docs_path)
            _parse_markdown_file(md_file, str(relative_path), parsed_docs)

    # Install required MkDocs extensions
    install_mkdocs_extensions()

    # Create temporary mkdocs.yml with simplified configuration
    temp_yaml = create_temp_mkdocs_config(config, mkdocs_yaml)

    # Build MkDocs site to capture any additional files
    build_dir = docs_path / 'site'
    try:
        # Use the directory containing mkdocs.yml as the working directory
        subprocess.run(['mkdocs', 'build', '-f', str(temp_yaml.absolute()), '-d', str(build_dir.absolute())], 
                     cwd=str(mkdocs_yaml.parent), 
                     check=True,
                     capture_output=True,
                     text=True)

        # Parse any additional markdown files not in nav
        for md_file in build_dir.rglob('*.md'):
            relative_path = md_file.relative_to(build_dir)
            if not any(doc['filename'] == str(relative_path) for doc in parsed_docs):
                _parse_markdown_file(md_file, str(relative_path), parsed_docs)

    except subprocess.CalledProcessError as e:
        logger.error(f"MkDocs build failed: {str(e)}")
        logger.error(f"MkDocs output: {e.output}")
        raise
    finally:
        # Clean up build directory and temporary config
        if build_dir.exists():
            shutil.rmtree(build_dir, ignore_errors=True)
        if temp_yaml.exists():
            temp_yaml.unlink()

    return parsed_docs

def _parse_nav_items(nav: List[Any], docs_path: Path, parsed_docs: List[Dict[str, Any]], prefix: str = ''):
    """Recursively parse navigation items."""
    for item in nav:
        if isinstance(item, dict):
            for title, content in item.items():
                if isinstance(content, str):
                    # Direct file reference
                    file_path = docs_path / content
                    if file_path.exists():
                        _parse_markdown_file(file_path, content, parsed_docs, title)
                    else:
                        logger.warning(f"File not found: {file_path}")
                elif isinstance(content, list):
                    # Nested section
                    new_prefix = f"{prefix}/{title}" if prefix else title
                    _parse_nav_items(content, docs_path, parsed_docs, new_prefix)
        elif isinstance(item, str):
            # Direct file reference without title
            file_path = docs_path / item
            if file_path.exists():
                _parse_markdown_file(file_path, item, parsed_docs)
            else:
                logger.warning(f"File not found: {file_path}")

def _parse_markdown_file(file_path: Path, relative_path: str, parsed_docs: List[Dict[str, Any]], title: str = None):
    """Parse a single markdown file."""
    try:
        with file_path.open('r', encoding='utf-8') as f:
            content = f.read()
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
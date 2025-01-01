"""
Docusaurus documentation parser for DocsForAI.

Requires:
- Node.js, npm, plus a typical Docusaurus project setup.
"""

import logging
from pathlib import Path
import shutil
from typing import List, Dict, Any, Optional
import json
import subprocess
from docsforai.converter.html_to_md import html_to_md
from docsforai.utils import run_subprocess_with_logging

logger = logging.getLogger(__name__)

def parse_docusaurus(docs_path: Path, npm_install_args: Optional[List[str]] = None, npm_build_args: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Parse Docusaurus documentation.

    Args:
        docs_path (Path): Path to the Docusaurus documentation source.
        npm_install_args (Optional[List[str]]): Additional arguments for npm install command.
        npm_build_args (Optional[List[str]]): Additional arguments for npm run build command.

    Returns:
        List[Dict[str, Any]]: Parsed Docusaurus documentation.

    Raises:
        FileNotFoundError: If neither docusaurus.config.js nor docusaurus.config.ts is found.
        json.JSONDecodeError: If sidebar.json is invalid.
        subprocess.CalledProcessError: If Docusaurus build fails.
    """
    logger.info(f"Parsing Docusaurus documentation at {docs_path}")
    logger.debug(f"Received npm_install_args: {npm_install_args}")
    logger.debug(f"Received npm_build_args: {npm_build_args}")

    # Check for either .js or .ts config file
    js_config_path = docs_path / 'docusaurus.config.js'
    ts_config_path = docs_path / 'docusaurus.config.ts'
    
    if not js_config_path.exists() and not ts_config_path.exists():
        logger.error("Neither docusaurus.config.js nor docusaurus.config.ts found")
        raise FileNotFoundError("Neither docusaurus.config.js nor docusaurus.config.ts found")

    parsed_docs = []

    # Parse sidebar.json
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

    build_dir = docs_path / 'build'
    try:
        # Install and build with detailed logging
        logger.debug(f"Running npm install with args: {npm_install_args}")
        run_subprocess_with_logging(['npm', 'install'], cwd=docs_path, additional_args=npm_install_args)
        
        logger.debug(f"Running npm run build with args: {npm_build_args}")
        run_subprocess_with_logging(['npm', 'run', 'build'], cwd=docs_path, additional_args=npm_build_args)

        # Parse built HTML
        for html_file in build_dir.rglob('*.html'):
            with html_file.open('r', encoding='utf-8') as f:
                content = f.read()
                parsed_docs.append({
                    'type': 'docusaurus_built',
                    'filename': html_file.relative_to(build_dir).as_posix(),
                    'content': html_to_md(content)  # <--- real HTML -> MD conversion
                })

    except subprocess.CalledProcessError as e:
        logger.error(f"Docusaurus build process failed")
        raise
    finally:
        # Clean up build directory
        # If you want to keep the built site, comment out the rmtree below
        shutil.rmtree(build_dir, ignore_errors=True)

    return parsed_docs
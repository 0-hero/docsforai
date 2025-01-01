"""
VuePress documentation parser for DocsForAI.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any
import json
import subprocess
import shutil
from docsforai.converter.html_to_md import html_to_md

logger = logging.getLogger(__name__)

def parse_vuepress(docs_path: Path) -> List[Dict[str, Any]]:
    """
    Parse VuePress documentation.

    Args:
        docs_path (Path): Path to the VuePress documentation source.

    Returns:
        List[Dict[str, Any]]: Parsed VuePress documentation.

    Raises:
        FileNotFoundError: If config.js is not found.
        json.JSONDecodeError: If sidebar configuration is invalid.
        subprocess.CalledProcessError: If VuePress build fails.
    """
    logger.info(f"Parsing VuePress documentation at {docs_path}")

    config_path = docs_path / '.vuepress' / 'config.js'
    if not config_path.exists():
        logger.error("config.js not found in .vuepress directory")
        raise FileNotFoundError("config.js not found in .vuepress directory")

    parsed_docs = []

    # parse .md
    for md_file in docs_path.rglob('*.md'):
        with md_file.open('r', encoding='utf-8') as f:
            content = f.read()
            parsed_docs.append({
                'type': 'vuepress',
                'filename': md_file.relative_to(docs_path).as_posix(),
                'content': content
            })

    build_dir = docs_path / '.vuepress' / 'dist'
    try:
        subprocess.run(['npm', 'install'], cwd=str(docs_path), check=True)
        subprocess.run(['npx', 'vuepress', 'build', str(docs_path)], check=True)

        for html_file in build_dir.rglob('*.html'):
            with html_file.open('r', encoding='utf-8') as f:
                content = f.read()
                parsed_docs.append({
                    'type': 'vuepress_built',
                    'filename': html_file.relative_to(build_dir).as_posix(),
                    'content': html_to_md(content)
                })

        sidebar_config = _extract_sidebar_config(config_path)
        if sidebar_config:
            parsed_docs.append({
                'type': 'vuepress_sidebar',
                'filename': 'sidebar_config.json',
                'content': json.dumps(sidebar_config, indent=2)
            })

    except subprocess.CalledProcessError as e:
        logger.error(f"VuePress build failed: {str(e)}")
        raise
    finally:
        shutil.rmtree(build_dir, ignore_errors=True)

    return parsed_docs

def _extract_sidebar_config(config_path: Path) -> Dict[str, Any]:
    """
    Extract sidebar configuration from VuePress config file.

    Args:
        config_path (Path): Path to the VuePress config.js file.

    Returns:
        Dict[str, Any]: Extracted sidebar configuration.

    Raises:
        json.JSONDecodeError: If sidebar configuration is invalid.
    """
    content = config_path.read_text()
    sidebar_start = content.find('sidebar:')
    if sidebar_start != -1:
        sidebar_end = content.find('}', sidebar_start)
        if sidebar_end != -1:
            sidebar_str = content[sidebar_start:sidebar_end+1]
            sidebar_json = sidebar_str.replace("sidebar:", '"sidebar":').replace("'", '"')
            try:
                return json.loads('{' + sidebar_json + '}')
            except json.JSONDecodeError as e:
                logger.error(f"Invalid sidebar configuration: {str(e)}")
                raise
    return {}

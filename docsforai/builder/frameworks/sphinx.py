"""
Sphinx documentation parser for DocsForAI.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import subprocess
import shutil
from docsforai.converter.html_to_md import html_to_md
from docsforai.utils import run_subprocess_with_logging

logger = logging.getLogger(__name__)

def parse_sphinx(docs_path: Path, sphinx_args: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Parse Sphinx documentation.

    Args:
        docs_path (Path): Path to the Sphinx documentation source.
        sphinx_args (Optional[List[str]]): Additional arguments for sphinx-build command.

    Returns:
        List[Dict[str, Any]]: Parsed Sphinx documentation.

    Raises:
        subprocess.CalledProcessError: If Sphinx build fails.
        FileNotFoundError: If required files are missing.
    """
    logger.info(f"Parsing Sphinx documentation at {docs_path}")

    conf_path = docs_path / 'conf.py'
    if not conf_path.exists():
        logger.error("conf.py not found in Sphinx docs directory")
        raise FileNotFoundError("conf.py not found in Sphinx docs directory")

    build_dir = docs_path / '_build'
    build_dir.mkdir(exist_ok=True)

    try:
        run_subprocess_with_logging(['sphinx-build', '-b', 'html', str(docs_path), str(build_dir)], additional_args=sphinx_args)

        parsed_docs = []
        for html_file in build_dir.rglob('*.html'):
            with html_file.open('r', encoding='utf-8') as f:
                content = f.read()
                parsed_docs.append({
                    'type': 'sphinx',
                    'filename': html_file.relative_to(build_dir).as_posix(),
                    'content': html_to_md(content)
                })

        index_path = docs_path / 'index.rst'
        if index_path.exists():
            parsed_docs.append({
                'type': 'sphinx_index',
                'filename': 'index.rst',
                'content': index_path.read_text(encoding='utf-8')
            })

        return parsed_docs

    except subprocess.CalledProcessError as e:
        logger.error(f"Sphinx build process failed")
        raise
    finally:
        shutil.rmtree(build_dir, ignore_errors=True)

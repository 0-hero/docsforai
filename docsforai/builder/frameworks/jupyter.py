"""
Jupyter Notebook documentation parser for DocsForAI.

Requires:
- Python packages: nbformat, nbconvert
"""

import logging
from pathlib import Path
from typing import List, Dict, Any
import nbformat
from nbconvert import MarkdownExporter

logger = logging.getLogger(__name__)

def parse_jupyter(docs_path: Path) -> List[Dict[str, Any]]:
    """
    Parse Jupyter Notebook documentation.

    Args:
        docs_path (Path): Path to the directory containing Jupyter Notebook files.

    Returns:
        List[Dict[str, Any]]: Parsed Jupyter Notebook documentation.
    """
    logger.info(f"Parsing Jupyter Notebook documentation at {docs_path}")

    parsed_docs = []
    exporter = MarkdownExporter()

    for ipynb_file in docs_path.rglob('*.ipynb'):
        try:
            with ipynb_file.open('r', encoding='utf-8') as f:
                nb = nbformat.read(f, as_version=4)

            (markdown, _) = exporter.from_notebook_node(nb)
            parsed_docs.append({
                'type': 'jupyter',
                'filename': ipynb_file.relative_to(docs_path).with_suffix('.md').as_posix(),
                'content': markdown
            })

        except Exception as e:
            logger.error(f"Error parsing Jupyter Notebook {ipynb_file}: {str(e)}")

    return parsed_docs
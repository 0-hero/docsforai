"""
API Blueprint documentation parser for DocsForAI.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any
import subprocess

logger = logging.getLogger(__name__)

def parse_apiblueprint(docs_path: Path) -> List[Dict[str, Any]]:
    """
    Parse API Blueprint documentation.

    Args:
        docs_path (Path): Path to the API Blueprint file.

    Returns:
        List[Dict[str, Any]]: Parsed API Blueprint documentation.

    Raises:
        subprocess.CalledProcessError: If Aglio conversion fails.
    """
    logger.info(f"Parsing API Blueprint documentation at {docs_path}")

    try:
        # Convert API Blueprint to HTML using Aglio
        result = subprocess.run(
            ['aglio', '-i', str(docs_path), '--type', 'md'],
            check=True,
            capture_output=True,
            text=True
        )

        return [{
            'type': 'apiblueprint',
            'filename': docs_path.with_suffix('.md').name,
            'content': result.stdout
        }]

    except subprocess.CalledProcessError as e:
        logger.error(f"Error converting API Blueprint file {docs_path}: {str(e)}")
        raise
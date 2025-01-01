"""
Godoc documentation parser for DocsForAI.

Requires:
- `go` installed.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any
import subprocess
import re
from docsforai.utils.subprocess_utils import run_subprocess_with_logging

logger = logging.getLogger(__name__)

def parse_godoc(docs_path: Path) -> List[Dict[str, Any]]:
    """
    Parse Godoc documentation.

    Args:
        docs_path (Path): Path to the Go project.

    Returns:
        List[Dict[str, Any]]: Parsed Godoc documentation.

    Raises:
        subprocess.CalledProcessError: If Godoc generation fails.
    """
    logger.info(f"Parsing Godoc documentation at {docs_path}")

    try:
        result = run_subprocess_with_logging(
            ['go', 'doc', '-all'],
            cwd=str(docs_path),
            capture_output=True,
            text=True
        )
        parsed_docs = _parse_godoc_output(result.stdout)
        return parsed_docs

    except subprocess.CalledProcessError as e:
        logger.error(f"Godoc generation failed: {str(e)}")
        raise

def _parse_godoc_output(output: str) -> List[Dict[str, Any]]:
    """Parse Godoc output."""
    parsed_docs = []
    current_package = None
    current_content = []

    for line in output.split('\n'):
        if line.startswith('package '):
            if current_package:
                parsed_docs.append({
                    'type': 'godoc_package',
                    'filename': f"{current_package}.md",
                    'content': '\n'.join(current_content)
                })
            current_package = line.split()[1]
            current_content = [f"# Package: {current_package}\n"]
        else:
            current_content.append(line)

    if current_package:
        parsed_docs.append({
            'type': 'godoc_package',
            'filename': f"{current_package}.md",
            'content': '\n'.join(current_content)
        })

    return parsed_docs
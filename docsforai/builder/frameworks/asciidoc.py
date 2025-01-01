"""
AsciiDoc documentation parser for DocsForAI.

Requires:
- `asciidoctor` CLI installed (usually `gem install asciidoctor`).
"""

import logging
from pathlib import Path
from typing import List, Dict, Any
import subprocess

logger = logging.getLogger(__name__)

def parse_asciidoc(docs_path: Path) -> List[Dict[str, Any]]:
    """
    Parse AsciiDoc documentation.

    Args:
        docs_path (Path): Path to the directory containing AsciiDoc files.

    Returns:
        List[Dict[str, Any]]: Parsed AsciiDoc documentation.

    Raises:
        subprocess.CalledProcessError: If AsciiDoctor conversion fails.
    """
    logger.info(f"Parsing AsciiDoc documentation at {docs_path}")

    parsed_docs = []

    for adoc_file in docs_path.rglob('*.adoc'):
        try:
            # Convert AsciiDoc to HTML using AsciiDoctor
            result = subprocess.run(
                ['asciidoctor', '-o', '-', str(adoc_file)],
                check=True,
                capture_output=True,
                text=True
            )

            parsed_docs.append({
                'type': 'asciidoc',
                'filename': adoc_file.relative_to(docs_path).with_suffix('.html').as_posix(),
                'content': result.stdout
            })

        except subprocess.CalledProcessError as e:
            logger.error(f"Error converting AsciiDoc file {adoc_file}: {str(e)}")
        except Exception as e:
            logger.error(f"Error processing AsciiDoc file {adoc_file}: {str(e)}")

    return parsed_docs
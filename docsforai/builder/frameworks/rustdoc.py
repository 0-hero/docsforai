"""
Rustdoc documentation parser for DocsForAI.

Requires:
- Rust toolchain (cargo, rustc)
"""

import logging
from pathlib import Path
import shutil
from typing import List, Dict, Any
import subprocess
import json

logger = logging.getLogger(__name__)

def parse_rustdoc(docs_path: Path) -> List[Dict[str, Any]]:
    """
    Parse Rustdoc documentation.

    Args:
        docs_path (Path): Path to the Rust project.

    Returns:
        List[Dict[str, Any]]: Parsed Rustdoc documentation.

    Raises:
        subprocess.CalledProcessError: If Rustdoc generation fails.
        json.JSONDecodeError: If Rustdoc output is invalid JSON.
    """
    logger.info(f"Parsing Rustdoc documentation at {docs_path}")

    output_dir = docs_path / 'target' / 'doc'

    try:
        subprocess.run([
            'cargo', 'doc',
            '--no-deps',
            '--document-private-items'
        ], check=True, cwd=str(docs_path))

        parsed_docs = []
        json_file = output_dir / 'search-index.js'
        with json_file.open('r') as f:
            json_content = f.read().replace('searchIndex=', '')
            rustdoc_data = json.loads(json_content)

        for item in rustdoc_data['index']:
            content = _parse_rustdoc_item(item, rustdoc_data)
            filename = f"{item['name'].replace('::', '_')}.md"

            parsed_docs.append({
                'type': f"rustdoc_{item['type']}",
                'filename': filename,
                'content': content
            })

        return parsed_docs

    except subprocess.CalledProcessError as e:
        logger.error(f"Rustdoc generation failed: {str(e)}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid Rustdoc JSON output: {str(e)}")
        raise
    finally:
        shutil.rmtree(output_dir, ignore_errors=True)

#TODO: Add signature
def _parse_rustdoc_item(item: Dict[str, Any], rustdoc_data: Dict[str, Any]) -> str:
    """Parse a Rustdoc item."""
    content = []
    content.append(f"# {item['type'].capitalize()}: {item['name']}\n")

    if 'doc' in item:
        content.append(f"\n{item['doc']}\n")

    # If function, show signature
    if item['type'] == 'fn':
        # We don't have a snippet in your example, so you might store signatures in rustdoc_data['paths'] or something
        pass

    # If there's a parent item
    if 'parent' in item:
        content.append(f"\n## Defined in: {item['parent']}\n")

    return '\n'.join(content)
"""
Rustdoc documentation parser for DocsForAI.
"""

import logging
from pathlib import Path
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
        # Run Rustdoc
        subprocess.run([
            'cargo', 'doc',
            '--no-deps',
            '--document-private-items'
        ], check=True, cwd=str(docs_path))

        parsed_docs = []

        # Parse JSON output
        json_file = output_dir / 'search-index.js'
        with json_file.open('r') as f:
            # Remove the "searchIndex=" prefix from the file content
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

def _parse_rustdoc_item(item: Dict[str, Any], rustdoc_data: Dict[str, Any]) -> str:
    """Parse a Rustdoc item."""
    content = []
    content.append(f"# {item['type'].capitalize()}: {item['name']}\n")

    if 'doc' in item:
        content.append(f"\n{item['doc']}\n")

    if item['type'] == 'fn':
        content.append("\n## Function Signature\n")
        content.append(f"```rust\n{rustdoc_data['paths'][item['path']]}\n```")

    if 'parent' in item:
        content.append(f"\n## Defined in: {item['parent']}\n")

    if 'args' in item:
        content.append("\n## Parameters\n")
        for arg in item['args']:
            content.append(f"- {arg}")

    if 'return' in item:
        content.append(f"\n## Returns\n{item['return']}")

    return '\n'.join(content)
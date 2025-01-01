"""
JSDoc documentation parser for DocsForAI.

Requires:
- Node.js, npm, jsdoc, and a JSON template (like `jsdoc-json`)
"""

import logging
from pathlib import Path
from typing import List, Dict, Any
import subprocess
import json
import shutil

logger = logging.getLogger(__name__)

def parse_jsdoc(docs_path: Path) -> List[Dict[str, Any]]:
    """
    Parse JSDoc documentation.

    Args:
        docs_path (Path): Path to the JavaScript source files.

    Returns:
        List[Dict[str, Any]]: Parsed JSDoc documentation.

    Raises:
        subprocess.CalledProcessError: If JSDoc generation fails.
        json.JSONDecodeError: If JSDoc output is invalid JSON.
    """
    logger.info(f"Parsing JSDoc documentation at {docs_path}")

    output_dir = docs_path / 'jsdoc_output'
    output_dir.mkdir(exist_ok=True)

    try:
        subprocess.run([
            'jsdoc',
            '-r',
            str(docs_path),
            '-d', str(output_dir),
            '-t', 'node_modules/jsdoc-json',
            '-q', 'format=json'
        ], check=True, cwd=str(docs_path))

        parsed_docs = []
        json_file = output_dir / 'jsdoc.json'
        with json_file.open('r') as f:
            jsdoc_data = json.load(f)

        for item in jsdoc_data:
            content = _parse_jsdoc_item(item)
            filename = f"{item['name']}.md"
            parsed_docs.append({
                'type': f"jsdoc_{item['kind']}",
                'filename': filename,
                'content': content
            })

        return parsed_docs

    except subprocess.CalledProcessError as e:
        logger.error(f"JSDoc generation failed: {str(e)}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSDoc JSON output: {str(e)}")
        raise
    finally:
        shutil.rmtree(output_dir, ignore_errors=True)

def _parse_jsdoc_item(item: Dict[str, Any]) -> str:
    """Parse a JSDoc item."""
    content = []
    content.append(f"# {item['kind'].capitalize()}: {item['name']}\n")

    if 'description' in item:
        content.append(f"\n{item['description']}\n")

    if 'params' in item:
        content.append("\n## Parameters\n")
        for param in item['params']:
            ptype = param.get('type', {}).get('names', ['any'])[0]
            content.append(f"- {param['name']} ({ptype}): {param.get('description','')}")

    if 'returns' in item:
        content.append("\n## Returns\n")
        for ret in item['returns']:
            rtype = ret.get('type', {}).get('names', ['any'])[0]
            content.append(f"- {rtype}: {ret.get('description', '')}")

    if 'examples' in item:
        content.append("\n## Examples\n")
        for example in item['examples']:
            content.append(f"```javascript\n{example}\n```")

    return '\n'.join(content)
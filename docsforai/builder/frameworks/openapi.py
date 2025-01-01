"""
OpenAPI documentation parser for DocsForAI.

Requires:
- Just Python-based YAML/JSON parsing unless you want to do more advanced stuff
"""

import logging
from pathlib import Path
from typing import List, Dict, Any
import yaml
import json

logger = logging.getLogger(__name__)

def parse_openapi(docs_path: Path) -> List[Dict[str, Any]]:
    """
    Parse OpenAPI documentation.

    Args:
        docs_path (Path): Path to the OpenAPI specification file.

    Returns:
        List[Dict[str, Any]]: Parsed OpenAPI documentation.

    Raises:
        ValueError: If the OpenAPI specification is invalid.
    """
    logger.info(f"Parsing OpenAPI documentation at {docs_path}")

    if docs_path.suffix in ['.yaml', '.yml']:
        with docs_path.open('r', encoding='utf-8') as f:
            try:
                spec = yaml.safe_load(f)
            except yaml.YAMLError as e:
                logger.error(f"Invalid YAML in OpenAPI specification: {str(e)}")
                raise ValueError("Invalid YAML in OpenAPI specification") from e
    elif docs_path.suffix == '.json':
        with docs_path.open('r', encoding='utf-8') as f:
            try:
                spec = json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in OpenAPI specification: {str(e)}")
                raise ValueError("Invalid JSON in OpenAPI specification") from e
    else:
        logger.error(f"Unsupported file format for OpenAPI specification: {docs_path.suffix}")
        raise ValueError(f"Unsupported file format for OpenAPI specification: {docs_path.suffix}")

    content = _generate_markdown_from_openapi(spec)

    return [{
        'type': 'openapi',
        'filename': docs_path.with_suffix('.md').name,
        'content': content
    }]

def _generate_markdown_from_openapi(spec: Dict[str, Any]) -> str:
    """Generate Markdown documentation from OpenAPI specification."""
    content = []
    content.append(f"# {spec.get('info', {}).get('title', 'API Documentation')}")
    content.append(f"\n{spec.get('info', {}).get('description', '')}\n")

    if 'servers' in spec:
        content.append("## Servers")
        for server in spec['servers']:
            content.append(f"- {server.get('url')}: {server.get('description', '')}")

    if 'paths' in spec:
        content.append("\n## Endpoints")
        for path, methods in spec['paths'].items():
            content.append(f"\n### {path}")
            for method, details in methods.items():
                content.append(f"\n#### {method.upper()}")
                content.append(f"\n{details.get('summary', '')}")
                content.append(f"\n{details.get('description', '')}")
                if 'parameters' in details:
                    content.append("\nParameters:")
                    for param in details['parameters']:
                        content.append(f"- {param.get('name')} ({param.get('in')}): {param.get('description', '')}")
                if 'requestBody' in details:
                    content.append("\nRequest Body:")
                    content.append(f"{details['requestBody'].get('description', '')}")
                if 'responses' in details:
                    content.append("\nResponses:")
                    for status, response in details['responses'].items():
                        content.append(f"- {status}: {response.get('description', '')}")

    return '\n'.join(content)
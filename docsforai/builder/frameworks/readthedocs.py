"""
Read the Docs documentation parser for DocsForAI.

Requires:
- `.readthedocs.yml` in the project root
"""

import logging
from pathlib import Path
from typing import List, Dict, Any
import yaml
import requests
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

def parse_readthedocs(docs_path: Path) -> List[Dict[str, Any]]:
    """
    Parse Read the Docs documentation.

    Args:
        docs_path (Path): Path to the Read the Docs configuration.

    Returns:
        List[Dict[str, Any]]: Parsed Read the Docs documentation.

    Raises:
        FileNotFoundError: If .readthedocs.yml is not found.
        yaml.YAMLError: If .readthedocs.yml is invalid.
        requests.RequestException: If API request fails.
    """
    logger.info(f"Parsing Read the Docs documentation at {docs_path}")

    config_path = docs_path / '.readthedocs.yml'
    if not config_path.exists():
        logger.error(".readthedocs.yml not found")
        raise FileNotFoundError(".readthedocs.yml not found")

    try:
        with config_path.open('r') as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        logger.error(f"Invalid .readthedocs.yml: {str(e)}")
        raise

    parsed_docs = []

    project_slug = config.get('name', '')
    if not project_slug:
        logger.error("Project name not found in .readthedocs.yml")
        raise ValueError("Project name not found in .readthedocs.yml")

    api_url = f"https://readthedocs.org/api/v3/projects/{project_slug}/"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        project_data = response.json()

        parsed_docs.append({
            'type': 'readthedocs_overview',
            'filename': 'project_overview.md',
            'content': f"# {project_data['name']}\n\n{project_data['description']}"
        })

        for version in project_data['versions']:
            version_url = urljoin(api_url, f"versions/{version['slug']}/")
            version_response = requests.get(version_url)
            version_response.raise_for_status()
            version_data = version_response.json()

            for page in version_data['downloads']:
                page_url = page['url']
                page_response = requests.get(page_url)
                page_response.raise_for_status()

                parsed_docs.append({
                    'type': 'readthedocs_page',
                    'filename': f"{version['slug']}/{page['path']}",
                    'content': page_response.text
                })

    except requests.RequestException as e:
        logger.error(f"Failed to fetch Read the Docs documentation: {str(e)}")
        raise

    return parsed_docs
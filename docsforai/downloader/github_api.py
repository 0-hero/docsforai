"""
GitHub API handler for downloading pre-built documentation.
"""

import logging
import requests
from pathlib import Path
from typing import Optional, Dict, Any
import json
import base64

logger = logging.getLogger(__name__)

GITHUB_API_BASE = "https://api.github.com"
REPO_OWNER = "0-hero"
REPO_NAME = "docsforai-prebuilt"

def download_from_github(package_name: str, version: Optional[str] = None, output_dir: Path = Path("./docs")) -> str:
    """
    Download pre-built documentation for a package from GitHub.

    Args:
        package_name (str): Name of the package.
        version (Optional[str]): Specific version to download. If None, downloads the latest version.
        output_dir (Path): Directory to save the downloaded documentation.

    Returns:
        str: Path to the downloaded documentation.

    Raises:
        ValueError: If the package or version is not found.
        requests.RequestException: If there's an error communicating with the GitHub API.
    """
    logger.info(f"Downloading documentation for {package_name} (version: {version or 'latest'})")

    try:
        if version:
            content = _get_specific_version(package_name, version)
        else:
            content = _get_latest_version(package_name)

        output_path = output_dir / f"{package_name}{'_' + version if version else ''}.md"
        output_dir.mkdir(parents=True, exist_ok=True)

        with output_path.open('w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Documentation saved to {output_path}")
        return str(output_path)

    except requests.RequestException as e:
        logger.error(f"Error communicating with GitHub API: {str(e)}")
        raise
    except ValueError as e:
        logger.error(str(e))
        raise

def _get_specific_version(package_name: str, version: str) -> str:
    """Get a specific version of the documentation."""
    url = f"{GITHUB_API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{package_name}/{version}.md"
    response = requests.get(url)
    response.raise_for_status()

    content = response.json()
    if 'content' not in content:
        raise ValueError(f"Version {version} not found for {package_name}")

    return base64.b64decode(content['content']).decode('utf-8')

def _get_latest_version(package_name: str) -> str:
    """Get the latest version of the documentation."""
    url = f"{GITHUB_API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{package_name}"
    response = requests.get(url)
    response.raise_for_status()

    versions = [item['name'] for item in response.json() if item['type'] == 'file' and item['name'].endswith('.md')]
    if not versions:
        raise ValueError(f"No documentation found for {package_name}")

    latest_version = max(versions, key=lambda v: _version_key(v.rstrip('.md')))
    return _get_specific_version(package_name, latest_version.rstrip('.md'))

def _version_key(version: str) -> tuple:
    """Convert version string to a tuple for comparison."""
    return tuple(map(int, version.split('.')))
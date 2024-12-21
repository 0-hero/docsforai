"""
Git handler for DocsForAI.
"""

import logging
from pathlib import Path
import subprocess
from typing import Optional

logger = logging.getLogger(__name__)

def clone_repository(repo_url: str, target_dir: Path, branch: Optional[str] = None) -> Path:
    """
    Clone a Git repository.

    Args:
        repo_url (str): URL of the Git repository.
        target_dir (Path): Directory to clone the repository into.
        branch (Optional[str]): Specific branch to clone. If None, clones the default branch.

    Returns:
        Path: Path to the cloned repository.

    Raises:
        subprocess.CalledProcessError: If the Git command fails.
        FileExistsError: If the target directory is not empty.
    """
    logger.info(f"Cloning repository: {repo_url}")

    if target_dir.exists() and any(target_dir.iterdir()):
        logger.error(f"Target directory is not empty: {target_dir}")
        raise FileExistsError(f"Target directory is not empty: {target_dir}")

    target_dir.mkdir(parents=True, exist_ok=True)

    try:
        cmd = ['git', 'clone', '--depth', '1', repo_url, str(target_dir)]
        if branch:
            cmd.extend(['-b', branch])

        subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info(f"Repository cloned successfully to {target_dir}")
        return target_dir

    except subprocess.CalledProcessError as e:
        logger.error(f"Git clone failed: {e.stderr}")
        raise

def update_repository(repo_dir: Path) -> None:
    """
    Update an existing Git repository.

    Args:
        repo_dir (Path): Path to the Git repository.

    Raises:
        subprocess.CalledProcessError: If the Git command fails.
        FileNotFoundError: If the repository directory doesn't exist.
    """
    logger.info(f"Updating repository: {repo_dir}")

    if not repo_dir.exists():
        logger.error(f"Repository directory not found: {repo_dir}")
        raise FileNotFoundError(f"Repository directory not found: {repo_dir}")

    try:
        subprocess.run(['git', 'pull'], cwd=repo_dir, check=True, capture_output=True, text=True)
        logger.info("Repository updated successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Git pull failed: {e.stderr}")
        raise
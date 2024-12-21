"""
File utility functions for DocsForAI.
"""

import logging
from pathlib import Path
import shutil
from typing import Union

logger = logging.getLogger(__name__)

def create_directory(path: Union[str, Path]) -> Path:
    """
    Create a directory if it doesn't exist.

    Args:
        path (Union[str, Path]): Path to the directory.

    Returns:
        Path: Path to the created directory.

    Raises:
        OSError: If directory creation fails.
    """
    dir_path = Path(path)
    try:
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory created: {dir_path}")
        return dir_path
    except OSError as e:
        logger.error(f"Failed to create directory {dir_path}: {str(e)}")
        raise

def cleanup_directory(path: Union[str, Path]) -> None:
    """
    Remove a directory and its contents.

    Args:
        path (Union[str, Path]): Path to the directory to be removed.

    Raises:
        OSError: If directory removal fails.
    """
    dir_path = Path(path)
    try:
        shutil.rmtree(dir_path, ignore_errors=True)
        logger.info(f"Directory removed: {dir_path}")
    except OSError as e:
        logger.error(f"Failed to remove directory {dir_path}: {str(e)}")
        raise

def read_file(file_path: Union[str, Path]) -> str:
    """
    Read the contents of a file.

    Args:
        file_path (Union[str, Path]): Path to the file.

    Returns:
        str: Contents of the file.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        IOError: If there's an error reading the file.
    """
    path = Path(file_path)
    try:
        with path.open('r', encoding='utf-8') as file:
            content = file.read()
        logger.info(f"File read successfully: {path}")
        return content
    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        raise
    except IOError as e:
        logger.error(f"Error reading file {path}: {str(e)}")
        raise

def write_file(file_path: Union[str, Path], content: str) -> None:
    """
    Write content to a file.

    Args:
        file_path (Union[str, Path]): Path to the file.
        content (str): Content to write to the file.

    Raises:
        IOError: If there's an error writing to the file.
    """
    path = Path(file_path)
    try:
        with path.open('w', encoding='utf-8') as file:
            file.write(content)
        logger.info(f"File written successfully: {path}")
    except IOError as e:
        logger.error(f"Error writing to file {path}: {str(e)}")
        raise
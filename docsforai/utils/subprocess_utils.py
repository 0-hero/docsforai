"""
Subprocess utilities for DocsForAI.
"""

import logging
import subprocess
from typing import List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

def run_subprocess_with_logging(
    cmd: List[str],
    cwd: Optional[str | Path] = None,
    additional_args: Optional[List[str]] = None,
    check: bool = True,
    capture_output: bool = True,
    text: bool = True
) -> subprocess.CompletedProcess:
    """
    Run a subprocess command with detailed error logging.

    Args:
        cmd (List[str]): Command to run as a list of strings
        cwd (Optional[str | Path]): Working directory for the command
        additional_args (Optional[List[str]]): Additional arguments to pass to the command
        check (bool): If True, raise a CalledProcessError if the command returns a non-zero exit status
        capture_output (bool): If True, capture stdout and stderr in the result
        text (bool): If True, decode stdout and stderr using the default encoding

    Returns:
        subprocess.CompletedProcess: Result of the subprocess command

    Raises:
        subprocess.CalledProcessError: If the command fails and check is True
    """
    try:
        if isinstance(cwd, Path):
            cwd = str(cwd)
        
        # Create the full command with additional args
        full_cmd = list(cmd)  # Create a copy of the original command
        if additional_args:
            full_cmd.extend(additional_args)

        logger.debug(f"Running command: {' '.join(full_cmd)}")
        if cwd:
            logger.debug(f"Working directory: {cwd}")

        result = subprocess.run(
            full_cmd,
            cwd=cwd,
            check=check,
            capture_output=capture_output,
            text=text
        )
        logger.debug(f"Command '{' '.join(full_cmd)}' completed successfully")
        return result

    except subprocess.CalledProcessError as e:
        logger.error(f"Command '{' '.join(full_cmd)}' failed with exit code {e.returncode}")
        if e.stdout:
            logger.error(f"Command stdout:\n{e.stdout}")
        if e.stderr:
            logger.error(f"Command stderr:\n{e.stderr}")
        raise 
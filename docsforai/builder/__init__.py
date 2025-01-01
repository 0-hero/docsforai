"""
Documentation builder for DocsForAI.

This module is responsible for building documentation from source repositories.
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

from .detector import detect_framework
from .parser import parse_documentation
from .consolidator import consolidate_documentation
from ..utils import clone_repository, create_directory, cleanup_directory, run_subprocess_with_logging
from ..utils.dependency_manager import check_dependencies, get_installation_instructions

logger = logging.getLogger(__name__)

def build_documentation(config: Dict[str, Any], git_args: Optional[List[str]] = None) -> str:
    """
    Build documentation from source using the specified configuration.

    Args:
        config (Dict[str, Any]): Configuration dictionary.
        git_args (Optional[List[str]]): Additional arguments for git clone command.

    Returns:
        str: Path to the built documentation.

    Raises:
        ValueError: If the build fails.
    """
    logger.info("Starting documentation build process")
    logger.debug(f"Configuration: {config}")
    logger.debug(f"Git arguments: {git_args}")

    try:
        temp_dir = create_directory(Path('./temp'))
        output_dir = create_directory(Path(config['output']['path']))

        try:
            # Get git args from config if not provided
            config_git_args = config.get('source', {}).get('git_args')
            if git_args is None and config_git_args:
                git_args = config_git_args
                logger.debug(f"Using git args from config: {git_args}")

            repo_dir = clone_repository(
                config['source']['url'],
                temp_dir,
                config['source'].get('branch'),
                additional_args=git_args
            )

            docs_dir = repo_dir / config['docs']['path']
            if not docs_dir.exists():
                raise ValueError(f"Documentation directory not found: {docs_dir}")

            framework = config['docs']['framework']
            if framework == 'auto':
                framework = detect_framework(docs_dir)
                logger.info(f"Detected documentation framework: {framework}")

            missing_deps = check_dependencies(framework)
            if missing_deps:
                instructions = get_installation_instructions(missing_deps)
                raise ValueError(
                    f"Missing dependencies for {framework}: {', '.join(missing_deps)}\n"
                    f"Installation instructions:\n" + '\n'.join(instructions)
                )

            # Install additional pip dependencies if specified
            pip_dependencies = config.get('build', {}).get('pip_dependencies', [])
            if pip_dependencies:
                logger.info("Installing additional pip dependencies")
                logger.debug(f"Dependencies to install: {pip_dependencies}")
                try:
                    run_subprocess_with_logging(['pip', 'install'] + pip_dependencies)
                except Exception as e:
                    logger.error(f"Failed to install pip dependencies: {str(e)}")
                    raise ValueError(f"Failed to install pip dependencies: {str(e)}")

            # Extract build arguments from config root level
            build_args = {}
            if 'build_args' in config:
                build_args = config['build_args']
                logger.debug(f"Found build_args in config root: {build_args}")
            else:
                logger.debug("No build_args found in config")

            parsed_docs = parse_documentation(docs_dir, framework, build_args)
            output_file = output_dir / config['output']['filename']
            consolidated_content = consolidate_documentation(
                parsed_docs,
                config['consolidation'],
                config['metadata']
            )

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(consolidated_content)

            logger.info(f"Documentation built successfully: {output_file}")
            return str(output_file)

        finally:
            cleanup_directory(temp_dir)

    except Exception as e:
        logger.error(f"Failed to build documentation: {str(e)}")
        raise ValueError(f"Failed to build documentation: {str(e)}") from e
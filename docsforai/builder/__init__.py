"""
Documentation builder for DocsForAI.

This module is responsible for building documentation from source repositories.
"""

import logging
from pathlib import Path
from typing import Dict, Any

from .detector import detect_framework
from .parser import parse_documentation
from .consolidator import consolidate_documentation
from ..utils import clone_repository, create_directory, cleanup_directory
from ..utils.dependency_manager import check_dependencies, get_installation_instructions

logger = logging.getLogger(__name__)

def build_documentation(config: Dict[str, Any]) -> str:
    """
    Build documentation from source using the specified configuration.

    Args:
        config (Dict[str, Any]): Configuration dictionary.

    Returns:
        str: Path to the built documentation.

    Raises:
        ValueError: If the build fails.
    """
    logger.info("Starting documentation build process")

    try:
        # Create temporary and output directories
        temp_dir = create_directory(Path('./temp'))
        output_dir = create_directory(Path(config['output']['path']))

        try:
            # Clone the repository
            repo_dir = clone_repository(
                config['source']['url'],
                temp_dir,
                config['source'].get('branch')
            )

            # Get the docs directory
            docs_dir = repo_dir / config['docs']['path']
            if not docs_dir.exists():
                raise ValueError(f"Documentation directory not found: {docs_dir}")

            # Detect framework if set to auto
            framework = config['docs']['framework']
            if framework == 'auto':
                framework = detect_framework(docs_dir)
                logger.info(f"Detected documentation framework: {framework}")

            # Check framework dependencies
            missing_deps = check_dependencies(framework)
            if missing_deps:
                instructions = get_installation_instructions(missing_deps)
                raise ValueError(
                    f"Missing dependencies for {framework}: {', '.join(missing_deps)}\n"
                    f"Installation instructions:\n" + '\n'.join(instructions)
                )

            # Parse the documentation
            parsed_docs = parse_documentation(docs_dir, framework)

            # Consolidate the documentation
            output_file = output_dir / config['output']['filename']
            consolidated_content = consolidate_documentation(
                parsed_docs,
                config['consolidation'],
                config['metadata']
            )

            # Write the output
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(consolidated_content)

            logger.info(f"Documentation built successfully: {output_file}")
            return str(output_file)

        finally:
            # Clean up temporary directory
            cleanup_directory(temp_dir)

    except Exception as e:
        logger.error(f"Failed to build documentation: {str(e)}")
        raise ValueError(f"Failed to build documentation: {str(e)}") from e
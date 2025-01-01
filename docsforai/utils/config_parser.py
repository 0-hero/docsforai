"""
Configuration parser for DocsForAI.
"""

import logging
from pathlib import Path
import yaml
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

SUPPORTED_SOURCE_TYPES = ['github', 'gitlab', 'bitbucket']
SUPPORTED_FRAMEWORKS = [
    'auto', 'sphinx', 'mkdocs', 'docusaurus', 'jekyll', 'hugo', 
    'vuepress', 'docsify', 'gitbook', 'apiblueprint', 'asciidoc',
    'doxygen', 'godoc', 'javadoc', 'jsdoc', 'jupyter', 'markdown',
    'openapi', 'readthedocs', 'restructuredtext', 'rustdoc'
]
SUPPORTED_OUTPUT_FORMATS = ['markdown', 'html']

def parse_config(config_path: Path) -> Dict[str, Any]:
    """
    Parse and validate the configuration file.

    Args:
        config_path (Path): Path to the configuration file.

    Returns:
        Dict[str, Any]: Validated configuration dictionary.

    Raises:
        FileNotFoundError: If the configuration file is not found.
        yaml.YAMLError: If the configuration file is not valid YAML.
        ValueError: If the configuration is invalid.
    """
    logger.info(f"Parsing configuration file: {config_path}")

    if not config_path.exists():
        logger.error(f"Configuration file not found: {config_path}")
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    try:
        with config_path.open('r') as config_file:
            config = yaml.safe_load(config_file)
    except yaml.YAMLError as e:
        logger.error(f"Invalid YAML in configuration file: {str(e)}")
        raise

    # Validate and set defaults for all sections
    validated_config = {
        'package_name': _validate_package_name(config),
        'version': config.get('version'),
        'source': _validate_source(config.get('source', {})),
        'docs': _validate_docs(config.get('docs', {})),
        'build': _validate_build(config.get('build', {})),
        'build_args': _validate_build_args(config.get('build_args', {})),
        'output': _validate_output(config.get('output', {})),
        'consolidation': _validate_consolidation(config.get('consolidation', {})),
        'metadata': _validate_metadata(config.get('metadata', {})),
        'advanced': _validate_advanced(config.get('advanced', {}))
    }

    logger.info("Configuration validation successful")
    return validated_config

def _validate_package_name(config: Dict[str, Any]) -> str:
    """Validate package name."""
    package_name = config.get('package_name')
    if not package_name:
        raise ValueError("Missing required field: package_name")
    if not isinstance(package_name, str):
        raise ValueError("package_name must be a string")
    return package_name

def _validate_source(source: Dict[str, Any]) -> Dict[str, Any]:
    """Validate source configuration."""
    if not source:
        raise ValueError("Missing required section: source")
    
    if 'url' not in source:
        raise ValueError("Missing required field in source: url")
    
    if 'type' in source and source['type'] not in SUPPORTED_SOURCE_TYPES:
        raise ValueError(f"Unsupported source type. Must be one of: {', '.join(SUPPORTED_SOURCE_TYPES)}")
    
    return {
        'type': source.get('type', 'github'),
        'url': source['url'],
        'branch': source.get('branch')
    }

def _validate_docs(docs: Dict[str, Any]) -> Dict[str, Any]:
    """Validate docs configuration."""
    if not docs:
        raise ValueError("Missing required section: docs")
    
    if 'path' not in docs:
        raise ValueError("Missing required field in docs: path")
    
    if 'framework' in docs and docs['framework'] != 'auto' and docs['framework'] not in SUPPORTED_FRAMEWORKS:
        raise ValueError(f"Unsupported framework. Must be 'auto' or one of: {', '.join(SUPPORTED_FRAMEWORKS)}")
    
    return {
        'path': docs['path'],
        'framework': docs.get('framework', 'auto'),
        'index_file': docs.get('index_file')
    }

def _validate_build(build: Dict[str, Any]) -> Dict[str, Any]:
    """Validate build configuration."""
    validated = {
        'requirements_file': build.get('requirements_file'),
        'environment': build.get('environment', {}),
        'pip_dependencies': []
    }
    
    # Validate pip dependencies
    if 'pip_dependencies' in build:
        if not isinstance(build['pip_dependencies'], list):
            raise ValueError("pip_dependencies must be a list of strings")
        for dep in build['pip_dependencies']:
            if not isinstance(dep, str):
                raise ValueError("Each pip dependency must be a string")
        validated['pip_dependencies'] = build['pip_dependencies']
    
    return validated

def _validate_build_args(build_args: Dict[str, Any]) -> Dict[str, Any]:
    """Validate build arguments configuration."""
    validated = {}
    
    # Validate npm arguments
    if 'npm_install_args' in build_args:
        if not isinstance(build_args['npm_install_args'], list):
            raise ValueError("npm_install_args must be a list of strings")
        validated['npm_install_args'] = build_args['npm_install_args']
    
    if 'npm_build_args' in build_args:
        if not isinstance(build_args['npm_build_args'], list):
            raise ValueError("npm_build_args must be a list of strings")
        validated['npm_build_args'] = build_args['npm_build_args']
    
    # Validate doxygen arguments
    if 'doxygen_args' in build_args:
        if not isinstance(build_args['doxygen_args'], list):
            raise ValueError("doxygen_args must be a list of strings")
        validated['doxygen_args'] = build_args['doxygen_args']
    
    # Validate hugo arguments
    if 'hugo_args' in build_args:
        if not isinstance(build_args['hugo_args'], list):
            raise ValueError("hugo_args must be a list of strings")
        validated['hugo_args'] = build_args['hugo_args']
    
    # Validate jekyll arguments
    if 'bundle_install_args' in build_args:
        if not isinstance(build_args['bundle_install_args'], list):
            raise ValueError("bundle_install_args must be a list of strings")
        validated['bundle_install_args'] = build_args['bundle_install_args']
    
    if 'bundle_build_args' in build_args:
        if not isinstance(build_args['bundle_build_args'], list):
            raise ValueError("bundle_build_args must be a list of strings")
        validated['bundle_build_args'] = build_args['bundle_build_args']
    
    # Validate sphinx arguments
    if 'sphinx_args' in build_args:
        if not isinstance(build_args['sphinx_args'], list):
            raise ValueError("sphinx_args must be a list of strings")
        validated['sphinx_args'] = build_args['sphinx_args']
    
    # Validate GitBook arguments
    if 'gitbook_config_file' in build_args:
        if not isinstance(build_args['gitbook_config_file'], str):
            raise ValueError("gitbook_config_file must be a string")
        validated['gitbook_config_file'] = build_args['gitbook_config_file']
    
    return validated

def _validate_output(output: Dict[str, Any]) -> Dict[str, Any]:
    """Validate output configuration."""
    if not output:
        raise ValueError("Missing required section: output")
    
    if 'path' not in output:
        raise ValueError("Missing required field in output: path")
    
    if 'format' in output and output['format'] not in SUPPORTED_OUTPUT_FORMATS:
        raise ValueError(f"Unsupported output format. Must be one of: {', '.join(SUPPORTED_OUTPUT_FORMATS)}")
    
    return {
        'path': output['path'],
        'format': output.get('format', 'markdown'),
        'single_file': output.get('single_file', True),
        'filename': output.get('filename', 'documentation.md')
    }

def _validate_consolidation(consolidation: Dict[str, Any]) -> Dict[str, Any]:
    """Validate consolidation configuration."""
    validated = {
        'include_changelog': consolidation.get('include_changelog', False),
        'changelog_path': consolidation.get('changelog_path'),
        'exclude_patterns': consolidation.get('exclude_patterns', []),
        'custom_order': consolidation.get('custom_order', [])
    }
    
    # Validate exclude_patterns is a list of strings
    if not isinstance(validated['exclude_patterns'], list):
        raise ValueError("exclude_patterns must be a list")
    
    # Validate custom_order is a list of strings
    if not isinstance(validated['custom_order'], list):
        raise ValueError("custom_order must be a list")
    
    return validated

def _validate_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Validate metadata configuration."""
    return {
        'author': metadata.get('author', ''),
        'description': metadata.get('description', ''),
        'license': metadata.get('license', ''),
        'website': metadata.get('website', ''),
        'repository': metadata.get('repository', '')
    }

def _validate_advanced(advanced: Dict[str, Any]) -> Dict[str, Any]:
    """Validate advanced configuration."""
    return {
        'timeout': advanced.get('timeout', 300),  # Default 5 minutes
        'max_file_size': advanced.get('max_file_size', 10000000),  # Default 10MB
        'ignore_errors': advanced.get('ignore_errors', False)
    }
"""
Documentation parser for DocsForAI.

This module is responsible for parsing documentation from various frameworks.
It delegates the actual parsing to framework-specific parsers.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any, Callable, Optional
from docsforai.builder.frameworks import (
    parse_apiblueprint,
    parse_asciidoc,
    parse_docsify,
    parse_docusaurus,
    parse_doxygen,
    parse_gitbook,
    parse_godoc,
    parse_hugo,
    parse_javadoc,
    parse_jekyll,
    parse_jsdoc,
    parse_jupyter,
    parse_markdown,
    parse_mkdocs,
    parse_openapi,
    parse_readthedocs,
    parse_restructuredtext,
    parse_rustdoc,
    parse_sphinx,
    parse_vuepress,
)

logger = logging.getLogger(__name__)

# Mapping of framework names to their respective parsing functions
FRAMEWORK_PARSERS: Dict[str, Callable] = {
    'apiblueprint': parse_apiblueprint,
    'asciidoc': parse_asciidoc,
    'docsify': parse_docsify,
    'docusaurus': parse_docusaurus,
    'doxygen': parse_doxygen,
    'gitbook': parse_gitbook,
    'godoc': parse_godoc,
    'hugo': parse_hugo,
    'javadoc': parse_javadoc,
    'jekyll': parse_jekyll,
    'jsdoc': parse_jsdoc,
    'jupyter': parse_jupyter,
    'markdown': parse_markdown,
    'mkdocs': parse_mkdocs,
    'openapi': parse_openapi,
    'readthedocs': parse_readthedocs,
    'restructuredtext': parse_restructuredtext,
    'rustdoc': parse_rustdoc,
    'sphinx': parse_sphinx,
    'vuepress': parse_vuepress,
}

def parse_documentation(docs_path: Path, framework: str, build_args: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Parse documentation using the appropriate framework-specific parser.

    Args:
        docs_path (Path): Path to the documentation directory.
        framework (str): Name of the documentation framework to use.
        build_args (Optional[Dict[str, Any]]): Additional build arguments for specific frameworks.
            Supported arguments per framework:
            - docusaurus: npm_install_args, npm_build_args
            - doxygen: doxygen_args
            - hugo: hugo_args
            - jekyll: bundle_install_args, bundle_build_args
            - sphinx: sphinx_args
            - gitbook: gitbook_config_file

    Returns:
        List[Dict[str, Any]]: List of parsed documentation elements.
        Each element is a dictionary containing at least:
        - filename (str): Name of the source file
        - content (str): Parsed content in Markdown format
        - metadata (Dict): Any additional metadata (optional)

    Raises:
        ValueError: If the framework is not supported or the parsing fails.
    """
    logger.info(f"Starting documentation parsing using {framework} framework")
    logger.debug(f"Received build_args: {build_args}")

    if framework not in FRAMEWORK_PARSERS:
        supported_frameworks = ', '.join(FRAMEWORK_PARSERS.keys())
        error_msg = f"Unsupported framework: {framework}. Supported frameworks are: {supported_frameworks}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    if not docs_path.exists():
        error_msg = f"Documentation path does not exist: {docs_path}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    try:
        parser_func = FRAMEWORK_PARSERS[framework]
        build_args = build_args or {}
        
        # Call the parser with appropriate arguments based on the framework
        if framework == 'docusaurus':
            logger.debug(f"Passing to docusaurus parser - npm_install_args: {build_args.get('npm_install_args')}, npm_build_args: {build_args.get('npm_build_args')}")
            parsed_docs = parser_func(docs_path, 
                                   npm_install_args=build_args.get('npm_install_args'),
                                   npm_build_args=build_args.get('npm_build_args'))
        elif framework == 'doxygen':
            logger.debug(f"Passing to doxygen parser - doxygen_args: {build_args.get('doxygen_args')}")
            parsed_docs = parser_func(docs_path, 
                                   doxygen_args=build_args.get('doxygen_args'))
        elif framework == 'hugo':
            logger.debug(f"Passing to hugo parser - hugo_args: {build_args.get('hugo_args')}")
            parsed_docs = parser_func(docs_path, 
                                   hugo_args=build_args.get('hugo_args'))
        elif framework == 'jekyll':
            logger.debug(f"Passing to jekyll parser - bundle_install_args: {build_args.get('bundle_install_args')}, bundle_build_args: {build_args.get('bundle_build_args')}")
            parsed_docs = parser_func(docs_path, 
                                   bundle_install_args=build_args.get('bundle_install_args'),
                                   bundle_build_args=build_args.get('bundle_build_args'))
        elif framework == 'sphinx':
            logger.debug(f"Passing to sphinx parser - sphinx_args: {build_args.get('sphinx_args')}")
            parsed_docs = parser_func(docs_path, 
                                   sphinx_args=build_args.get('sphinx_args'))
        elif framework == 'gitbook':
            logger.debug(f"Passing to gitbook parser - config_file: {build_args.get('gitbook_config_file')}")
            parsed_docs = parser_func(docs_path,
                                   config_file=build_args.get('gitbook_config_file'))
        else:
            logger.debug(f"Using default parser without build args for framework: {framework}")
            parsed_docs = parser_func(docs_path)

        _validate_parsed_docs(parsed_docs)
        logger.info(f"Successfully parsed {len(parsed_docs)} documentation files")
        return parsed_docs

    except Exception as e:
        error_msg = f"Error parsing documentation with {framework}: {str(e)}"
        logger.error(error_msg)
        raise ValueError(error_msg) from e

def _validate_parsed_docs(parsed_docs: List[Dict[str, Any]]) -> None:
    """
    Validate that the parsed documentation meets the required format.

    Args:
        parsed_docs (List[Dict[str, Any]]): List of parsed documentation elements to validate.

    Raises:
        ValueError: If the parsed documentation format is invalid.
    """
    if not isinstance(parsed_docs, list):
        raise ValueError("Parsed documentation must be a list")

    for doc in parsed_docs:
        if not isinstance(doc, dict):
            raise ValueError("Each parsed documentation element must be a dictionary")
        required_fields = ['type', 'filename', 'content']
        missing_fields = [field for field in required_fields if field not in doc]
        if missing_fields:
            raise ValueError(f"Missing required fields in parsed documentation: {', '.join(missing_fields)}")
        if not isinstance(doc['type'], str):
            raise ValueError("'type' field must be a string")
        if not isinstance(doc['filename'], str):
            raise ValueError("'filename' field must be a string")
        if not isinstance(doc['content'], str):
            raise ValueError("'content' field must be a string")

def parse_common_documentation(docs_path: Path) -> List[Dict[str, Any]]:
    """
    Parse documentation when no specific framework is detected.
    This function handles common documentation files like README.md and basic Markdown/RST files.

    Args:
        docs_path (Path): Path to the documentation directory.

    Returns:
        List[Dict[str, Any]]: List of parsed documentation elements.
    """
    logger.info("Parsing common documentation files")
    parsed_docs = []

    try:
        md_parser = FRAMEWORK_PARSERS['markdown']
        parsed_docs.extend(md_parser(docs_path))

        rst_parser = FRAMEWORK_PARSERS['restructuredtext']
        parsed_docs.extend(rst_parser(docs_path))

        if not parsed_docs:
            for file_path in docs_path.rglob('*'):
                if file_path.is_file() and file_path.suffix in ['.md', '.rst', '.txt']:
                    content = file_path.read_text(encoding='utf-8')
                    parsed_docs.append({
                        'type': 'common',
                        'filename': file_path.relative_to(docs_path).as_posix(),
                        'content': content
                    })

        if not parsed_docs:
            logger.warning("No documentation files found in common formats")
            return []

        logger.info(f"Successfully parsed {len(parsed_docs)} common documentation files")
        return parsed_docs
    except Exception as e:
        logger.error(f"Error parsing common documentation: {str(e)}")
        return []
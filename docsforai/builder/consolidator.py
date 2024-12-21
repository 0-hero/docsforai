"""
Documentation consolidator for DocsForAI.

This module is responsible for consolidating parsed documentation into a single Markdown file.
"""

import logging
from typing import List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

def consolidate_documentation(
    parsed_docs: List[Dict[str, Any]],
    consolidation_config: Dict[str, Any],
    metadata: Dict[str, str]
) -> str:
    """
    Consolidate parsed documentation into a single Markdown file.

    Args:
        parsed_docs (List[Dict[str, Any]]): List of parsed documentation elements.
        consolidation_config (Dict[str, Any]): Configuration for consolidation.
        metadata (Dict[str, str]): Metadata to include in the consolidated documentation.

    Returns:
        str: Consolidated documentation as a Markdown string.
    """
    logger.info("Starting documentation consolidation")

    consolidated_content = []

    # Add metadata header
    consolidated_content.extend([
        f"# {metadata.get('package_name', 'Documentation')}\n",
        f"Version: {metadata.get('version', 'N/A')}\n",
        f"Author: {metadata.get('author', 'N/A')}\n",
        "\n---\n\n"
    ])

    # Group documents by type
    docs_by_type: Dict[str, List[Dict[str, Any]]] = {}
    for doc in parsed_docs:
        doc_type = doc['type']
        if doc_type not in docs_by_type:
            docs_by_type[doc_type] = []
        docs_by_type[doc_type].append(doc)

    # Add table of contents
    consolidated_content.append("## Table of Contents\n\n")
    for doc_type, docs in docs_by_type.items():
        # Add section header for document type
        type_header = doc_type.replace('_', ' ').title()
        consolidated_content.append(f"### {type_header}\n\n")
        
        # Add links to documents of this type
        for doc in docs:
            if consolidation_config.get('exclude_patterns'):
                if any(pattern in doc['filename'] for pattern in consolidation_config['exclude_patterns']):
                    logger.info(f"Excluding {doc['filename']} based on exclude patterns")
                    continue
            
            link_text = doc['filename'].replace('_', ' ').replace('.md', '')
            anchor = doc['filename'].lower().replace(' ', '-').replace('.', '')
            consolidated_content.append(f"- [{link_text}](#{anchor})\n")
        consolidated_content.append("\n")
    
    consolidated_content.append("\n---\n\n")

    # Add content grouped by type
    for doc_type, docs in docs_by_type.items():
        # Add section header for document type
        type_header = doc_type.replace('_', ' ').title()
        consolidated_content.append(f"# {type_header} Documentation\n\n")
        
        # Add each document of this type
        for doc in docs:
            if consolidation_config.get('exclude_patterns'):
                if any(pattern in doc['filename'] for pattern in consolidation_config['exclude_patterns']):
                    continue

            # Add document header
            consolidated_content.append(f"## {doc['filename']}\n\n")
            
            # Add document content
            consolidated_content.append(doc['content'])
            consolidated_content.append("\n\n---\n\n")

    # Add changelog if specified
    if consolidation_config.get('include_changelog'):
        changelog_path = consolidation_config.get('changelog_path')
        if changelog_path:
            changelog_content = _get_changelog(Path(changelog_path))
            if changelog_content:
                consolidated_content.extend([
                    "# Changelog\n\n",
                    changelog_content,
                    "\n\n---\n\n"
                ])

    logger.info("Documentation consolidation completed")
    return ''.join(consolidated_content)

def _get_changelog(changelog_path: Path) -> str:
    """
    Retrieve the content of the changelog file.

    Args:
        changelog_path (Path): Path to the changelog file.

    Returns:
        str: Content of the changelog file, or empty string if not found.
    """
    try:
        return changelog_path.read_text(encoding='utf-8')
    except FileNotFoundError:
        logger.warning(f"Changelog file not found: {changelog_path}")
        return ""
    except Exception as e:
        logger.error(f"Error reading changelog file: {str(e)}")
        return ""
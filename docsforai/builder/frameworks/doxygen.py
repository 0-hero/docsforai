"""
Doxygen documentation parser for DocsForAI.

Requires:
- `doxygen` in PATH
- A valid Doxyfile in `docs_path`.
"""

import logging
from pathlib import Path
import shutil
from typing import List, Dict, Any, Optional
import subprocess
import xml.etree.ElementTree as ET
from docsforai.utils import run_subprocess_with_logging

logger = logging.getLogger(__name__)

def parse_doxygen(docs_path: Path, doxygen_args: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Parse Doxygen documentation.

    Args:
        docs_path (Path): Path to the Doxygen configuration file.
        doxygen_args (Optional[List[str]]): Additional arguments for doxygen command.

    Returns:
        List[Dict[str, Any]]: Parsed Doxygen documentation.

    Raises:
        FileNotFoundError: If Doxyfile is not found.
        subprocess.CalledProcessError: If Doxygen build fails.
    """
    logger.info(f"Parsing Doxygen documentation at {docs_path}")

    doxyfile_path = docs_path / 'Doxyfile'
    if not doxyfile_path.exists():
        logger.error("Doxyfile not found")
        raise FileNotFoundError("Doxyfile not found")

    output_dir = docs_path / 'doxygen_output'
    output_dir.mkdir(exist_ok=True)

    try:
        run_subprocess_with_logging(['doxygen', str(doxyfile_path)], cwd=docs_path, additional_args=doxygen_args)

        parsed_docs = []
        xml_dir = output_dir / 'xml'
        if xml_dir.exists():
            index_xml = xml_dir / 'index.xml'
            if index_xml.exists():
                tree = ET.parse(index_xml)
                root = tree.getroot()

                for compound in root.findall('.//compound'):
                    kind = compound.get('kind')
                    name = compound.find('name').text if compound.find('name') is not None else 'unknown'
                    filename = compound.get('refid') + '.xml'

                    compound_xml = xml_dir / filename
                    if compound_xml.exists():
                        compound_tree = ET.parse(compound_xml)
                        compound_root = compound_tree.getroot()

                        content = _parse_compound(compound_root, kind)
                        parsed_docs.append({
                            'type': f'doxygen_{kind}',
                            'filename': f"{kind}_{name}.md",
                            'content': content
                        })

        return parsed_docs

    except subprocess.CalledProcessError as e:
        logger.error(f"Doxygen build process failed")
        raise
    finally:
        # Remove doxygen_output if you want ephemeral usage
        shutil.rmtree(output_dir, ignore_errors=True)


def _parse_compound(compound_root: ET.Element, kind: str) -> str:
    """Parse a compound (class, namespace, etc.) from Doxygen XML."""
    content = []
    name = compound_root.find('.//compoundname')
    name_text = name.text if name is not None else 'Unnamed'
    content.append(f"# {kind.capitalize()}: {name_text}\n")

    brief = compound_root.find('.//briefdescription')
    if brief is not None and brief.text:
        content.append(f"\n{brief.text.strip()}\n")

    detailed = compound_root.find('.//detaileddescription')
    if detailed is not None:
        for para in detailed.findall('.//para'):
            if para.text:
                content.append(f"\n{para.text.strip()}\n")

    for section in compound_root.findall('.//sectiondef'):
        section_kind = section.get('kind')
        content.append(f"\n## {section_kind.replace('_', ' ').capitalize()}\n")

        for member in section.findall('memberdef'):
            member_name = member.find('name').text if member.find('name') is not None else 'unknown'
            member_type = member.find('type')
            member_type_text = member_type.text if (member_type is not None and member_type.text) else ''
            content.append(f"\n### {member_type_text} {member_name}\n")

            member_brief = member.find('briefdescription')
            if member_brief is not None and member_brief.text:
                content.append(f"\n{member_brief.text.strip()}\n")

            member_detailed = member.find('detaileddescription')
            if member_detailed is not None:
                for para in member_detailed.findall('.//para'):
                    if para.text:
                        content.append(f"\n{para.text.strip()}\n")

    return '\n'.join(content)
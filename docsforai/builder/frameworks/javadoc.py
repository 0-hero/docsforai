"""
Javadoc documentation parser for DocsForAI.

Requires:
- `javac` and `javadoc` in PATH
- The doclet JAR (xmldoclet) if you want XML outputs
"""

import logging
from pathlib import Path
import shutil
from typing import List, Dict, Any
import subprocess
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

def parse_javadoc(docs_path: Path) -> List[Dict[str, Any]]:
    """
    Parse Javadoc documentation.

    Args:
        docs_path (Path): Path to the Java source files.

    Returns:
        List[Dict[str, Any]]: Parsed Javadoc documentation.

    Raises:
        subprocess.CalledProcessError: If Javadoc generation fails.
    """
    logger.info(f"Parsing Javadoc documentation at {docs_path}")

    output_dir = docs_path / 'javadoc_output'
    output_dir.mkdir(exist_ok=True)

    try:
        subprocess.run([
            'javadoc',
            '-d', str(output_dir),
            '-sourcepath', str(docs_path),
            '-subpackages', '.',
            '-doclet', 'com.sun.tools.doclets.formats.xml.XMLDoclet',
            '-docletpath', '/path/to/xmldoclet.jar'
        ], check=True, cwd=str(docs_path))

        parsed_docs = []
        for xml_file in output_dir.glob('*.xml'):
            tree = ET.parse(xml_file)
            root = tree.getroot()

            for class_elem in root.findall('.//class'):
                class_name = class_elem.get('name')
                content = _parse_class(class_elem)

                parsed_docs.append({
                    'type': 'javadoc_class',
                    'filename': f"{class_name}.md",
                    'content': content
                })

        return parsed_docs

    except subprocess.CalledProcessError as e:
        logger.error(f"Javadoc generation failed: {str(e)}")
        raise
    finally:
        shutil.rmtree(output_dir, ignore_errors=True)

def _parse_class(class_elem: ET.Element) -> str:
    """Parse a class element from Javadoc XML."""
    content = []
    class_name = class_elem.get('name', 'UnknownClass')
    content.append(f"# Class: {class_name}\n")

    comment = class_elem.find('comment')
    if comment is not None and comment.text:
        content.append(f"\n{comment.text.strip()}\n")

    for method in class_elem.findall('.//method'):
        method_name = method.get('name', 'UnknownMethod')
        content.append(f"\n## Method: {method_name}\n")

        method_comment = method.find('comment')
        if method_comment is not None and method_comment.text:
            content.append(f"\n{method_comment.text.strip()}\n")

        for param in method.findall('.//parameter'):
            param_name = param.get('name')
            param_type = param.get('type')
            content.append(f"\n- Parameter: {param_name} ({param_type})")

        return_elem = method.find('return')
        if return_elem is not None:
            return_type = return_elem.get('type', 'void')
            content.append(f"\n- Returns: {return_type}")

    return '\n'.join(content)
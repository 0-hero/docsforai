"""
Converter for reStructuredText to Markdown.
"""

import logging
from pathlib import Path
from docutils.core import publish_parts
from docutils.writers import Writer
from docutils.nodes import NodeVisitor, Node
from docutils import nodes

logger = logging.getLogger(__name__)

class MarkdownWriter(Writer):
    def __init__(self):
        Writer.__init__(self)
        self.translator_class = MarkdownTranslator

class MarkdownTranslator(NodeVisitor):
    def __init__(self, document):
        NodeVisitor.__init__(self, document)
        self.output = []
        self.list_depth = 0

    def visit_paragraph(self, node):
        self.output.append('')

    def depart_paragraph(self, node):
        self.output.append('')

    def visit_title(self, node):
        self.output.append(f"{'#' * (node.parent.index(node) + 1)} ")

    def visit_Text(self, node):
        self.output.append(node.astext())

    def visit_list_item(self, node):
        self.output.append("  " * self.list_depth + "- ")
        self.list_depth += 1

    def depart_list_item(self, node):
        self.list_depth -= 1

    def visit_literal_block(self, node):
        self.output.append("```")

    def depart_literal_block(self, node):
        self.output.append("```")

    def unknown_visit(self, node):
        pass

    def unknown_departure(self, node):
        pass

def rst_to_md(rst_content: str) -> str:
    """
    Convert reStructuredText to Markdown.

    Args:
        rst_content (str): reStructuredText content.

    Returns:
        str: Converted Markdown content.

    Raises:
        ValueError: If conversion fails.
    """
    try:
        parts = publish_parts(source=rst_content, writer=MarkdownWriter())
        return ''.join(parts['whole'])
    except Exception as e:
        logger.error(f"Error converting RST to Markdown: {str(e)}")
        raise ValueError("Failed to convert RST to Markdown") from e
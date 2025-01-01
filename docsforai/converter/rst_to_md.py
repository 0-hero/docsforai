"""
Converter for reStructuredText to Markdown.
"""

import logging
from docutils.core import publish_parts
from docutils.writers import Writer
from docutils.nodes import NodeVisitor
from docutils.writers.html4css1 import Writer as HTMLWriter

logger = logging.getLogger(__name__)

class MarkdownWriter(Writer):
    def __init__(self):
        super().__init__()
        self.translator_class = MarkdownTranslator

class MarkdownTranslator(NodeVisitor):
    def __init__(self, document):
        super().__init__(document)
        self.output = []

    # Minimal AST handling
    def visit_paragraph(self, node):
        self.output.append('')

    def depart_paragraph(self, node):
        self.output.append('')

    def visit_title(self, node):
        self.output.append('# ')

    def visit_Text(self, node):
        self.output.append(node.astext())

    def unknown_visit(self, node):
        pass

    def unknown_departure(self, node):
        pass

def rst_to_md(rst_content: str) -> str:
    try:
        parts = publish_parts(source=rst_content, writer=MarkdownWriter())
        return ''.join(parts['whole'])
    except Exception as e:
        logger.error(f"Error converting RST to Markdown: {str(e)}")
        raise ValueError("Failed to convert RST to Markdown") from e
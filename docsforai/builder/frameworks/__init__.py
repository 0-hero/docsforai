"""
Framework-specific parsing modules for DocsForAI.

This package contains modules for parsing documentation from various frameworks.
"""

from .apiblueprint import parse_apiblueprint
from .asciidoc import parse_asciidoc
from .docsify import parse_docsify
from .docusaurus import parse_docusaurus
from .doxygen import parse_doxygen
from .gitbook import parse_gitbook
from .godoc import parse_godoc
from .hugo import parse_hugo
from .javadoc import parse_javadoc
from .jekyll import parse_jekyll
from .jsdoc import parse_jsdoc
from .jupyter import parse_jupyter
from .markdown import parse_markdown
from .mkdocs import parse_mkdocs
from .openapi import parse_openapi
from .readthedocs import parse_readthedocs
from .restructuredtext import parse_restructuredtext
from .rustdoc import parse_rustdoc
from .sphinx import parse_sphinx
from .vuepress import parse_vuepress

__all__ = [
    'parse_apiblueprint',
    'parse_asciidoc',
    'parse_docsify',
    'parse_docusaurus',
    'parse_doxygen',
    'parse_gitbook',
    'parse_godoc',
    'parse_hugo',
    'parse_javadoc',
    'parse_jekyll',
    'parse_jsdoc',
    'parse_jupyter',
    'parse_markdown',
    'parse_mkdocs',
    'parse_openapi',
    'parse_readthedocs',
    'parse_restructuredtext',
    'parse_rustdoc',
    'parse_sphinx',
    'parse_vuepress',
]

"""
Framework detector for DocsForAI.

This module is responsible for detecting the documentation framework used in a repository.
"""

import logging
import json
import re
from pathlib import Path
from typing import Dict, Callable, List

logger = logging.getLogger(__name__)

def _has_content_match(file_path: Path, patterns: List[str]) -> bool:
    """Check if file content matches any of the given patterns."""
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        return any(pattern in content for pattern in patterns)
    except Exception:
        return False

def _check_sphinx(path: Path) -> bool:
    # Primary check for conf.py
    conf_py = path / 'conf.py'
    if conf_py.exists():
        return _has_content_match(conf_py, ['sphinx', 'sphinx-build'])
    
    # Check for sphinx-specific files and directories
    sphinx_indicators = [
        path / 'source' / 'conf.py',
        path / 'docs' / 'conf.py',
        path / '_build',
        path / 'source' / '_templates',
    ]
    if any(p.exists() for p in sphinx_indicators):
        return True
    
    # Check requirements files for sphinx dependencies
    req_files = ['requirements.txt', 'dev-requirements.txt', 'docs/requirements.txt']
    for req_file in req_files:
        req_path = path / req_file
        if req_path.exists() and _has_content_match(req_path, ['sphinx']):
            return True
    
    return False

def _check_mkdocs(path: Path) -> bool:
    # Check for mkdocs.yml or .yaml
    mkdocs_files = [path / 'mkdocs.yml', path / 'mkdocs.yaml', 
                    path / 'docs' / 'mkdocs.yml', path / 'docs' / 'mkdocs.yaml']
    
    for mkdocs_file in mkdocs_files:
        if mkdocs_file.exists():
            return _has_content_match(mkdocs_file, ['site_name:', 'docs_dir:', 'mkdocs'])
    
    # Check requirements files
    req_files = ['requirements.txt', 'dev-requirements.txt', 'docs/requirements.txt']
    for req_file in req_files:
        req_path = path / req_file
        if req_path.exists() and _has_content_match(req_path, ['mkdocs']):
            return True
    
    return False

def _check_docusaurus(path: Path) -> bool:
    # Check for configuration files
    config_files = [
        path / 'docusaurus.config.js',
        path / 'siteConfig.js',
        path / 'website' / 'siteConfig.js'
    ]
    
    for config_file in config_files:
        if config_file.exists():
            return _has_content_match(config_file, ['docusaurus', '@docusaurus/core'])
    
    # Check package.json for docusaurus dependencies
    package_json = path / 'package.json'
    if package_json.exists():
        try:
            with open(package_json) as f:
                data = json.load(f)
                deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                return any('docusaurus' in dep for dep in deps)
        except Exception:
            pass
    
    return False

def _check_jekyll(path: Path) -> bool:
    # Check for Jekyll configuration files
    jekyll_files = [
        path / '_config.yml',
        path / '_config.yaml',
        path / 'docs' / '_config.yml'
    ]
    
    for config_file in jekyll_files:
        if config_file.exists():
            return _has_content_match(config_file, ['jekyll', 'theme:', 'plugins:', 'collections:'])
    
    # Check for typical Jekyll directory structure
    jekyll_dirs = ['_layouts', '_includes', '_posts', '_site']
    if any((path / dir_name).exists() for dir_name in jekyll_dirs):
        return True
    
    # Check Gemfile for Jekyll
    gemfile = path / 'Gemfile'
    if gemfile.exists():
        return _has_content_match(gemfile, ['jekyll'])
    
    return False

def _check_hugo(path: Path) -> bool:
    # Check for Hugo configuration files
    hugo_files = [
        path / 'config.toml',
        path / 'config.yaml',
        path / 'config.json',
        path / 'hugo.toml',
        path / 'hugo.yaml',
        path / 'hugo.json'
    ]
    
    for config_file in hugo_files:
        if config_file.exists():
            return _has_content_match(config_file, ['baseURL', 'theme', 'hugo'])
    
    # Check for Hugo-specific directories
    hugo_dirs = ['layouts', 'content', 'themes', 'archetypes']
    if any((path / dir_name).exists() for dir_name in hugo_dirs):
        return True
    
    return False

def _check_apiblueprint(path: Path) -> bool:
    # Check for API Blueprint files
    for apib_file in path.glob('**/*.apib'):
        if _has_content_match(apib_file, ['FORMAT: 1A', '# Group', '## Action']):
            return True
    
    for blueprint_file in path.glob('**/*.apiblueprint'):
        if _has_content_match(blueprint_file, ['FORMAT: 1A', '# Group', '## Action']):
            return True
    
    # Check package.json for aglio or other API Blueprint tools
    package_json = path / 'package.json'
    if package_json.exists():
        try:
            with open(package_json) as f:
                data = json.load(f)
                deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                return any(dep in ['aglio', 'apib2swagger', 'apiary-client'] for dep in deps)
        except Exception:
            pass
    
    return False

def _check_asciidoc(path: Path) -> bool:
    # Check for AsciiDoc files
    for ext in ['.adoc', '.asciidoc', '.asc']:
        for doc_file in path.glob(f'**/*{ext}'):
            if _has_content_match(doc_file, ['= ', '== ', ':toc:', 'ifdef::', 'include::']):
                return True
    
    # Check for AsciiDoctor configuration
    config_files = [
        path / 'asciidoctor.json',
        path / '.asciidoctor.json',
        path / 'docs' / 'asciidoctor.json'
    ]
    
    for config_file in config_files:
        if config_file.exists():
            return True
    
    # Check Gemfile for AsciiDoctor
    gemfile = path / 'Gemfile'
    if gemfile.exists():
        return _has_content_match(gemfile, ['asciidoctor'])
    
    return False

def _check_docsify(path: Path) -> bool:
    # Check for Docsify setup
    if not (path / '.nojekyll').exists():
        return False
    
    index_files = [path / 'index.html', path / 'docs' / 'index.html']
    for index_file in index_files:
        if index_file.exists() and _has_content_match(index_file, ['docsify', 'window.$docsify']):
            return True
    
    # Check for docsify configuration file
    config_files = [path / '.docsifyrc', path / 'docsify.json']
    for config_file in config_files:
        if config_file.exists():
            return True
    
    # Check package.json for docsify
    package_json = path / 'package.json'
    if package_json.exists():
        try:
            with open(package_json) as f:
                data = json.load(f)
                deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                return any('docsify' in dep for dep in deps)
        except Exception:
            pass
    
    return False

def _check_doxygen(path: Path) -> bool:
    # Check for Doxygen configuration files
    doxygen_files = [
        path / 'Doxyfile',
        path / 'doxyfile',
        path / 'doxygen.conf',
        path / '.doxygen',
        path / 'docs' / 'Doxyfile'
    ]
    
    for config_file in doxygen_files:
        if config_file.exists():
            return _has_content_match(config_file, ['GENERATE_HTML', 'PROJECT_NAME', 'DOXYGEN'])
    
    # Check for Doxygen-style comments in source files
    for ext in ['.cpp', '.hpp', '.c', '.h', '.java']:
        for source_file in path.glob(f'**/*{ext}'):
            if _has_content_match(source_file, ['/**', '///', '\\brief', '@brief', '@param', '@return']):
                return True
    
    return False

def _check_gitbook(path: Path) -> bool:
    # Check for GitBook configuration files
    gitbook_files = [
        path / 'book.json',
        path / '.gitbook.yaml',
        path / '.gitbook.yml',
        path / 'docs' / 'book.json'
    ]
    
    for config_file in gitbook_files:
        if config_file.exists():
            return _has_content_match(config_file, ['gitbook', 'structure', 'plugins'])
    
    # Check for GitBook directory structure
    if (path / 'SUMMARY.md').exists() and (path / 'README.md').exists():
        return True
    
    # Check package.json for GitBook
    package_json = path / 'package.json'
    if package_json.exists():
        try:
            with open(package_json) as f:
                data = json.load(f)
                deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                return any('gitbook' in dep for dep in deps)
        except Exception:
            pass
    
    return False

def _check_godoc(path: Path) -> bool:
    # Check for Go module
    if not (path / 'go.mod').exists():
        return False
    
    # Look for Go files with package documentation
    for go_file in path.glob('**/*.go'):
        if _has_content_match(go_file, ['package ', '// ', '/* ', 'func ', 'type ']):
            return True
    
    # Check for doc.go files (common in Go projects)
    return any((path / d / 'doc.go').exists() for d in path.iterdir() if d.is_dir())

def _check_javadoc(path: Path) -> bool:
    # Look for Java files with Javadoc comments
    for java_file in path.glob('**/*.java'):
        if _has_content_match(java_file, ['/**', '@param', '@return', '@throws', '@author', '@see']):
            return True
    
    # Check for Maven or Gradle configuration with Javadoc plugin
    build_files = [
        path / 'pom.xml',
        path / 'build.gradle',
        path / 'build.gradle.kts'
    ]
    
    for build_file in build_files:
        if build_file.exists():
            return _has_content_match(build_file, ['javadoc', 'maven-javadoc-plugin', 'org.gradle.api.tasks.javadoc'])
    
    return False

def _check_jsdoc(path: Path) -> bool:
    # Check for JSDoc configuration files
    jsdoc_files = [
        path / 'jsdoc.json',
        path / '.jsdoc.json',
        path / 'conf.json',
        path / '.jsdoc.conf.json',
        path / 'jsdoc.conf.json'
    ]
    
    for config_file in jsdoc_files:
        if config_file.exists():
            return _has_content_match(config_file, ['jsdoc', 'plugins', 'templates'])
    
    # Check package.json for JSDoc
    package_json = path / 'package.json'
    if package_json.exists():
        try:
            with open(package_json) as f:
                data = json.load(f)
                deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                return any('jsdoc' in dep for dep in deps)
        except Exception:
            pass
    
    # Look for JS/TS files with JSDoc comments
    for ext in ['.js', '.jsx', '.ts', '.tsx']:
        for js_file in path.glob(f'**/*{ext}'):
            if _has_content_match(js_file, ['/**', '@param', '@returns', '@type', '@typedef', '@module']):
                return True
    
    return False

def _check_jupyter(path: Path) -> bool:
    # Check for Jupyter notebooks
    for notebook in path.glob('**/*.ipynb'):
        try:
            with open(notebook) as f:
                data = json.load(f)
                if 'cells' in data and 'metadata' in data:
                    return True
        except Exception:
            continue
    
    # Check for Jupyter configuration files
    jupyter_files = [
        path / '.jupyter',
        path / 'jupyter_notebook_config.py',
        path / 'jupyter_notebook_config.json'
    ]
    
    return any(f.exists() for f in jupyter_files)

def _check_markdown(path: Path) -> bool:
    # Look for Markdown files with specific documentation patterns
    doc_patterns = [
        '# ', '## ', '### ',  # Headers
        '```', '~~~',         # Code blocks
        '- [ ]', '- [x]',     # Task lists
        '[TOC]', '{{TOC}}',   # Table of contents
        '|---',               # Tables
    ]
    
    for md_file in path.glob('**/*.md'):
        if _has_content_match(md_file, doc_patterns):
            return True
    
    return False

def _check_openapi(path: Path) -> bool:
    # Check for OpenAPI/Swagger files
    api_files = [
        'swagger.yaml', 'swagger.yml', 'swagger.json',
        'openapi.yaml', 'openapi.yml', 'openapi.json',
        'api.yaml', 'api.yml', 'api.json'
    ]
    
    for api_file in api_files:
        file_path = path / api_file
        if file_path.exists():
            try:
                content = file_path.read_text(encoding='utf-8')
                if '.json' in api_file:
                    data = json.loads(content)
                    if any(key in data for key in ['swagger', 'openapi']):
                        return True
                else:
                    if any(pattern in content for pattern in ['swagger:', 'openapi:', 'info:', 'paths:']):
                        return True
            except Exception:
                continue
    
    return False

def _check_readthedocs(path: Path) -> bool:
    # Check for Read the Docs configuration files
    rtd_files = [
        path / '.readthedocs.yaml',
        path / '.readthedocs.yml',
        path / 'readthedocs.yaml',
        path / 'readthedocs.yml',
        path / '.readthedocs' / 'config.yaml'
    ]
    
    for config_file in rtd_files:
        if config_file.exists():
            return _has_content_match(config_file, ['version:', 'python:', 'sphinx:', 'mkdocs:'])
    
    # Check for Read the Docs integration in other configuration files
    if (path / '.github' / 'workflows').exists():
        for workflow in (path / '.github' / 'workflows').glob('*.yml'):
            if _has_content_match(workflow, ['readthedocs', 'Read the Docs']):
                return True
    
    return False

def _check_restructuredtext(path: Path) -> bool:
    # Look for reStructuredText files with specific patterns
    rst_patterns = [
        '===', '---', '^^^',  # Section headers
        '.. toctree::',       # Table of contents
        '.. code-block::',    # Code blocks
        ':ref:',              # Cross-references
        '.. note::',          # Directives
        '.. warning::',
        '|release|'           # Substitutions
    ]
    
    for rst_file in path.glob('**/*.rst'):
        if _has_content_match(rst_file, rst_patterns):
            return True
    
    return False

def _check_rustdoc(path: Path) -> bool:
    # Check for Rust project
    if not (path / 'Cargo.toml').exists():
        return False
    
    # Look for Rust files with documentation comments
    for rust_file in path.glob('**/*.rs'):
        if _has_content_match(rust_file, ['///', '//!', '# Examples', '# Panics', '# Safety']):
            return True
    
    # Check Cargo.toml for documentation features
    cargo_toml = path / 'Cargo.toml'
    if cargo_toml.exists():
        return _has_content_match(cargo_toml, ['[package.metadata.docs.rs]', 'documentation ='])
    
    return False

def _check_vuepress(path: Path) -> bool:
    # Check for VuePress configuration files
    vuepress_files = [
        path / '.vuepress/config.js',
        path / '.vuepress/config.ts',
        path / 'docs/.vuepress/config.js',
        path / 'docs/.vuepress/config.ts'
    ]
    
    for config_file in vuepress_files:
        if config_file.exists():
            return _has_content_match(config_file, ['module.exports', 'export default', 'title:', 'description:'])
    
    # Check package.json for VuePress
    package_json = path / 'package.json'
    if package_json.exists():
        try:
            with open(package_json) as f:
                data = json.load(f)
                deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                return any('vuepress' in dep for dep in deps)
        except Exception:
            pass
    
    # Check for VuePress directory structure
    return (path / '.vuepress').exists() or (path / 'docs' / '.vuepress').exists()

FRAMEWORK_CHECKS: Dict[str, Callable[[Path], bool]] = {
    'sphinx': _check_sphinx,
    'mkdocs': _check_mkdocs,
    'docusaurus': _check_docusaurus,
    'jekyll': _check_jekyll,
    'hugo': _check_hugo,
    'apiblueprint': _check_apiblueprint,
    'asciidoc': _check_asciidoc,
    'docsify': _check_docsify,
    'doxygen': _check_doxygen,
    'gitbook': _check_gitbook,
    'godoc': _check_godoc,
    'javadoc': _check_javadoc,
    'jsdoc': _check_jsdoc,
    'jupyter': _check_jupyter,
    'markdown': _check_markdown,
    'openapi': _check_openapi,
    'readthedocs': _check_readthedocs,
    'restructuredtext': _check_restructuredtext,
    'rustdoc': _check_rustdoc,
    'vuepress': _check_vuepress,
}

def detect_framework(repo_path: Path) -> str:
    """
    Detect the documentation framework used in the repository.

    Args:
        repo_path (Path): Path to the repository root.

    Returns:
        str: The detected framework name, or 'unknown' if not detected.

    Raises:
        ValueError: If the repo_path does not exist.
    """
    if not repo_path.exists():
        logger.error(f"Repository path does not exist: {repo_path}")
        raise ValueError(f"Repository path does not exist: {repo_path}")

    for framework, check_func in FRAMEWORK_CHECKS.items():
        if check_func(repo_path):
            logger.info(f"Detected framework: {framework}")
            return framework

    # If no specific framework is detected, check for common documentation files
    common_docs = ['README.md', 'README.rst', 'index.md', 'index.rst']
    for doc in common_docs:
        if (repo_path / doc).exists():
            logger.info(f"Detected common documentation file: {doc}")
            return 'common'

    logger.warning("No known documentation framework detected")
    return 'unknown'
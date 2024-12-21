import shutil
import subprocess
import sys
import logging
import pkg_resources
from typing import List, Dict

logger = logging.getLogger(__name__)

EXTERNAL_DEPENDENCIES = {
    'node': ('node', '--version'),
    'npm': ('npm', '--version'),
    'ruby': ('ruby', '--version'),
    'bundler': ('bundle', '--version'),
    'hugo': ('hugo', 'version'),
    'doxygen': ('doxygen', '--version'),
    'javac': ('javac', '-version'),
    'rustc': ('rustc', '--version'),
    'go': ('go', 'version'),
}

PYTHON_DEPENDENCIES = {
    'mkdocs': [
        'mkdocs>=1.2.0',
        'mkdocs-material>=8.0.0',
        'pymdown-extensions>=9.0',
        'mkdocs-material-extensions>=1.0',
        'mkdocs-pymdownx-material-extras>=2.0',
        'mkdocstrings>=0.18.0',
        'mkdocs-git-revision-date-localized-plugin>=1.0',
    ],
    'sphinx': ['sphinx>=4.0.0'],
    'jupyter': ['nbconvert>=6.1.0'],
    'asciidoc': ['asciidoc>=9.1.0'],
    'restructuredtext': ['docutils>=0.17.1'],
    'markdown': ['markdown>=3.3.4'],
}

INSTALLATION_INSTRUCTIONS = {
    'node': "Please install Node.js from https://nodejs.org/",
    'npm': "npm is included with Node.js. Please install Node.js from https://nodejs.org/",
    'ruby': "Please install Ruby from https://www.ruby-lang.org/",
    'bundler': "Please install Bundler using 'gem install bundler'",
    'hugo': "Please install Hugo from https://gohugo.io/",
    'doxygen': "Please install Doxygen from https://www.doxygen.nl/",
    'javac': "Please install Java JDK from https://www.oracle.com/java/technologies/javase-jdk11-downloads.html",
    'rustc': "Please install Rust from https://www.rust-lang.org/",
    'go': "Please install Go from https://golang.org/",
}

def check_dependencies(framework: str) -> List[str]:
    """
    Check if all required dependencies for a framework are installed.

    Args:
        framework (str): The documentation framework to check dependencies for.

    Returns:
        List[str]: List of missing dependencies.
    """
    missing = []

    # Check external dependencies
    if framework == 'docusaurus':
        missing.extend(_check_external_dep('node'))
        missing.extend(_check_external_dep('npm'))
    elif framework == 'jekyll':
        missing.extend(_check_external_dep('ruby'))
        missing.extend(_check_external_dep('bundler'))
    elif framework == 'hugo':
        missing.extend(_check_external_dep('hugo'))
    elif framework in ['vuepress', 'docsify', 'gitbook', 'jsdoc']:
        missing.extend(_check_external_dep('node'))
        missing.extend(_check_external_dep('npm'))
    elif framework == 'doxygen':
        missing.extend(_check_external_dep('doxygen'))
    elif framework == 'javadoc':
        missing.extend(_check_external_dep('javac'))
    elif framework == 'rustdoc':
        missing.extend(_check_external_dep('rustc'))
    elif framework == 'godoc':
        missing.extend(_check_external_dep('go'))

    # Check Python package dependencies
    if framework in PYTHON_DEPENDENCIES:
        missing.extend(_check_python_deps(framework))
    
    return missing

def _check_external_dep(dep: str) -> List[str]:
    """Check if an external dependency is installed."""
    if shutil.which(EXTERNAL_DEPENDENCIES[dep][0]) is None:
        return [dep]
    return []

def _check_python_deps(framework: str) -> List[str]:
    """Check if Python package dependencies are installed."""
    missing = []
    for req in PYTHON_DEPENDENCIES[framework]:
        try:
            pkg_resources.require(req)
        except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
            missing.append(req)
    return missing

def get_installation_instructions(missing_deps: List[str]) -> List[str]:
    """Get installation instructions for missing dependencies."""
    instructions = []
    
    # Instructions for external dependencies
    for dep in missing_deps:
        if dep in INSTALLATION_INSTRUCTIONS:
            instructions.append(INSTALLATION_INSTRUCTIONS[dep])
    
    # Instructions for Python packages
    python_deps = [dep for dep in missing_deps if dep not in INSTALLATION_INSTRUCTIONS]
    if python_deps:
        deps_str = ' '.join(python_deps)
        instructions.append(f"Install Python packages using: pip install {deps_str}")
    
    return instructions
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Base requirements
base_requirements = [
    "requests>=2.26.0",
    "PyYAML>=5.4.1",
    "gitpython>=3.1.24",
    "html2text",
    "nbconvert",
    "nbformat",
    "docutils",
    "toml",
    "click>=8.0.0",
    "beautifulsoup4>=4.9.3",
]

# Additional requirements for each framework
extra_requirements = {
    'sphinx': ['sphinx>=4.0.0'],
    'mkdocs': [
        'mkdocs>=1.2.0',
        'mkdocs-material>=8.0.0',
        'pymdown-extensions>=9.0',  # For superfences and other extensions
        'mkdocs-material-extensions>=1.0',
        'mkdocs-pymdownx-material-extras>=2.0',
        'mkdocstrings>=0.18.0',
        'mkdocs-git-revision-date-localized-plugin>=1.0',
    ],
    'docusaurus': [],  # Requires Node.js and npm
    'jekyll': [],  # Requires Ruby and Bundler
    'hugo': [],  # Requires Hugo binary
    'vuepress': [],  # Requires Node.js and npm
    'docsify': [],  # Requires Node.js and npm
    'gitbook': [],  # Requires Node.js and npm
    'doxygen': [],  # Requires Doxygen binary
    'javadoc': [],  # Requires Java JDK
    'jsdoc': [],  # Requires Node.js and npm
    'rustdoc': [],  # Requires Rust and Cargo
    'godoc': [],  # Requires Go
    'jupyter': ['nbconvert>=6.1.0'],
    'asciidoc': ['asciidoc>=9.1.0'],
    'restructuredtext': ['docutils>=0.17.1'],
    'markdown': ['markdown>=3.3.4'],
}

# All requirements
all_requirements = base_requirements + [req for reqs in extra_requirements.values() for req in reqs]

setuptools.setup(
    name="docsforai",
    version="0.1.0",
    author="Ram Chandalada",
    description="A tool for building, consolidating, and downloading documentation for various software projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/0-hero/docsforai",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=base_requirements,
    extras_require={
        'all': all_requirements,
        **extra_requirements
    },
    entry_points={
        "console_scripts": [
            "docsforai=docsforai.cli:main",
        ],
    },
    include_package_data=True,
)
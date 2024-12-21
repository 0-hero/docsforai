# DocsForAI User Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Supported Documentation Frameworks](#supported-documentation-frameworks)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

## Introduction

DocsForAI is a powerful tool designed to build, consolidate, and download documentation for various software projects. It supports multiple documentation frameworks and provides a unified output format, making it easier to manage and distribute documentation across different projects.

## Installation

To install DocsForAI, you need Python 3.7 or later. You can install it using pip:

```bash
pip install docsforai
```

For development installations, clone the repository and install in editable mode:

```bash
git clone https://github.com/docsforai/docsforai.git
cd docsforai
pip install -e .
```

## Dependencies

DocsForAI supports various documentation frameworks, some of which require external dependencies. When you try to build documentation for a specific framework, DocsForAI will check for the necessary dependencies and provide instructions if any are missing.

Here are some common external dependencies:

- Node.js and npm: Required for Docusaurus, VuePress, Docsify, GitBook, and JSDoc
- Ruby and Bundler: Required for Jekyll
- Hugo: Required for Hugo sites
- Doxygen: Required for C++ documentation
- Java JDK: Required for Javadoc
- Rust and Cargo: Required for Rustdoc
- Go: Required for Godoc

When installing DocsForAI, you can choose to install only the basic functionality or include additional Python dependencies for specific frameworks:

```bash
pip install docsforai  # Basic installation
pip install docsforai[all]  # Full installation with all Python dependencies
pip install docsforai[sphinx,mkdocs]  # Install with Sphinx and MkDocs support
```

## Configuration

DocsForAI uses a YAML configuration file to specify the documentation build process. Here's a sample configuration:

```yaml
package_name: "example-package"
version: "1.0.0"
source:
  type: "github"
  url: "https://github.com/username/example-package"
docs:
  path: "docs"
  framework: "auto"
output:
  path: "./built_docs"
  format: "markdown"
  single_file: true
  filename: "complete_docs.md"
```

For a full list of configuration options, see the [Configuration Reference](#configuration-reference).

## Usage

DocsForAI provides two main commands:

1. Building documentation:

```bash
docsforai build path/to/config.yaml
```

2. Downloading pre-built documentation:

```bash
docsforai download package-name [--version VERSION]
```

### Building Documentation

To build documentation, create a configuration file and run:

```bash
docsforai build config.yaml
```

This will clone the repository, detect the documentation framework (if set to "auto"), parse the documentation, and generate a consolidated output file.

### Downloading Pre-built Documentation

To download pre-built documentation for a package:

```bash
docsforai download numpy --version 1.21.0
```

If no version is specified, it will download the latest version.

## Supported Documentation Frameworks

DocsForAI supports the following documentation frameworks:

- Sphinx
- MkDocs
- Docusaurus
- Jekyll
- Hugo
- VuePress
- Docsify
- GitBook
- Read the Docs
- Doxygen
- Javadoc
- JSDoc
- Rustdoc
- Godoc

It also supports common markup formats like Markdown, reStructuredText, AsciiDoc, and Jupyter Notebooks.

## Troubleshooting

### Common Issues

1. **Git clone fails**: Ensure you have git installed and have the necessary permissions to clone the repository.
2. **Framework detection fails**: Specify the framework explicitly in the configuration file if auto-detection doesn't work.
3. **Build process hangs**: Check your internet connection and ensure you have all necessary dependencies installed.

### Logging

DocsForAI uses Python's logging module. To enable debug logging, set the environment variable:

```bash
export DOCSFORAI_LOG_LEVEL=DEBUG
```

## FAQ

1. **Q: Can I use DocsForAI with private repositories?**
   A: Yes, you can use personal access tokens for authentication. Set the `DOCSFORAI_GITHUB_TOKEN` environment variable.

2. **Q: How do I exclude certain files from the documentation?**
   A: Use the `exclude_patterns` option in the consolidation section of your configuration file.

3. **Q: Can I customize the output format?**
   A: Currently, DocsForAI supports Markdown and HTML output. For more advanced customization, you can modify the output template.

## Configuration Reference

| Option | Description | Default |
|--------|-------------|---------|
| `package_name` | Name of the package | Required |
| `version` | Version of the package | Latest |
| `source.type` | Type of source repository | github |
| `source.url` | URL of the source repository | Required |
| `docs.path` | Path to documentation in the repository | docs |
| `docs.framework` | Documentation framework to use | auto |
| `output.path` | Output directory for built documentation | ./built_docs |
| `output.format` | Output format (markdown or html) | markdown |
| `output.single_file` | Whether to consolidate into a single file | true |
| `output.filename` | Name of the output file | complete_docs.md |

For more detailed information on each configuration option, refer to the comments in the [config_template.yaml](../templates/config_template.yaml) file.

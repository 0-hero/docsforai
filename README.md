# DocsForAI

DocsForAI is a powerful tool designed to build, consolidate, and download documentation for various software projects. It supports multiple documentation frameworks and provides a unified output format, making it easier to manage and distribute documentation across different projects.

## Features

- Supports multiple documentation frameworks (Sphinx, MkDocs, Docusaurus, etc.)
- Consolidates documentation into a single file
- Downloads pre-built documentation for popular packages
- Converts between different documentation formats

## Installation

You can install DocsForAI using pip:

```bash
pip install docsforai  # Basic installation (downloader only)
pip install docsforai[all]  # Full installation with all dependencies
```
You can also install specific framework dependencies:
```bash
pip install docsforai[sphinx]  # Install with Sphinx support
pip install docsforai[mkdocs,jupyter]  # Install with MkDocs and Jupyter support
```

## Quick Start

1. Create a configuration file `config.yaml`:

```yaml
package_name: "example-package"
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

2. Build documentation:

```bash
docsforai build config.yaml
```

3. Download pre-built documentation:

```bash
docsforai download numpy --version 1.21.0
```

For more detailed information, please refer to our [User Guide](docs/user_guide.md).

## Contributing

We welcome contributions! Please see our [Contributing Guide](docs/contributing.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

4. `requirements.txt`:

```
requests==2.26.0
PyYAML==5.4.1
beautifulsoup4==4.10.0
html2text==2020.1.16
nbconvert==6.1.0
docutils==0.17.1
gitpython==3.1.24
```

5. `LICENSE`:

Make sure to include a LICENSE file in your project. Here's an example using the MIT License:

```
MIT License

Copyright (c) 2023 DocsForAI Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
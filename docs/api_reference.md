# DocsForAI API Reference

## Table of Contents

1. [Builder Module](#builder-module)
2. [Downloader Module](#downloader-module)
3. [Converter Module](#converter-module)
4. [Utils Module](#utils-module)

## Builder Module

The builder module is responsible for building and consolidating documentation.

### `build_documentation(config_path: Path) -> str`

Build and consolidate documentation based on the provided configuration.

**Parameters:**
- `config_path` (Path): Path to the configuration file.

**Returns:**
- str: A message indicating the result of the build process.

**Raises:**
- ValueError: If the configuration is invalid or the build process fails.

### `detect_framework(repo_path: Path) -> str`

Detect the documentation framework used in the repository.

**Parameters:**
- `repo_path` (Path): Path to the repository root.

**Returns:**
- str: The detected framework name, or 'unknown' if not detected.

### `parse_documentation(docs_path: Path, framework: str) -> List[Dict[str, Any]]`

Parse documentation files based on the detected framework.

**Parameters:**
- `docs_path` (Path): Path to the documentation directory.
- `framework` (str): The detected documentation framework.

**Returns:**
- List[Dict[str, Any]]: A list of parsed documentation elements.

### `consolidate_documentation(parsed_docs: List[Dict[str, Any]], consolidation_config: Dict[str, Any], metadata: Dict[str, str]) -> str`

Consolidate parsed documentation into a single Markdown file.

**Parameters:**
- `parsed_docs` (List[Dict[str, Any]]): List of parsed documentation elements.
- `consolidation_config` (Dict[str, Any]): Configuration for consolidation.
- `metadata` (Dict[str, str]): Metadata to include in the consolidated documentation.

**Returns:**
- str: Consolidated documentation as a Markdown string.

## Downloader Module

The downloader module handles downloading pre-built documentation from various sources.

### `download_from_github(package_name: str, version: Optional[str] = None, output_dir: Path = Path("./docs")) -> str`

Download pre-built documentation for a package from GitHub.

**Parameters:**
- `package_name` (str): Name of the package.
- `version` (Optional[str]): Specific version to download. If None, downloads the latest version.
- `output_dir` (Path): Directory to save the downloaded documentation.

**Returns:**
- str: Path to the downloaded documentation.

**Raises:**
- ValueError: If the package or version is not found.
- requests.RequestException: If there's an error communicating with the GitHub API.

## Converter Module

The converter module provides functionality to convert between different documentation formats.

### `rst_to_md(rst_content: str) -> str`

Convert reStructuredText to Markdown.

**Parameters:**
- `rst_content` (str): reStructuredText content.

**Returns:**
- str: Converted Markdown content.

### `adoc_to_md(adoc_content: str) -> str`

Convert AsciiDoc to Markdown.

**Parameters:**
- `adoc_content` (str): AsciiDoc content.

**Returns:**
- str: Converted Markdown content.

### `html_to_md(html_content: str) -> str`

Convert HTML to Markdown.

**Parameters:**
- `html_content` (str): HTML content.

**Returns:**
- str: Converted Markdown content.

### `ipynb_to_md(ipynb_content: str) -> str`

Convert Jupyter Notebook to Markdown.

**Parameters:**
- `ipynb_content` (str): Jupyter Notebook content as JSON string.

**Returns:**
- str: Converted Markdown content.

## Utils Module

The utils module contains various utility functions used throughout the project.

### `parse_config(config_path: Path) -> Dict[str, Any]`

Parse the configuration file.

**Parameters:**
- `config_path` (Path): Path to the configuration file.

**Returns:**
- Dict[str, Any]: Parsed configuration.

**Raises:**
- FileNotFoundError: If the configuration file is not found.
- yaml.YAMLError: If the configuration file is not valid YAML.
- ValueError: If the configuration is invalid.

### `clone_repository(repo_url: str, target_dir: Path, branch: Optional[str] = None) -> Path`

Clone a Git repository.

**Parameters:**
- `repo_url` (str): URL of the Git repository.
- `target_dir` (Path): Directory to clone the repository into.
- `branch` (Optional[str]): Specific branch to clone. If None, clones the default branch.

**Returns:**
- Path: Path to the cloned repository.

**Raises:**
- subprocess.CalledProcessError: If the Git command fails.
- FileExistsError: If the target directory is not empty.

### `create_directory(path: Union[str, Path]) -> Path`

Create a directory if it doesn't exist.

**Parameters:**
- `path` (Union[str, Path]): Path to the directory.

**Returns:**
- Path: Path to the created directory.

**Raises:**
- OSError: If directory creation fails.

### `cleanup_directory(path: Union[str, Path]) -> None`

Remove a directory and its contents.

**Parameters:**
- `path` (Union[str, Path]): Path to the directory to be removed.

**Raises:**
- OSError: If directory removal fails.

### `check_dependencies() -> List[str]`

Check for required dependencies.

**Returns:**
- List[str]: List of missing dependencies.

### `install_dependency(dependency: str) -> bool`

Attempt to install a dependency.

**Parameters:**
- `dependency` (str): Name of the dependency to install.

**Returns:**
- bool: True if installation was successful, False otherwise.

For more detailed information on each function and its implementation, refer to the source code and inline documentation.
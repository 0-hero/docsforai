# Contributing to DocsForAI

We welcome contributions to DocsForAI! This document provides guidelines for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [How to Contribute](#how-to-contribute)
4. [Development Setup](#development-setup)
5. [Coding Standards](#coding-standards)
6. [Testing](#testing)
7. [Documentation](#documentation)
8. [Submitting Changes](#submitting-changes)
9. [Review Process](#review-process)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork locally: `git clone https://github.com/your-username/docsforai.git`
3. Create a new branch for your feature or bug fix: `git checkout -b feature-or-fix-name`

## How to Contribute

1. Ensure the bug or feature hasn't already been reported or worked on by checking the [Issues](https://github.com/docsforai/docsforai/issues) and [Pull Requests](https://github.com/docsforai/docsforai/pulls).
2. For bugs, open an issue describing the bug and include steps to reproduce it.
3. For features, open an issue describing the new feature and its potential benefits.
4. Wait for approval or feedback before starting work on the issue.

## Development Setup

1. Create a virtual environment: `python -m venv venv`
2. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`
3. Install the development dependencies: `pip install -r requirements-dev.txt`
4. Install the package in editable mode: `pip install -e .`

## Coding Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code.
- Use type hints for function arguments and return values.
- Write clear, concise comments and docstrings.
- Use meaningful variable and function names.

We use `flake8` for linting and `black` for code formatting. Run these before submitting your changes:

```bash
flake8 .
black .
```

## Testing

- Write unit tests for all new functionality.
- Ensure all existing tests pass before submitting changes.
- Aim for high test coverage (we use `pytest-cov` to measure coverage).

To run tests:

```bash
pytest
```

To run tests with coverage:

```bash
pytest --cov=docsforai
```

## Documentation

- Update the documentation for any changes in functionality.
- Write clear and concise documentation that follows our existing style.
- Update the [API Reference](api_reference.md) for any changes to the public API.

## Submitting Changes

1. Commit your changes: `git commit -am 'Add some feature'`
2. Push to your fork: `git push origin feature-or-fix-name`
3. Submit a pull request to the `main` branch of the original repository.

Ensure your pull request:
- Clearly describes the problem and solution
- Includes any relevant issue numbers
- Contains only commits relevant to the feature or bug fix

## Review Process

1. At least one core contributor must approve the changes.
2. All automated checks (tests, linting, etc.) must pass.
3. Any requested changes must be addressed before merging.

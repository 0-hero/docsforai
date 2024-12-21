import pytest
from docsforai.converter.rst_to_md import rst_to_md
from docsforai.converter.adoc_to_md import adoc_to_md
from docsforai.converter.html_to_md import html_to_md
from docsforai.converter.ipynb_to_md import ipynb_to_md
from unittest.mock import patch, MagicMock

def test_rst_to_md():
    rst_content = """
    Test Title
    ==========
    
    This is a test paragraph.
    
    * List item 1
    * List item 2
    
    .. code-block:: python
    
        print("Hello, World!")
    """
    md_content = rst_to_md(rst_content)
    
    assert '# Test Title' in md_content
    assert 'This is a test paragraph.' in md_content
    assert '* List item 1' in md_content
    assert '```python' in md_content
    assert 'print("Hello, World!")' in md_content

@patch('docsforai.converter.adoc_to_md.subprocess.run')
def test_adoc_to_md(mock_run):
    mock_result = MagicMock()
    mock_result.stdout = "# Converted AsciiDoc\n\nThis is a paragraph."
    mock_run.return_value = mock_result

    adoc_content = "= AsciiDoc Title\n\nThis is a paragraph."
    md_content = adoc_to_md(adoc_content)

    assert '# Converted AsciiDoc' in md_content
    assert 'This is a paragraph.' in md_content

def test_html_to_md():
    html_content = """
    <h1>Test Title</h1>
    <p>This is a paragraph.</p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
    """
    md_content = html_to_md(html_content)

    assert '# Test Title' in md_content
    assert 'This is a paragraph.' in md_content
    assert '* Item 1' in md_content
    assert '* Item 2' in md_content

def test_ipynb_to_md():
    ipynb_content = """
    {
     "cells": [
      {
       "cell_type": "markdown",
       "metadata": {},
       "source": [
        "# Notebook Title\\n",
        "\\n",
        "This is a markdown cell."
       ]
      },
      {
       "cell_type": "code",
       "execution_count": null,
       "metadata": {},
       "outputs": [],
       "source": [
        "print(\\"Hello, World!\\")"
       ]
      }
     ],
     "metadata": {
      "kernelspec": {
       "display_name": "Python 3",
       "language": "python",
       "name": "python3"
      }
     },
     "nbformat": 4,
     "nbformat_minor": 2
    }
    """
    md_content = ipynb_to_md(ipynb_content)

    assert '# Notebook Title' in md_content
    assert 'This is a markdown cell.' in md_content
    assert 'print("Hello, World!")' in md_content

def test_rst_to_md_error_handling():
    with pytest.raises(ValueError, match="Failed to convert RST to Markdown"):
        rst_to_md("Invalid RST Content")

@patch('docsforai.converter.adoc_to_md.subprocess.run')
def test_adoc_to_md_error_handling(mock_run):
    mock_run.side_effect = Exception("Pandoc error")
    
    with pytest.raises(ValueError, match="Failed to convert AsciiDoc to Markdown"):
        adoc_to_md("Test AsciiDoc")

def test_html_to_md_error_handling():
    with pytest.raises(ValueError, match="Failed to convert HTML to Markdown"):
        html_to_md("<invalid>HTML</invalid>")

def test_ipynb_to_md_error_handling():
    with pytest.raises(ValueError, match="Invalid Jupyter Notebook format"):
        ipynb_to_md("Invalid JSON")
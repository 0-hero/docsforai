import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from docsforai.builder import build_documentation
from docsforai.builder.detector import detect_framework
from docsforai.builder.parser import parse_documentation
from docsforai.builder.consolidator import consolidate_documentation

@pytest.fixture
def mock_config():
    return {
        'package_name': 'test-package',
        'source': {'url': 'https://github.com/test/repo'},
        'docs': {'path': 'docs', 'framework': 'auto'},
        'output': {'path': 'output', 'filename': 'test_docs.md'},
        'consolidation': {'include_changelog': True, 'changelog_path': 'CHANGELOG.md'},
        'metadata': {'author': 'Test Author'}
    }

@pytest.fixture
def mock_repo_path(tmp_path):
    repo_path = tmp_path / "repo"
    repo_path.mkdir()
    (repo_path / "docs").mkdir()
    (repo_path / "docs" / "index.md").write_text("# Test Documentation")
    return repo_path

def test_detect_framework(mock_repo_path):
    assert detect_framework(mock_repo_path) == 'common'

    (mock_repo_path / "docs" / "conf.py").touch()
    assert detect_framework(mock_repo_path) == 'sphinx'

def test_parse_documentation(mock_repo_path):
    parsed_docs = parse_documentation(mock_repo_path / "docs", 'common')
    assert len(parsed_docs) == 1
    assert parsed_docs[0]['filename'] == 'index.md'
    assert parsed_docs[0]['content'] == '# Test Documentation'

def test_consolidate_documentation():
    parsed_docs = [
        {'filename': 'index.md', 'content': '# Index'},
        {'filename': 'api.md', 'content': '## API'}
    ]
    config = {'include_changelog': False}
    metadata = {'package_name': 'test-package', 'author': 'Test Author'}
    
    consolidated = consolidate_documentation(parsed_docs, config, metadata)
    assert '# test-package' in consolidated
    assert '# Index' in consolidated
    assert '## API' in consolidated

@patch('docsforai.builder.clone_repository')
@patch('docsforai.builder.parse_documentation')
@patch('docsforai.builder.consolidate_documentation')
def test_build_documentation(mock_consolidate, mock_parse, mock_clone, mock_config, tmp_path):
    mock_clone.return_value = tmp_path / "repo"
    mock_parse.return_value = [{'filename': 'test.md', 'content': 'Test content'}]
    mock_consolidate.return_value = "Consolidated content"

    result = build_documentation(Path('test_config.yaml'))
    
    assert "Documentation successfully built" in result
    assert (tmp_path / "output" / "test_docs.md").exists()

@pytest.mark.parametrize("framework", ['sphinx', 'mkdocs', 'docusaurus', 'jekyll', 'hugo'])
def test_parse_documentation_frameworks(framework, mock_repo_path):
    with patch(f'docsforai.builder.frameworks.{framework}.parse_{framework}') as mock_parse:
        mock_parse.return_value = [{'filename': 'test.md', 'content': f'{framework} content'}]
        result = parse_documentation(mock_repo_path, framework)
        assert result[0]['content'] == f'{framework} content'

def test_build_documentation_error_handling(mock_config):
    with pytest.raises(ValueError):
        build_documentation(Path('non_existent_config.yaml'))

    with patch('docsforai.builder.parse_config', return_value=mock_config):
        with patch('docsforai.builder.clone_repository', side_effect=Exception("Clone failed")):
            with pytest.raises(Exception, match="Clone failed"):
                build_documentation(Path('test_config.yaml'))
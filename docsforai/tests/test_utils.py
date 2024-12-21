import pytest
from pathlib import Path
from docsforai.utils.config_parser import parse_config, _validate_config
from docsforai.utils.git_handler import clone_repository, update_repository
from docsforai.utils.file_utils import create_directory, cleanup_directory, read_file, write_file
from docsforai.utils.dependency_manager import check_dependencies, install_dependency
from unittest.mock import patch, MagicMock

# Config Parser Tests

def test_parse_config(tmp_path):
    config_content = """
    package_name: test-package
    source:
      url: https://github.com/test/repo
    docs:
      path: docs
    output:
      path: ./output
    """
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content)

    config = parse_config(config_file)
    assert config['package_name'] == 'test-package'
    assert config['source']['url'] == 'https://github.com/test/repo'

def test_validate_config():
    valid_config = {
        'package_name': 'test',
        'source': {'url': 'https://github.com/test/repo'},
        'docs': {'path': 'docs'},
        'output': {'path': 'output'}
    }
    _validate_config(valid_config)  # Should not raise an exception

    invalid_config = {'package_name': 'test'}
    with pytest.raises(ValueError):
        _validate_config(invalid_config)

# Git Handler Tests

@patch('docsforai.utils.git_handler.subprocess.run')
def test_clone_repository(mock_run, tmp_path):
    repo_url = 'https://github.com/test/repo'
    clone_repository(repo_url, tmp_path)
    mock_run.assert_called_once()
    assert 'git clone' in ' '.join(mock_run.call_args[0][0])

@patch('docsforai.utils.git_handler.subprocess.run')
def test_update_repository(mock_run, tmp_path):
    update_repository(tmp_path)
    mock_run.assert_called_once()
    assert 'git pull' in ' '.join(mock_run.call_args[0][0])

# File Utils Tests

def test_create_directory(tmp_path):
    new_dir = tmp_path / "new_dir"
    created_dir = create_directory(new_dir)
    assert created_dir.exists()
    assert created_dir.is_dir()

def test_cleanup_directory(tmp_path):
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    (test_dir / "test_file.txt").touch()
    
    cleanup_directory(test_dir)
    assert not test_dir.exists()

def test_read_file(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Test content")
    
    content = read_file(test_file)
    assert content == "Test content"

def test_write_file(tmp_path):
    test_file = tmp_path / "test.txt"
    write_file(test_file, "New content")
    
    assert test_file.read_text() == "New content"

# Dependency Manager Tests

@patch('docsforai.utils.dependency_manager.subprocess.run')
def test_check_dependencies(mock_run):
    mock_run.return_value = MagicMock(returncode=0)
    missing = check_dependencies()
    assert len(missing) == 0

    mock_run.side_effect = FileNotFoundError
    missing = check_dependencies()
    assert len(missing) > 0

@patch('docsforai.utils.dependency_manager.subprocess.run')
def test_install_dependency(mock_run):
    result = install_dependency('mkdocs')
    assert result == True
    mock_run.assert_called_once()

    result = install_dependency('unknown_dependency')
    assert result == False

# Error Handling Tests

def test_parse_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        parse_config(Path('non_existent_config.yaml'))

@patch('docsforai.utils.git_handler.subprocess.run')
def test_clone_repository_error(mock_run):
    mock_run.side_effect = Exception("Git error")
    with pytest.raises(Exception, match="Git error"):
        clone_repository('https://github.com/test/repo', Path('/tmp'))

def test_read_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_file(tmp_path / "non_existent.txt")

def test_write_file_permission_error(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.touch()
    test_file.chmod(0o444)  # Read-only

    with pytest.raises(IOError):
        write_file(test_file, "New content")
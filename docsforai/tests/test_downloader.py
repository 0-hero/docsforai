import pytest
from unittest.mock import patch, MagicMock
from docsforai.downloader.github_api import download_from_github, _get_specific_version, _get_latest_version
from pathlib import Path

@pytest.fixture
def mock_requests_get():
    with patch('docsforai.downloader.github_api.requests.get') as mock_get:
        yield mock_get

def test_download_from_github(mock_requests_get, tmp_path):
    mock_response = MagicMock()
    mock_response.json.return_value = {'content': 'SGVsbG8gV29ybGQ='}  # Base64 for "Hello World"
    mock_requests_get.return_value = mock_response

    result = download_from_github('test-package', output_dir=tmp_path)
    
    assert result == str(tmp_path / 'test-package.md')
    assert Path(result).read_text() == 'Hello World'

def test_download_from_github_specific_version(mock_requests_get, tmp_path):
    mock_response = MagicMock()
    mock_response.json.return_value = {'content': 'VGVzdCBWZXJzaW9u'}  # Base64 for "Test Version"
    mock_requests_get.return_value = mock_response

    result = download_from_github('test-package', version='1.0.0', output_dir=tmp_path)
    
    assert result == str(tmp_path / 'test-package_1.0.0.md')
    assert Path(result).read_text() == 'Test Version'

def test_get_specific_version(mock_requests_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {'content': 'VGVzdCBWZXJzaW9u'}  # Base64 for "Test Version"
    mock_requests_get.return_value = mock_response

    result = _get_specific_version('test-package', '1.0.0')
    assert result == 'Test Version'

def test_get_latest_version(mock_requests_get):
    mock_response_list = MagicMock()
    mock_response_list.json.return_value = [
        {'name': '1.0.0.md', 'type': 'file'},
        {'name': '1.1.0.md', 'type': 'file'},
        {'name': '0.9.0.md', 'type': 'file'}
    ]
    mock_response_content = MagicMock()
    mock_response_content.json.return_value = {'content': 'TGF0ZXN0IFZlcnNpb24='}  # Base64 for "Latest Version"
    
    mock_requests_get.side_effect = [mock_response_list, mock_response_content]

    result = _get_latest_version('test-package')
    assert result == 'Latest Version'

def test_download_from_github_error_handling(mock_requests_get):
    mock_requests_get.side_effect = Exception("API Error")

    with pytest.raises(Exception, match="API Error"):
        download_from_github('test-package')

def test_get_latest_version_no_versions(mock_requests_get):
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_requests_get.return_value = mock_response

    with pytest.raises(ValueError, match="No documentation found"):
        _get_latest_version('test-package')
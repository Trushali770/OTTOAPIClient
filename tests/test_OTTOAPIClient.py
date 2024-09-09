import pytest
import json
import requests
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from WebAPIClient.Containers import JSONPlaceholderClient, load_config


@pytest.fixture
def client():
    return JSONPlaceholderClient()

@pytest.fixture
def mock_response():
    mock = MagicMock()
    mock.status_code = 200
    mock.json.return_value = {"id": 1, "title": "Test Post"}
    mock.content = b'{"id": 1, "title": "Test Post"}'
    return mock

# def test_load_config():
#     with patch('builtins.open', create=True) as mock_open:
#         mock_open.return_value.__enter__.return_value.read.return_value = '{"key": "value"}'
#         config = load_config('dummy_path')
#         assert config == {"key": "value"}

@patch('requests.get')
def test_get_posts(mock_get, client, mock_response):
    mock_get.return_value = mock_response
    result = client.get_posts()
    assert result == {"id": 1, "title": "Test Post"}
    mock_get.assert_called_once_with(f'{client.BASE_URL}/posts')

@patch('requests.get')
def test_get_post(mock_get, client, mock_response):
    mock_get.return_value = mock_response
    result = client.get_post(1)
    assert result == {"id": 1, "title": "Test Post"}
    mock_get.assert_called_once_with(f'{client.BASE_URL}/posts/1')

@patch('requests.post')
def test_create_post(mock_post, client, mock_response):
    mock_post.return_value = mock_response
    post_data = {"title": "New Post", "body": "Content"}
    result = client.create_post(post_data)
    assert result == {"id": 1, "title": "Test Post"}
    mock_post.assert_called_once_with(f'{client.BASE_URL}/posts', json=post_data)

@patch('requests.put')
def test_update_post(mock_put, client, mock_response):
    mock_put.return_value = mock_response
    post_data = {"title": "Updated Post", "body": "New Content"}
    result = client.update_post(1, post_data)
    assert result == {"id": 1, "title": "Test Post"}
    mock_put.assert_called_once_with(f'{client.BASE_URL}/posts/1', json=post_data)

@patch('requests.delete')
def test_delete_post(mock_delete, client, mock_response):
    mock_delete.return_value = mock_response
    result = client.delete_post(1)
    assert result == 200
    mock_delete.assert_called_once_with(f'{client.BASE_URL}/posts/1')

@pytest.mark.parametrize("method", ["get", "post", "put", "delete"])
def test_request_error(method, client):
    with patch(f'requests.{method}') as mock_request:
        mock_request.side_effect = requests.exceptions.RequestException("Error")
        with pytest.raises(requests.exceptions.RequestException):
            if method == "get":
                client.get_posts()
            elif method == "post":
                client.create_post({"title": "Test"})
            elif method == "put":
                client.update_post(1, {"title": "Test"})
            elif method == "delete":
                client.delete_post(1)
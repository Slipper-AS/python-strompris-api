from unittest.mock import patch
import pytest
from strompris_api import get_access_token, get_products

@patch('strompris_api.requests.post')
def test_get_access_token(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {'accessToken': 'test_token'}

    token = get_access_token('valid_client_id', 'valid_client_secret')

    assert token == 'test_token'

    with pytest.raises(ValueError):
        get_access_token('', '')


@patch('strompris_api.get_access_token')
@patch('strompris_api.requests.get')
def test_get_products(mock_get, mock_get_access_token):
    mock_get_access_token.return_value = 'test_token'
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'data': 'test_data'}

    products = get_products('2023-01-01')
    assert products == {'data': 'test_data'}

    with pytest.raises(ValueError):
        get_products('01-01-2023')
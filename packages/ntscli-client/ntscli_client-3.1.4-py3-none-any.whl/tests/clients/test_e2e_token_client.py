"""Tests for E2E Token Client"""
import pytest
from unittest.mock import Mock
from requests import Session, exceptions
from src.clients.e2e_token_client import E2ETokenClient


E2E_TOKEN_URL = "https://public.nflxe2etokens.prod.netflix.net/REST/v1/tokens/mint/metatron"
TEST_APP_NAME = "wall_e"


def test_e2e_token_client_success(mocker, mock_dump_all):
    """Test successful E2E token retrieval"""
    mock_token = "mock_token_abc123"
    
    mock_get = mocker.patch.object(Session, 'get')
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"token": mock_token}
    
    client = E2ETokenClient()
    response = client.get_e2e_token(TEST_APP_NAME)
    
    assert response["token"] == mock_token
    mock_get.assert_called_once_with(f"{E2E_TOKEN_URL}?targetApp={TEST_APP_NAME}")


def test_e2e_token_client_http_error(mocker, mock_dump_all):
    """Test that HTTP errors are properly raised"""
    failure_msg = "Simulated server error"
    
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = exceptions.HTTPError(failure_msg)
    
    mock_get = mocker.patch.object(Session, 'get')
    mock_get.return_value = mock_response
    
    client = E2ETokenClient()
    
    with pytest.raises(exceptions.HTTPError) as exc_info:
        client.get_e2e_token(TEST_APP_NAME)
    
    assert str(exc_info.value) == failure_msg
    mock_get.assert_called_once_with(f"{E2E_TOKEN_URL}?targetApp={TEST_APP_NAME}")

"""Tests for Hardware Manager Client"""
import pytest
from unittest.mock import Mock
from requests import Session, exceptions
from src.clients.hardware_manager_client import HardwareManagerClient


def test_init_with_net_key(net_key, mock_session_mount, mock_dump_all):
    """Test initialization with NET_KEY authentication"""
    client = HardwareManagerClient(net_key=net_key)
    
    assert client.auth_header == "Authorization"
    assert client.auth_value == f"Bearer {net_key}"
    assert client.url == "https://hardwaremanager.netflixpartners.com"
    assert client.port == 443


def test_init_with_netflix_access(mocker, mock_dump_all):
    """Test initialization with Netflix Access (Metatron)"""
    mock_e2e_client = mocker.patch('src.clients.hardware_manager_client.E2ETokenClient')
    mock_e2e_instance = Mock()
    mock_e2e_instance.get_e2e_token.return_value = {"token": "test_token"}
    mock_e2e_client.return_value = mock_e2e_instance
    
    client = HardwareManagerClient(use_netflix_access=True)
    
    assert client.auth_header == "X-Forwarded-Authentication"
    assert client.auth_value == "test_token"
    assert client.port == 7004


def test_init_without_auth_raises_exception():
    """Test that initialization without auth raises exception"""
    with pytest.raises(Exception, match="not authenticated"):
        HardwareManagerClient()


def test_get_devices_for_host_success(net_key, rae, mocker, mock_session_mount, mock_dump_all):
    """Test successful device list retrieval"""
    mock_post = mocker.patch.object(Session, 'post')
    mock_post.return_value.json.return_value = {
        "devices": [
            {"ip": "192.168.1.100", "name": "Device1"},
            {"ip": "192.168.1.101", "name": "Device2"}
        ]
    }
    
    client = HardwareManagerClient(net_key=net_key)
    result = client.get_devices_for_host(rae)
    
    assert "devices" in result
    assert len(result["devices"]) == 2
    
    # Verify correct endpoint was called
    call_url = mock_post.call_args[0][0]
    assert f"/api/host/{rae}/command/host.devices.list" in call_url


def test_set_device_ui_to_prod(net_key, rae, mocker, mock_session_mount, mock_dump_all):
    """Test setting device UI to prod environment"""
    mock_post = mocker.patch.object(Session, 'post')
    mock_post.return_value.json.return_value = {"deviceUI": "prod"}

    client = HardwareManagerClient(net_key=net_key)
    result = client.set_device_ui(rae, "192.168.1.100", "prod")

    assert result["deviceUI"] == "prod"

    # Verify endpoint and payload
    call_url = mock_post.call_args[0][0]
    assert f"/api/host/{rae}/command/device.deviceui" in call_url
    assert "ip=192.168.1.100" in call_url

    json_data = mock_post.call_args[1]["json"]
    assert json_data == {"ui": "prod"}


def test_set_device_ui_to_test(net_key, rae, mocker, mock_session_mount, mock_dump_all):
    """Test setting device UI to test environment"""
    mock_post = mocker.patch.object(Session, 'post')
    mock_post.return_value.json.return_value = {"deviceUI": "test"}

    client = HardwareManagerClient(net_key=net_key)
    result = client.set_device_ui(rae, "192.168.1.100", "test")

    assert result["deviceUI"] == "test"


def test_http_error_handling(net_key, rae, mocker, mock_session_mount, mock_dump_all):
    """Test that HTTP errors are properly raised"""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_http_error = exceptions.HTTPError("Server Error")
    mock_http_error.response = mock_response
    mock_response.raise_for_status.side_effect = mock_http_error
    
    mock_post = mocker.patch.object(Session, 'post')
    mock_post.return_value = mock_response

    client = HardwareManagerClient(net_key=net_key)

    with pytest.raises(Exception, match="Failed to call host command"):
        client.get_devices_for_host(rae)


def test_headers_include_client_appid(net_key, rae, mocker, mock_session_mount, mock_dump_all):
    """Test that headers include the client app ID"""
    mock_post = mocker.patch.object(Session, 'post')
    mock_post.return_value.json.return_value = {}

    client = HardwareManagerClient(net_key=net_key)
    client.get_devices_for_host(rae)

    headers = mock_post.call_args[1]["headers"]
    assert "x-netflix.client.appid" in headers
    assert headers["x-netflix.client.appid"] == "nts-cli"


def test_get_host_peripherals_success(net_key, rae, mocker, mock_session_mount, mock_dump_all):
    """Test successful host peripherals retrieval"""
    mock_post = mocker.patch.object(Session, 'post')
    mock_post.return_value.json.return_value = [
        {
            "type": "analyzer",
            "peripheral_id": "eleven-hdmi-0",
            "esn": "",
            "hw_config": {
                "type": "eleven",
                "location": "local",
                "input_channel": 0
            },
            "active": True,
            "name": "Eleven"
        },
        {
            "type": "eyepatch",
            "peripheral_id": "6137790",
            "esn": "NFANDROID2-PRV-TEST",
            "hw_config": {
                "type": "eyepatch",
                "serial": "6137790",
                "version": "1.09"
            },
            "active": True,
            "name": "Eyepatch"
        }
    ]

    client = HardwareManagerClient(net_key=net_key)
    result = client.get_host_peripherals(rae)

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["hw_config"]["type"] == "eleven"
    assert result[1]["hw_config"]["type"] == "eyepatch"
    
    # Verify correct endpoint was called
    call_url = mock_post.call_args[0][0]
    assert f"/api/host/{rae}/command/peripheral.list" in call_url


def test_get_host_peripherals_empty_list(net_key, rae, mocker, mock_session_mount, mock_dump_all):
    """Test peripherals retrieval with no peripherals"""
    mock_post = mocker.patch.object(Session, 'post')
    mock_post.return_value.json.return_value = []

    client = HardwareManagerClient(net_key=net_key)
    result = client.get_host_peripherals(rae)

    assert isinstance(result, list)
    assert len(result) == 0


def test_get_host_peripherals_error(net_key, rae, mocker, mock_session_mount, mock_dump_all):
    """Test that errors from peripheral.list are properly raised"""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_http_error = exceptions.HTTPError("Not Found")
    mock_http_error.response = mock_response
    mock_response.raise_for_status.side_effect = mock_http_error

    mock_post = mocker.patch.object(Session, 'post')
    mock_post.return_value = mock_response

    client = HardwareManagerClient(net_key=net_key)

    with pytest.raises(Exception, match="Failed to call host command"):
        client.get_host_peripherals(rae)

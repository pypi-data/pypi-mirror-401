"""Tests for Device Test Client"""
import pytest
from unittest.mock import Mock
from requests import Session, exceptions
from src.clients.device_test_client import DeviceTestClient, TestPlanFilters
from src.exceptions import (
    UnauthorizedException,
    ForbiddenException,
    UnclaimedDeviceException,
    DeviceAlreadyReservedException
)


# ============================================================================
# Initialization Tests
# ============================================================================

def test_init_with_net_key(net_key, mock_session_mount, mock_dump_all):
    """Test initialization with NET_KEY authentication"""
    client = DeviceTestClient(net_key=net_key)
    
    assert client.auth_header == "Authorization"
    assert client.auth_value == f"Bearer {net_key}"
    assert client.url == "https://third-party-gateway.dta.netflix.net"
    assert isinstance(client._exec_details_cache, dict)
    assert len(client._exec_details_cache) == 0


def test_init_with_netflix_access(mocker, mock_dump_all):
    """Test initialization with Netflix Access (Metatron)"""
    mock_e2e_client = mocker.patch('src.clients.device_test_client.E2ETokenClient')
    mock_e2e_instance = Mock()
    mock_e2e_instance.get_e2e_token.return_value = {"token": "test_token"}
    mock_e2e_client.return_value = mock_e2e_instance
    
    client = DeviceTestClient(use_netflix_access=True)
    
    assert client.auth_header == "X-Forwarded-Authentication"
    assert client.auth_value == "test_token"
    assert client.url == "https://third-party-gateway-mtls.dta.netflix.net"


def test_init_without_auth_raises_exception():
    """Test that initialization without auth raises exception"""
    with pytest.raises(Exception, match="not authenticated"):
        DeviceTestClient()


# ============================================================================
# Test Plan Retrieval Tests
# ============================================================================

def test_get_test_plan_success(net_key, esn, mocker, mock_session_mount, mock_dump_all):
    """Test successful test plan retrieval"""
    mock_get = mocker.patch.object(Session, 'get')
    mock_get.return_value.json.return_value = {
        "esn": esn,
        "test_case_guids": ["guid1", "guid2"]
    }

    client = DeviceTestClient(net_key=net_key)
    result = client.get_test_plan(esn)
    
    assert result["esn"] == esn
    assert len(result["test_case_guids"]) == 2
    mock_get.assert_called_once()


def test_get_test_plan_with_filters(net_key, esn, mocker, mock_session_mount, mock_dump_all):
    """Test test plan retrieval with all filters"""
    mock_get = mocker.patch.object(Session, 'get')
    mock_get.return_value.json.return_value = {"esn": esn}

    client = DeviceTestClient(net_key=net_key)
    filters = TestPlanFilters(
        automation="AUTOMATED",
        state="ENABLED",
        name="TEST*",
        tag="smoke",
        category="performance"
    )
    client.get_test_plan(esn, filters)

    # Verify URL contains query parameters
    url = mock_get.call_args[0][0]
    assert "testcaseAutomationFilter" in url
    assert "testcaseStateFilter" in url
    assert "testcaseNameFilter" in url
    assert "testcaseTagFilter" in url
    assert "testcaseCategoryFilter" in url


def test_get_test_plan_with_exclusion_filters(net_key, esn, mocker, mock_session_mount, mock_dump_all):
    """Test test plan retrieval with exclusion filters"""
    mock_get = mocker.patch.object(Session, 'get')
    mock_get.return_value.json.return_value = {"esn": esn}

    client = DeviceTestClient(net_key=net_key)
    filters = TestPlanFilters(
        name="SYNC*",
        name_exclude="FLAKY*",
        tag_exclude="wip",
        category_exclude="experimental"
    )
    client.get_test_plan(esn, filters)

    # Verify URL contains both inclusion and exclusion query parameters
    url = mock_get.call_args[0][0]
    assert "testcaseNameFilter" in url
    assert "testcaseNameExclude" in url
    assert "testcaseTagExclude" in url
    assert "testcaseCategoryExclude" in url


# ============================================================================
# Execution Details & Caching Tests
# ============================================================================

def test_get_test_execution_details_success(net_key, marker_set_id, mocker, mock_session_mount, mock_dump_all):
    """Test successful execution details retrieval"""
    mock_get = mocker.patch.object(Session, 'get')
    mock_get.return_value.json.return_value = {
        "data": {
            "attachments": [
                {"key": "test_ntscli.zip", "url": "https://s3.test.com/test.zip"}
            ]
        }
    }
    
    client = DeviceTestClient(net_key=net_key)
    result = client.get_test_execution_details(marker_set_id)
    
    assert "data" in result
    assert "attachments" in result["data"]
    mock_get.assert_called_once()


def test_get_test_execution_details_uses_cache(net_key, marker_set_id, mocker, mock_session_mount, mock_dump_all):
    """Test that execution details are cached and reused"""
    mock_get = mocker.patch.object(Session, 'get')
    mock_get.return_value.json.return_value = {"data": {"attachments": []}}
    
    client = DeviceTestClient(net_key=net_key)
    
    # First call - hits API
    result1 = client.get_test_execution_details(marker_set_id)
    assert mock_get.call_count == 1
    
    # Second call - uses cache
    result2 = client.get_test_execution_details(marker_set_id)
    assert mock_get.call_count == 1  # Still 1, not 2
    
    # Results are identical
    assert result1 == result2
    assert marker_set_id in client._exec_details_cache


# ============================================================================
# Device Status Tests
# ============================================================================

def test_get_status_by_esn(net_key, esn, mocker, mock_session_mount, mock_dump_all):
    """Test device status retrieval by ESN"""
    mock_get = mocker.patch.object(Session, 'get')
    mock_get.return_value.json.return_value = [
        {
            "esn": esn,
            "rae": "r3010203",
            "host": "test-host",
            "status": "idle"
        }
    ]
    
    client = DeviceTestClient(net_key=net_key)
    result = client.get_status(None, esn)
    
    assert len(result) == 1
    assert result[0]["esn"] == esn
    assert result[0]["status"] == "idle"
    assert result[0]["batchId"] is None


# ============================================================================
# Test Plan Cancellation Tests
# ============================================================================

def test_cancel_test_plan_run_success(net_key, batch_id, esn, mocker, mock_session_mount, mock_dump_all):
    """Test successful test plan cancellation"""
    mock_post = mocker.patch.object(Session, 'post')
    mock_post.return_value.json.return_value = {
        "batch_id": batch_id,
        "details": "Cancelled successfully"
    }
    
    client = DeviceTestClient(net_key=net_key)
    result = client.cancel_test_plan_run(batch_id, esn)
    
    assert result["batchId"] == batch_id
    assert "details" in result


# ============================================================================
# Exception Handling Tests
# ============================================================================

def test_401_raises_unauthorized_exception(net_key, esn, mocker, mock_session_mount, mock_dump_all):
    """Test that 401 status raises UnauthorizedException"""
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"
    mock_http_error = exceptions.HTTPError()
    mock_http_error.response = mock_response
    mock_response.raise_for_status.side_effect = mock_http_error
    
    mock_get = mocker.patch.object(Session, 'get')
    mock_get.return_value = mock_response
    
    client = DeviceTestClient(net_key=net_key)
    
    with pytest.raises(UnauthorizedException):
        client.get_test_plan(esn)


def test_403_raises_forbidden_exception(net_key, esn, mocker, mock_session_mount, mock_dump_all):
    """Test that 403 status raises ForbiddenException"""
    mock_response = Mock()
    mock_response.status_code = 403
    mock_response.text = "Forbidden"
    mock_http_error = exceptions.HTTPError()
    mock_http_error.response = mock_response
    mock_response.raise_for_status.side_effect = mock_http_error
    
    mock_get = mocker.patch.object(Session, 'get')
    mock_get.return_value = mock_response
    
    client = DeviceTestClient(net_key=net_key)
    
    with pytest.raises(ForbiddenException):
        client.get_test_plan(esn)


def test_unclaimed_device_raises_exception(net_key, esn, mocker, mock_session_mount, mock_dump_all):
    """Test that unclaimed device message raises UnclaimedDeviceException"""
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.text = "Device must be claimed"
    mock_http_error = exceptions.HTTPError()
    mock_http_error.response = mock_response
    mock_response.raise_for_status.side_effect = mock_http_error
    
    mock_post = mocker.patch.object(Session, 'post')
    mock_post.return_value = mock_response
    
    client = DeviceTestClient(net_key=net_key)
    plan = {"esn": esn, "test_case_guids": []}
    
    with pytest.raises(UnclaimedDeviceException):
        client.run_test_plan(plan, wait=False)


def test_reserved_device_raises_exception(net_key, esn, mocker, mock_session_mount, mock_dump_all):
    """Test that reserved device message raises DeviceAlreadyReservedException"""
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.text = "Device has already been reserved"
    mock_http_error = exceptions.HTTPError()
    mock_http_error.response = mock_response
    mock_response.raise_for_status.side_effect = mock_http_error
    
    mock_post = mocker.patch.object(Session, 'post')
    mock_post.return_value = mock_response
    
    client = DeviceTestClient(net_key=net_key)
    plan = {"esn": esn, "test_case_guids": []}
    
    with pytest.raises(DeviceAlreadyReservedException):
        client.run_test_plan(plan, wait=False)


# ============================================================================
# Device Registry Tests
# ============================================================================

def test_get_registry_device_details_success(net_key, esn, mocker, mock_session_mount, mock_dump_all):
    """Test successful device registry details retrieval"""
    mock_get = mocker.patch.object(Session, 'get')
    mock_get.return_value.json.return_value = {
        "esn": esn,
        "user": "testuser@netflix.com",
        "reservedAt": "2026-01-08T10:00:00Z",
        "status": "reserved"
    }

    client = DeviceTestClient(net_key=net_key)
    result = client.get_registry_device_details(esn)

    assert result["esn"] == esn
    assert result["user"] == "testuser@netflix.com"
    assert result["status"] == "reserved"
    mock_get.assert_called_once()


def test_release_device_reservation_success(net_key, esn, mocker, mock_session_mount, mock_dump_all):
    """Test successful device reservation release with empty response"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = ""  # Empty response body
    mock_response.raise_for_status = Mock()

    mock_delete = mocker.patch.object(Session, 'delete')
    mock_delete.return_value = mock_response

    client = DeviceTestClient(net_key=net_key)
    result = client.release_device_reservation(esn, "testuser@netflix.com")

    # Should return None (void)
    assert result is None
    mock_delete.assert_called_once()

    # Verify the URL includes both esn and user parameters (URL encoded)
    call_url = mock_delete.call_args[0][0]
    assert f"esn={esn}" in call_url
    assert "user=testuser%40netflix.com" in call_url  # @ is encoded as %40


def test_release_device_reservation_with_response_body(net_key, esn, mocker, mock_session_mount, mock_dump_all):
    """Test device reservation release when API returns a response body"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = '{"message": "Released"}'
    mock_response.raise_for_status = Mock()

    mock_delete = mocker.patch.object(Session, 'delete')
    mock_delete.return_value = mock_response

    client = DeviceTestClient(net_key=net_key)
    result = client.release_device_reservation(esn, "testuser@netflix.com")

    # Should still return None (void) regardless of response body
    assert result is None


def test_release_device_reservation_unauthorized(net_key, esn, mocker, mock_session_mount, mock_dump_all):
    """Test that 401 on release raises UnauthorizedException"""
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"
    mock_http_error = exceptions.HTTPError()
    mock_http_error.response = mock_response
    mock_response.raise_for_status.side_effect = mock_http_error

    mock_delete = mocker.patch.object(Session, 'delete')
    mock_delete.return_value = mock_response

    client = DeviceTestClient(net_key=net_key)

    with pytest.raises(UnauthorizedException):
        client.release_device_reservation(esn, "testuser@netflix.com")


def test_release_device_reservation_not_found(net_key, esn, mocker, mock_session_mount, mock_dump_all):
    """Test release when device reservation doesn't exist (404)"""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.text = "Reservation not found"
    mock_http_error = exceptions.HTTPError()
    mock_http_error.response = mock_response
    mock_response.raise_for_status.side_effect = mock_http_error

    mock_delete = mocker.patch.object(Session, 'delete')
    mock_delete.return_value = mock_response

    client = DeviceTestClient(net_key=net_key)

    with pytest.raises(Exception):
        client.release_device_reservation(esn, "testuser@netflix.com")


def test_release_device_reservation_special_characters(net_key, esn, mocker, mock_session_mount, mock_dump_all):
    """Test that user parameter with special characters is properly URL encoded"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = ""
    mock_response.raise_for_status = Mock()

    mock_delete = mocker.patch.object(Session, 'delete')
    mock_delete.return_value = mock_response

    client = DeviceTestClient(net_key=net_key)
    # User with spaces, @, and + symbols
    result = client.release_device_reservation(esn, "test user+alias@netflix.com")

    assert result is None
    mock_delete.assert_called_once()

    # Verify URL encoding: spaces -> %20, @ -> %40, + -> %2B
    call_url = mock_delete.call_args[0][0]
    assert "user=test+user%2Balias%40netflix.com" in call_url  # urlencode uses + for spaces


# ============================================================================
# Testcase Metadata Tests
# ============================================================================

def test_get_testcases_success(net_key, esn, mocker, mock_session_mount, mock_dump_all):
    """Test successful testcase metadata retrieval"""
    mock_post = mocker.patch.object(Session, 'post')
    mock_post.return_value.json.return_value = {
        "data": {
            "testcases": [
                {"name": "TEST1", "tags": ["smoke"], "category": "functional"}
            ]
        }
    }
    
    client = DeviceTestClient(net_key=net_key)
    result = client.get_testcases(esn, ["guid1"])
    
    assert len(result) == 1
    assert result[0]["name"] == "TEST1"


def test_get_testcases_empty_input_returns_empty_list(net_key, esn, mocker, mock_session_mount, mock_dump_all):
    """Test that empty input returns empty list without API call"""
    mock_post = mocker.patch.object(Session, 'post')
    
    client = DeviceTestClient(net_key=net_key)
    
    assert client.get_testcases("", []) == []
    assert client.get_testcases(esn, []) == []
    mock_post.assert_not_called()


# ============================================================================
# Extract CLI Results Tests (Attachment Handling)
# ============================================================================

def test_extract_cli_results_without_attachments(net_key, esn, mock_session_mount):
    """Test __extract_cli_results without include_attachments flag"""
    client = DeviceTestClient(net_key=net_key)
    client.get_testcases = Mock(return_value=[])
    
    results = [
        {
            "esn": esn,
            "testCase": "TEST1",
            "result": "passed",
            "result_message": "",
            "markerSetId": "marker1",
            "runtimeVersion": "1.0"
        }
    ]
    
    cli_results = client._DeviceTestClient__extract_cli_results(results, include_attachments=False)
    
    assert len(cli_results) == 1
    assert cli_results[0]["name"] == "TEST1"
    assert cli_results[0]["result"] == "passed"
    assert "attachmentsUrl" not in cli_results[0]


def test_extract_cli_results_with_attachments(net_key, esn, mocker, mock_session_mount):
    """Test __extract_cli_results with include_attachments=True"""
    client = DeviceTestClient(net_key=net_key)
    client.get_testcases = Mock(return_value=[])
    
    mock_get_exec_details = mocker.patch.object(client, 'get_test_execution_details')
    mock_get_exec_details.return_value = {
        "data": {
            "attachments": [
                {"key": "test_ntscli.zip", "url": "https://s3.test.com/file.zip"}
            ]
        }
    }
    
    results = [
        {
            "esn": esn,
            "testCase": "TEST1",
            "result": "passed",
            "result_message": "",
            "markerSetId": "marker1",
            "runtimeVersion": "1.0"
        }
    ]
    
    cli_results = client._DeviceTestClient__extract_cli_results(results, include_attachments=True)
    
    assert len(cli_results) == 1
    assert "attachmentsUrl" in cli_results[0]
    assert cli_results[0]["attachmentsUrl"] == "https://s3.test.com/file.zip"
    mock_get_exec_details.assert_called_once_with("marker1")


def test_extract_cli_results_filters_for_ntscli_zip(net_key, esn, mocker, mock_session_mount):
    """Test that only _ntscli.zip attachments are extracted"""
    client = DeviceTestClient(net_key=net_key)
    client.get_testcases = Mock(return_value=[])
    
    mock_get_exec_details = mocker.patch.object(client, 'get_test_execution_details')
    mock_get_exec_details.return_value = {
        "data": {
            "attachments": [
                {"key": "other_file.txt", "url": "https://s3.test.com/other.txt"},
                {"key": "logs_ntscli.zip", "url": "https://s3.test.com/logs.zip"},
                {"key": "another.pdf", "url": "https://s3.test.com/doc.pdf"}
            ]
        }
    }
    
    results = [
        {
            "esn": esn,
            "testCase": "TEST1",
            "result": "passed",
            "result_message": "",
            "markerSetId": "marker1",
            "runtimeVersion": "1.0"
        }
    ]
    
    cli_results = client._DeviceTestClient__extract_cli_results(results, include_attachments=True)
    
    # Should only get the _ntscli.zip URL
    assert cli_results[0]["attachmentsUrl"] == "https://s3.test.com/logs.zip"


def test_extract_cli_results_no_ntscli_zip_returns_none(net_key, esn, mocker, mock_session_mount):
    """Test that attachmentsUrl is None when no _ntscli.zip file exists"""
    client = DeviceTestClient(net_key=net_key)
    client.get_testcases = Mock(return_value=[])
    
    mock_get_exec_details = mocker.patch.object(client, 'get_test_execution_details')
    mock_get_exec_details.return_value = {
        "data": {
            "attachments": [
                {"key": "other_file.txt", "url": "https://s3.test.com/other.txt"}
            ]
        }
    }
    
    results = [
        {
            "esn": esn,
            "testCase": "TEST1",
            "result": "failed",
            "result_message": "Test failed",
            "markerSetId": "marker1",
            "runtimeVersion": "1.0"
        }
    ]
    
    cli_results = client._DeviceTestClient__extract_cli_results(results, include_attachments=True)
    
    assert cli_results[0]["attachmentsUrl"] is None
    assert cli_results[0]["failures"] == ["Test failed"]

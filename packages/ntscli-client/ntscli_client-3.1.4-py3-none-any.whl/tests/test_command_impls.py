"""Tests for command implementations"""
import pytest
import json
from io import StringIO
from unittest.mock import Mock
from src.clients.device_test_client import TestPlanFilters
from src.command_impls.get_plan_impl import get_plan_impl
from src.command_impls.run_impl import run_impl
from src.command_impls.status_impl import status_impl
from src.command_impls.cancel_impl import cancel_impl
from src.command_impls.get_run_plan_summary_impl import get_run_plan_summary_impl
from src.command_impls.release_device_impl import release_device_impl
from src.command_impls.run_eyepatch_calibration_impl import run_eyepatch_calibration_impl


# ============================================================================
# Get Plan Implementation Tests
# ============================================================================

def test_get_plan_full_type(esn, net_key, mocker):
    """Test get_plan_impl with FULL plan type"""
    mock_client = Mock()
    mock_client.get_test_plan.return_value = {
        "esn": esn,
        "test_case_guids": ["guid1", "guid2"]
    }
    
    mock_client_class = mocker.patch('src.command_impls.get_plan_impl.DeviceTestClient')
    mock_client_class.return_value = mock_client
    
    out_file = StringIO()
    filters = TestPlanFilters()
    get_plan_impl(
        esn=esn,
        plan_type="FULL",
        filters=filters,
        playlist_id=None,
        dynamic_filter_id=None,
        sdk_or_apk=None,
        out_file=out_file,
        net_key=net_key,
        use_netflix_access=False
    )
    
    result = json.loads(out_file.getvalue())
    assert result["esn"] == esn
    assert "test_overrides" in result
    mock_client.get_test_plan.assert_called_once_with(esn, filters)


def test_get_plan_playlist_type(esn, net_key, mocker):
    """Test get_plan_impl with PLAYLIST plan type"""
    mock_client = Mock()
    mock_client.get_playlist_test_plan.return_value = {
        "esn": esn,
        "playlist_id": "playlist-123"
    }
    
    mock_client_class = mocker.patch('src.command_impls.get_plan_impl.DeviceTestClient')
    mock_client_class.return_value = mock_client
    
    out_file = StringIO()
    filters = TestPlanFilters()
    get_plan_impl(
        esn=esn,
        plan_type="PLAYLIST",
        filters=filters,
        playlist_id="playlist-123",
        dynamic_filter_id=None,
        sdk_or_apk=None,
        out_file=out_file,
        net_key=net_key,
        use_netflix_access=False
    )
    
    result = json.loads(out_file.getvalue())
    assert result["esn"] == esn
    mock_client.get_playlist_test_plan.assert_called_once()


def test_get_plan_dynamic_filter_type(esn, net_key, mocker):
    """Test get_plan_impl with DYNAMIC_FILTER plan type"""
    mock_client = Mock()
    mock_client.get_dynamic_filter_test_plan.return_value = {
        "esn": esn,
        "filter_id": "filter-123"
    }
    
    mock_client_class = mocker.patch('src.command_impls.get_plan_impl.DeviceTestClient')
    mock_client_class.return_value = mock_client
    
    out_file = StringIO()
    filters = TestPlanFilters()
    get_plan_impl(
        esn=esn,
        plan_type="DYNAMIC_FILTER",
        filters=filters,
        playlist_id=None,
        dynamic_filter_id="filter-123",
        sdk_or_apk="SDK-1.0",
        out_file=out_file,
        net_key=net_key,
        use_netflix_access=False
    )
    
    result = json.loads(out_file.getvalue())
    assert result["esn"] == esn
    mock_client.get_dynamic_filter_test_plan.assert_called_once_with(
        "filter-123", esn, "SDK-1.0"
    )


def test_get_plan_full_type_with_filters(esn, net_key, mocker):
    """Test get_plan_impl with FULL plan type and filters"""
    mock_client = Mock()
    mock_client.get_test_plan.return_value = {
        "esn": esn,
        "test_case_guids": ["guid1"]
    }

    mock_client_class = mocker.patch('src.command_impls.get_plan_impl.DeviceTestClient')
    mock_client_class.return_value = mock_client

    out_file = StringIO()
    filters = TestPlanFilters(
        automation="AUTOMATED",
        state="ENABLED",
        name="SYNC*",
        name_exclude="FLAKY*",
        tag="smoke",
        tag_exclude="wip"
    )
    get_plan_impl(
        esn=esn,
        plan_type="FULL",
        filters=filters,
        playlist_id=None,
        dynamic_filter_id=None,
        sdk_or_apk=None,
        out_file=out_file,
        net_key=net_key,
        use_netflix_access=False
    )

    result = json.loads(out_file.getvalue())
    assert result["esn"] == esn
    assert "test_overrides" in result

    # Verify filters were passed correctly
    call_args = mock_client.get_test_plan.call_args
    assert call_args[0][0] == esn
    passed_filters = call_args[0][1]
    assert passed_filters.automation == "AUTOMATED"
    assert passed_filters.name == "SYNC*"
    assert passed_filters.name_exclude == "FLAKY*"


# ============================================================================
# Run Implementation Tests
# ============================================================================

def test_run_impl_without_wait(esn, batch_id, net_key, mocker):
    """Test run_impl without wait flag"""
    mock_client = Mock()
    mock_client.run_test_plan.return_value = {
        "batchId": batch_id,
        "executionFinished": False
    }
    
    mock_client_class = mocker.patch('src.command_impls.run_impl.DeviceTestClient')
    mock_client_class.return_value = mock_client
    
    plan = {"esn": esn, "test_case_guids": ["guid1"]}
    out_file = StringIO()
    
    run_impl(
        plan=plan,
        wait=False,
        out_file=out_file,
        net_key=net_key,
        use_netflix_access=False
    )
    
    result = json.loads(out_file.getvalue())
    assert result["batchId"] == batch_id
    mock_client.run_test_plan.assert_called_once_with(plan, False)


def test_run_impl_with_wait(esn, batch_id, net_key, mocker):
    """Test run_impl with wait flag"""
    mock_client = Mock()
    mock_client.run_test_plan.return_value = {
        "batchId": batch_id,
        "executionFinished": True,
        "passed": 5,
        "failed": 0
    }
    
    mock_client_class = mocker.patch('src.command_impls.run_impl.DeviceTestClient')
    mock_client_class.return_value = mock_client
    
    plan = {"esn": esn, "test_case_guids": ["guid1"]}
    out_file = StringIO()
    
    run_impl(
        plan=plan,
        wait=True,
        out_file=out_file,
        net_key=net_key,
        use_netflix_access=False
    )
    
    result = json.loads(out_file.getvalue())
    assert result["executionFinished"] is True
    mock_client.run_test_plan.assert_called_once_with(plan, True)


# ============================================================================
# Status Implementation Tests
# ============================================================================

def test_status_impl_with_esn(esn, net_key, mocker):
    """Test status_impl with ESN"""
    mock_client = Mock()
    mock_client.get_status.return_value = [
        {
            "esn": esn,
            "status": "idle",
            "batchId": None
        }
    ]
    
    mock_client_class = mocker.patch('src.command_impls.status_impl.DeviceTestClient')
    mock_client_class.return_value = mock_client
    
    out_file = StringIO()
    status_impl(
        rae=None,
        esn=esn,
        out_file=out_file,
        net_key=net_key,
        use_netflix_access=False
    )
    
    result = json.loads(out_file.getvalue())
    assert len(result) == 1
    assert result[0]["esn"] == esn


def test_status_impl_with_rae(rae, net_key, mocker):
    """Test status_impl with RAE"""
    mock_client = Mock()
    mock_client.get_status.return_value = [
        {"rae": rae, "status": "idle"}
    ]
    
    mock_client_class = mocker.patch('src.command_impls.status_impl.DeviceTestClient')
    mock_client_class.return_value = mock_client
    
    out_file = StringIO()
    status_impl(
        rae=rae,
        esn=None,
        out_file=out_file,
        net_key=net_key,
        use_netflix_access=False
    )
    
    result = json.loads(out_file.getvalue())
    assert len(result) == 1
    mock_client.get_status.assert_called_once_with(rae, None)


# ============================================================================
# Cancel Implementation Tests
# ============================================================================

def test_cancel_impl_success(esn, batch_id, net_key, mocker):
    """Test cancel_impl successfully cancels a batch"""
    mock_client = Mock()
    mock_client.cancel_test_plan_run.return_value = {
        "batchId": batch_id,
        "details": "Cancelled successfully"
    }
    
    mock_client_class = mocker.patch('src.command_impls.cancel_impl.DeviceTestClient')
    mock_client_class.return_value = mock_client
    
    out_file = StringIO()
    cancel_impl(
        batch_id=batch_id,
        esn=esn,
        out_file=out_file,
        net_key=net_key,
        use_netflix_access=False
    )
    
    result = json.loads(out_file.getvalue())
    assert result["batchId"] == batch_id
    assert "details" in result
    mock_client.cancel_test_plan_run.assert_called_once_with(batch_id, esn)


# ============================================================================
# Get Run Plan Summary Implementation Tests
# ============================================================================

def test_get_run_plan_summary_without_attachments(batch_id, net_key, mocker):
    """Test get_run_plan_summary_impl without attachments"""
    mock_client = Mock()
    mock_client.get_run_plan_summary.return_value = {
        "batchId": batch_id,
        "passed": 5,
        "failed": 0,
        "testResultDetails": []
    }
    
    mock_client_class = mocker.patch('src.command_impls.get_run_plan_summary_impl.DeviceTestClient')
    mock_client_class.return_value = mock_client
    
    out_file = StringIO()
    get_run_plan_summary_impl(
        batch_id=batch_id,
        out_file=out_file,
        net_key=net_key,
        use_netflix_access=False,
        include_attachments=False
    )
    
    result = json.loads(out_file.getvalue())
    assert result["batchId"] == batch_id
    mock_client.get_run_plan_summary.assert_called_once_with(
        batch_id, wait=False, include_attachments=False
    )


def test_get_run_plan_summary_with_attachments(batch_id, net_key, mocker):
    """Test get_run_plan_summary_impl with attachments enabled"""
    mock_client = Mock()
    mock_client.get_run_plan_summary.return_value = {
        "batchId": batch_id,
        "passed": 5,
        "failed": 0,
        "testResultDetails": [
            {
                "name": "TEST1",
                "result": "passed",
                "attachmentsUrl": "https://s3.test.com/file.zip"
            }
        ]
    }
    
    mock_client_class = mocker.patch('src.command_impls.get_run_plan_summary_impl.DeviceTestClient')
    mock_client_class.return_value = mock_client
    
    out_file = StringIO()
    get_run_plan_summary_impl(
        batch_id=batch_id,
        out_file=out_file,
        net_key=net_key,
        use_netflix_access=False,
        include_attachments=True
    )
    
    result = json.loads(out_file.getvalue())
    assert result["batchId"] == batch_id
    assert "attachmentsUrl" in result["testResultDetails"][0]
    mock_client.get_run_plan_summary.assert_called_once_with(
        batch_id, wait=False, include_attachments=True
    )


# ============================================================================
# Release Device Implementation Tests
# ============================================================================

def test_release_device_impl_with_reservation(esn, net_key, mocker):
    """Test release_device_impl when device has an active reservation"""
    mock_client = Mock()
    mock_client.get_registry_device_details.return_value = {
        "esn": esn,
        "user": "testuser@netflix.com",
        "status": "reserved"
    }
    mock_client.release_device_reservation.return_value = None

    mock_client_class = mocker.patch('src.command_impls.release_device_impl.DeviceTestClient')
    mock_client_class.return_value = mock_client

    out_file = StringIO()
    release_device_impl(
        esn=esn,
        out_file=out_file,
        net_key=net_key,
        use_netflix_access=False
    )

    result = json.loads(out_file.getvalue())
    assert result["message"] == "manually released device reservation"

    # Verify both methods were called
    mock_client.get_registry_device_details.assert_called_once_with(esn)
    mock_client.release_device_reservation.assert_called_once_with(esn, "testuser@netflix.com")


def test_release_device_impl_without_reservation(esn, net_key, mocker):
    """Test release_device_impl when device has no active reservation"""
    mock_client = Mock()
    mock_client.get_registry_device_details.return_value = {
        "esn": esn,
        "user": None,
        "status": "available"
    }

    mock_client_class = mocker.patch('src.command_impls.release_device_impl.DeviceTestClient')
    mock_client_class.return_value = mock_client

    out_file = StringIO()
    release_device_impl(
        esn=esn,
        out_file=out_file,
        net_key=net_key,
        use_netflix_access=False
    )

    result = json.loads(out_file.getvalue())
    assert result["message"] == "device is not reserved"

    # Verify only get_registry_device_details was called, not release
    mock_client.get_registry_device_details.assert_called_once_with(esn)
    mock_client.release_device_reservation.assert_not_called()


def test_release_device_impl_with_netflix_access(esn, mocker):
    """Test release_device_impl with Netflix Access authentication"""
    mock_client = Mock()
    mock_client.get_registry_device_details.return_value = {
        "esn": esn,
        "user": "employee@netflix.com",
        "status": "reserved"
    }
    mock_client.release_device_reservation.return_value = None

    mock_client_class = mocker.patch('src.command_impls.release_device_impl.DeviceTestClient')
    mock_client_class.return_value = mock_client

    out_file = StringIO()
    release_device_impl(
        esn=esn,
        out_file=out_file,
        net_key=None,
        use_netflix_access=True
    )

    result = json.loads(out_file.getvalue())
    assert result["message"] == "manually released device reservation"

    # Verify DeviceTestClient was initialized with correct auth
    mock_client_class.assert_called_once_with(None, True)


# ============================================================================
# Run Eyepatch Calibration Implementation Tests
# ============================================================================

def test_run_eyepatch_calibration_impl_with_old_eyepatch(esn, net_key, mocker, capsys):
    """Test run_eyepatch_calibration_impl detects old Eyepatch and shows warning"""
    # Mock DeviceTestClient
    mock_device_client = Mock()
    mock_device_client.get_registry_device_details.return_value = {
        "esn": esn,
        "hardware_serial": "RAE-12345"
    }
    mock_device_client.get_eyepatch_calibration_plan.return_value = {
        "test_case_guids": ["guid1"]
    }
    mock_device_client.run_test_plan.return_value = {
        "batchId": "batch-123",
        "status": "completed"
    }

    # Mock HardwareManagerClient
    mock_hwm_client = Mock()
    mock_hwm_client.get_host_peripherals.return_value = [
        {
            "type": "eyepatch",
            "peripheral_id": "6137790",
            "esn": esn,
            "hw_config": {
                "type": "eyepatch",
                "serial": "6137790",
                "version": "1.09"
            },
            "active": True,
            "name": "My Custom Eyepatch Name"  # Cosmetic name, should not be used for detection
        },
        {
            "type": "analyzer",
            "peripheral_id": "eleven-hdmi-0",
            "esn": "",
            "hw_config": {
                "type": "eleven",
                "location": "local"
            },
            "active": True,
            "name": "Eleven"
        }
    ]

    mock_device_client_class = mocker.patch('src.command_impls.run_eyepatch_calibration_impl.DeviceTestClient')
    mock_device_client_class.return_value = mock_device_client

    mock_hwm_client_class = mocker.patch('src.command_impls.run_eyepatch_calibration_impl.HardwareManagerClient')
    mock_hwm_client_class.return_value = mock_hwm_client

    out_file = StringIO()
    run_eyepatch_calibration_impl(
        esn=esn,
        audio_source="line-in",
        eyepatch_serial="EP-123",
        out_file=out_file,
        net_key=net_key,
        use_netflix_access=False
    )

    # Verify warning was printed to stderr
    captured = capsys.readouterr()
    assert "Warning" in captured.err

    # Verify the calibration still ran
    result = json.loads(out_file.getvalue())
    assert result["batchId"] == "batch-123"

    # Verify all expected methods were called
    mock_device_client.get_registry_device_details.assert_called_once_with(esn)
    mock_hwm_client.get_host_peripherals.assert_called_once_with("RAE-12345")
    mock_device_client.get_eyepatch_calibration_plan.assert_called_once_with(esn, "line-in", "EP-123")
    mock_device_client.run_test_plan.assert_called_once()


def test_run_eyepatch_calibration_impl_without_old_eyepatch(esn, net_key, mocker, capsys):
    """Test run_eyepatch_calibration_impl with only Eleven (no warning)"""
    # Mock DeviceTestClient
    mock_device_client = Mock()
    mock_device_client.get_registry_device_details.return_value = {
        "esn": esn,
        "hardware_serial": "RAE-67890"
    }
    mock_device_client.get_eyepatch_calibration_plan.return_value = {
        "test_case_guids": ["guid1"]
    }
    mock_device_client.run_test_plan.return_value = {
        "batchId": "batch-456",
        "status": "completed"
    }

    # Mock HardwareManagerClient - only Eleven peripherals
    mock_hwm_client = Mock()
    mock_hwm_client.get_host_peripherals.return_value = [
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
            "type": "analyzer",
            "peripheral_id": "eleven-hdmi-1",
            "esn": "",
            "hw_config": {
                "type": "eleven",
                "location": "local",
                "input_channel": 1
            },
            "active": True,
            "name": "Eleven"
        }
    ]

    mock_device_client_class = mocker.patch('src.command_impls.run_eyepatch_calibration_impl.DeviceTestClient')
    mock_device_client_class.return_value = mock_device_client

    mock_hwm_client_class = mocker.patch('src.command_impls.run_eyepatch_calibration_impl.HardwareManagerClient')
    mock_hwm_client_class.return_value = mock_hwm_client

    out_file = StringIO()
    run_eyepatch_calibration_impl(
        esn=esn,
        audio_source="arc",
        eyepatch_serial="EP-456",
        out_file=out_file,
        net_key=net_key,
        use_netflix_access=False
    )

    # Verify NO warning was printed
    captured = capsys.readouterr()
    assert "Warning" not in captured.err

    # Verify the calibration ran
    result = json.loads(out_file.getvalue())
    assert result["batchId"] == "batch-456"


def test_run_eyepatch_calibration_impl_case_insensitive_check(esn, net_key, mocker, capsys):
    """Test that Eyepatch detection is case-insensitive on hw_config.type"""
    # Mock DeviceTestClient
    mock_device_client = Mock()
    mock_device_client.get_registry_device_details.return_value = {
        "esn": esn,
        "hardware_serial": "RAE-99999"
    }
    mock_device_client.get_eyepatch_calibration_plan.return_value = {
        "test_case_guids": ["guid1"]
    }
    mock_device_client.run_test_plan.return_value = {
        "batchId": "batch-789",
        "status": "completed"
    }

    # Mock HardwareManagerClient - Eyepatch with different casing in hw_config.type
    mock_hwm_client = Mock()
    mock_hwm_client.get_host_peripherals.return_value = [
        {
            "type": "eyepatch",
            "peripheral_id": "6137791",
            "esn": esn,
            "hw_config": {
                "type": "EYEPATCH",  # All caps - should still be detected
                "serial": "6137791"
            },
            "active": True,
            "name": "Whatever Name"  # Name is ignored
        }
    ]

    mock_device_client_class = mocker.patch('src.command_impls.run_eyepatch_calibration_impl.DeviceTestClient')
    mock_device_client_class.return_value = mock_device_client

    mock_hwm_client_class = mocker.patch('src.command_impls.run_eyepatch_calibration_impl.HardwareManagerClient')
    mock_hwm_client_class.return_value = mock_hwm_client

    out_file = StringIO()
    run_eyepatch_calibration_impl(
        esn=esn,
        audio_source="line-in",
        eyepatch_serial="EP-789",
        out_file=out_file,
        net_key=net_key,
        use_netflix_access=False
    )

    # Verify warning was printed (case-insensitive match worked)
    captured = capsys.readouterr()
    assert "Warning" in captured.err


def test_run_eyepatch_calibration_impl_with_netflix_access(esn, mocker, capsys):
    """Test run_eyepatch_calibration_impl with Netflix Access authentication"""
    # Mock DeviceTestClient
    mock_device_client = Mock()
    mock_device_client.get_registry_device_details.return_value = {
        "esn": esn,
        "hardware_serial": "RAE-11111"
    }
    mock_device_client.get_eyepatch_calibration_plan.return_value = {
        "test_case_guids": ["guid1"]
    }
    mock_device_client.run_test_plan.return_value = {
        "batchId": "batch-111",
        "status": "completed"
    }

    # Mock HardwareManagerClient
    mock_hwm_client = Mock()
    mock_hwm_client.get_host_peripherals.return_value = []

    mock_device_client_class = mocker.patch('src.command_impls.run_eyepatch_calibration_impl.DeviceTestClient')
    mock_device_client_class.return_value = mock_device_client

    mock_hwm_client_class = mocker.patch('src.command_impls.run_eyepatch_calibration_impl.HardwareManagerClient')
    mock_hwm_client_class.return_value = mock_hwm_client

    out_file = StringIO()
    run_eyepatch_calibration_impl(
        esn=esn,
        audio_source="line-in",
        eyepatch_serial="EP-111",
        out_file=out_file,
        net_key=None,
        use_netflix_access=True
    )

    # Verify clients were initialized with correct auth
    mock_device_client_class.assert_called_once_with(None, True)
    mock_hwm_client_class.assert_called_once_with(None, True)

    # Verify calibration completed
    result = json.loads(out_file.getvalue())
    assert result["batchId"] == "batch-111"

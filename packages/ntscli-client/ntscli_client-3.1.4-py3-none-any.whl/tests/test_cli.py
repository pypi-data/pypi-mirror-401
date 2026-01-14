"""Tests for CLI commands"""
import pytest
import json
from io import StringIO
from unittest.mock import Mock, patch
from click.testing import CliRunner
from src.cli import default


# ============================================================================
# Get Plan CLI Tests
# ============================================================================

def test_get_plan_cli_full_type(esn, net_key, mocker):
    """Test get-plan CLI command with FULL plan type"""
    mock_impl = mocker.patch('src.cli.get_plan_impl')
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'get-plan',
        '--esn', esn,
        '--plan-type', 'FULL',
        '--net-key', net_key
    ])
    
    assert result.exit_code == 0
    mock_impl.assert_called_once()


def test_get_plan_cli_with_filters(esn, net_key, mocker):
    """Test get-plan CLI with inclusion filters"""
    mock_impl = mocker.patch('src.cli.get_plan_impl')
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'get-plan',
        '--esn', esn,
        '--plan-type', 'FULL',
        '--testcase-automation-filter', 'AUTOMATED',
        '--testcase-state-filter', 'ENABLED',
        '--testcase-name-filter', 'TEST*',
        '--testcase-tag-filter', 'smoke',
        '--testcase-category-filter', 'performance',
        '--net-key', net_key
    ])
    
    assert result.exit_code == 0
    mock_impl.assert_called_once()


def test_get_plan_cli_with_exclusion_filters(esn, net_key, mocker):
    """Test get-plan CLI with exclusion filters"""
    mock_impl = mocker.patch('src.cli.get_plan_impl')
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'get-plan',
        '--esn', esn,
        '--plan-type', 'FULL',
        '--testcase-name-exclude', 'FLAKY*',
        '--testcase-tag-exclude', 'wip',
        '--testcase-category-exclude', 'experimental',
        '--net-key', net_key
    ])
    
    assert result.exit_code == 0
    mock_impl.assert_called_once()


def test_get_plan_cli_playlist_type(esn, net_key, mocker):
    """Test get-plan CLI command with PLAYLIST plan type"""
    mock_impl = mocker.patch('src.cli.get_plan_impl')
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'get-plan',
        '--esn', esn,
        '--plan-type', 'PLAYLIST',
        '--playlist-id', 'playlist-123',
        '--net-key', net_key
    ])
    
    assert result.exit_code == 0
    mock_impl.assert_called_once()


def test_get_plan_cli_dynamic_filter_type(esn, net_key, mocker):
    """Test get-plan CLI command with DYNAMIC_FILTER plan type"""
    mock_impl = mocker.patch('src.cli.get_plan_impl')
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'get-plan',
        '--esn', esn,
        '--plan-type', 'DYNAMIC_FILTER',
        '--dynamic-filter-id', 'filter-123',
        '--sdk-or-apk', 'SDK-1.0',
        '--net-key', net_key
    ])
    
    assert result.exit_code == 0
    mock_impl.assert_called_once()


def test_get_plan_cli_missing_esn(net_key):
    """Test get-plan CLI fails when ESN is missing"""
    runner = CliRunner()
    result = runner.invoke(default, [
        'get-plan',
        '--plan-type', 'FULL',
        '--net-key', net_key
    ])
    
    assert result.exit_code != 0


def test_get_plan_cli_missing_plan_type(esn, net_key):
    """Test get-plan CLI fails when plan-type is missing"""
    runner = CliRunner()
    result = runner.invoke(default, [
        'get-plan',
        '--esn', esn,
        '--net-key', net_key
    ])
    
    assert result.exit_code != 0


# ============================================================================
# Run Plan CLI Tests
# ============================================================================

def test_run_plan_cli_without_wait(net_key, mocker, tmp_path):
    """Test run-plan CLI command without wait flag"""
    mock_impl = mocker.patch('src.cli.run_impl')
    
    # Create a test plan file
    plan_file = tmp_path / "plan.json"
    plan_file.write_text(json.dumps({
        "esn": "NFCDCH-02-1234567890",
        "test_case_guids": ["guid1", "guid2"]
    }))
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'run-plan',
        '--plan-file', str(plan_file),
        '--net-key', net_key
    ])
    
    assert result.exit_code == 0
    mock_impl.assert_called_once()


def test_run_plan_cli_with_wait(net_key, mocker, tmp_path):
    """Test run-plan CLI command with wait flag"""
    mock_impl = mocker.patch('src.cli.run_impl')
    
    plan_file = tmp_path / "plan.json"
    plan_file.write_text(json.dumps({
        "esn": "NFCDCH-02-1234567890",
        "test_case_guids": ["guid1"]
    }))
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'run-plan',
        '--plan-file', str(plan_file),
        '--wait',
        '--net-key', net_key
    ])
    
    assert result.exit_code == 0
    mock_impl.assert_called_once()


def test_run_plan_cli_with_overrides(net_key, mocker, tmp_path):
    """Test run-plan CLI command with overrides"""
    mock_impl = mocker.patch('src.cli.run_impl')
    
    plan_file = tmp_path / "plan.json"
    plan_file.write_text(json.dumps({
        "esn": "NFCDCH-02-1234567890",
        "test_case_guids": ["guid1"]
    }))
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'run-plan',
        '--plan-file', str(plan_file),
        '--override', 'key1=value1',
        '--override', 'key2=value2',
        '--net-key', net_key
    ])
    
    assert result.exit_code == 0
    mock_impl.assert_called_once()


def test_run_plan_cli_missing_plan_file(net_key):
    """Test run-plan CLI fails when plan-file is missing"""
    runner = CliRunner()
    result = runner.invoke(default, [
        'run-plan',
        '--net-key', net_key
    ])
    
    assert result.exit_code != 0


def test_run_plan_cli_invalid_json(net_key, tmp_path):
    """Test run-plan CLI fails with invalid JSON in plan file"""
    plan_file = tmp_path / "invalid.json"
    plan_file.write_text("not valid json")
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'run-plan',
        '--plan-file', str(plan_file),
        '--net-key', net_key
    ])
    
    assert result.exit_code != 0


def test_run_plan_cli_too_many_tests(net_key, tmp_path):
    """Test run-plan CLI fails when plan has more than 2000 test cases"""
    plan_file = tmp_path / "huge_plan.json"
    plan_file.write_text(json.dumps({
        "esn": "NFCDCH-02-1234567890",
        "test_case_guids": [f"guid{i}" for i in range(2001)]
    }))
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'run-plan',
        '--plan-file', str(plan_file),
        '--net-key', net_key
    ])
    
    assert result.exit_code != 0


# ============================================================================
# Get Device Status CLI Tests
# ============================================================================

def test_get_device_status_cli_with_esn(esn, net_key, mocker):
    """Test get-device-status CLI command with ESN"""
    mock_impl = mocker.patch('src.cli.status_impl')
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'get-device-status',
        '--esn', esn,
        '--net-key', net_key
    ])
    
    assert result.exit_code == 0
    mock_impl.assert_called_once()


def test_get_device_status_cli_with_rae(rae, net_key, mocker):
    """Test get-device-status CLI command with RAE"""
    mock_impl = mocker.patch('src.cli.status_impl')
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'get-device-status',
        '--rae', rae,
        '--net-key', net_key
    ])
    
    assert result.exit_code == 0
    mock_impl.assert_called_once()


def test_get_device_status_cli_with_both_esn_and_rae(esn, rae, net_key, mocker):
    """Test get-device-status CLI command with both ESN and RAE"""
    mock_impl = mocker.patch('src.cli.status_impl')
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'get-device-status',
        '--esn', esn,
        '--rae', rae,
        '--net-key', net_key
    ])
    
    assert result.exit_code == 0
    mock_impl.assert_called_once()


# ============================================================================
# Cancel Running Plan CLI Tests
# ============================================================================

def test_cancel_running_plan_cli(esn, batch_id, net_key, mocker):
    """Test cancel-running-plan CLI command"""
    mock_impl = mocker.patch('src.cli.cancel_impl')
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'cancel-running-plan',
        '--batch-id', batch_id,
        '--esn', esn,
        '--net-key', net_key
    ])
    
    assert result.exit_code == 0
    mock_impl.assert_called_once()


def test_cancel_running_plan_cli_missing_batch_id(esn, net_key):
    """Test cancel-running-plan CLI fails when batch-id is missing"""
    runner = CliRunner()
    result = runner.invoke(default, [
        'cancel-running-plan',
        '--esn', esn,
        '--net-key', net_key
    ])
    
    assert result.exit_code != 0


# ============================================================================
# Get Run Plan Summary CLI Tests
# ============================================================================

def test_get_run_plan_summary_cli(batch_id, net_key, mocker):
    """Test get-run-plan-summary CLI command"""
    mock_impl = mocker.patch('src.cli.get_run_plan_summary_impl')
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'get-run-plan-summary',
        '--batch-id', batch_id,
        '--net-key', net_key
    ])
    
    assert result.exit_code == 0
    mock_impl.assert_called_once()


def test_get_run_plan_summary_cli_with_attachments(batch_id, net_key, mocker):
    """Test get-run-plan-summary CLI with include-attachments flag"""
    mock_impl = mocker.patch('src.cli.get_run_plan_summary_impl')
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'get-run-plan-summary',
        '--batch-id', batch_id,
        '--include-attachments',
        '--net-key', net_key
    ])
    
    assert result.exit_code == 0
    mock_impl.assert_called_once()
    
    # Verify include_attachments was passed as True
    call_kwargs = mock_impl.call_args[1]
    assert call_kwargs['include_attachments'] is True


def test_get_run_plan_summary_cli_missing_batch_id(net_key):
    """Test get-run-plan-summary CLI fails when batch-id is missing"""
    runner = CliRunner()
    result = runner.invoke(default, [
        'get-run-plan-summary',
        '--net-key', net_key
    ])
    
    assert result.exit_code != 0


# ============================================================================
# Run Eyepatch Calibration Plan CLI Tests
# ============================================================================

def test_run_eyepatch_calibration_cli(esn, net_key, mocker):
    """Test run-eyepatch-calibration-plan CLI command"""
    mock_impl = mocker.patch('src.cli.run_eyepatch_calibration_impl')
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'run-eyepatch-calibration-plan',
        '--esn', esn,
        '--audio-source', 'line-in',
        '--eyepatch-serial', 'EP-123',
        '--net-key', net_key
    ])
    
    assert result.exit_code == 0
    mock_impl.assert_called_once()


def test_run_eyepatch_calibration_cli_deprecated_options(esn, net_key, mocker):
    """Test run-eyepatch-calibration-plan CLI with deprecated options shows warnings"""
    mock_impl = mocker.patch('src.cli.run_eyepatch_calibration_impl')
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'run-eyepatch-calibration-plan',
        '--esn', esn,
        '--audio-source', 'arc',
        '--form-factor', 'set-top-box',
        '--audio-mode', 'PASSTHROUGH',
        '--net-key', net_key
    ])
    
    assert result.exit_code == 0
    assert 'deprecated' in result.output.lower()


def test_run_eyepatch_calibration_cli_missing_audio_source(esn, net_key):
    """Test run-eyepatch-calibration-plan CLI fails when audio-source is missing"""
    runner = CliRunner()
    result = runner.invoke(default, [
        'run-eyepatch-calibration-plan',
        '--esn', esn,
        '--net-key', net_key
    ])
    
    assert result.exit_code != 0


# ============================================================================
# Run Eleven Calibration Plan CLI Tests
# ============================================================================

def test_run_eleven_calibration_cli(esn, net_key, mocker):
    """Test run-eleven-calibration-plan CLI command"""
    mock_impl = mocker.patch('src.cli.run_eleven_calibration_impl')
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'run-eleven-calibration-plan',
        '--esn', esn,
        '--net-key', net_key
    ])
    
    assert result.exit_code == 0
    mock_impl.assert_called_once()


def test_run_eleven_calibration_cli_missing_esn(net_key):
    """Test run-eleven-calibration-plan CLI fails when ESN is missing"""
    runner = CliRunner()
    result = runner.invoke(default, [
        'run-eleven-calibration-plan',
        '--net-key', net_key
    ])
    
    assert result.exit_code != 0


# ============================================================================
# Get Host Devices CLI Tests
# ============================================================================

def test_get_host_devices_cli(rae, net_key, mocker):
    """Test get-host-devices CLI command"""
    mock_client = Mock()
    mock_client.get_devices_for_host.return_value = [
        {"esn": "ESN1", "status": "idle"},
        {"esn": "ESN2", "status": "busy"}
    ]
    
    mock_client_class = mocker.patch('src.cli.HardwareManagerClient')
    mock_client_class.return_value = mock_client
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'get-host-devices',
        '--rae', rae,
        '--net-key', net_key
    ])
    
    assert result.exit_code == 0
    mock_client.get_devices_for_host.assert_called_once_with(rae)


def test_get_host_devices_cli_missing_rae(net_key):
    """Test get-host-devices CLI fails when RAE is missing"""
    runner = CliRunner()
    result = runner.invoke(default, [
        'get-host-devices',
        '--net-key', net_key
    ])
    
    assert result.exit_code != 0


# ============================================================================
# Set Device UI CLI Tests
# ============================================================================

def test_set_device_ui_cli(rae, net_key, mocker):
    """Test set-device-ui CLI command"""
    mock_client = Mock()
    mock_client.set_device_ui.return_value = {"deviceUI": "test"}
    
    mock_client_class = mocker.patch('src.cli.HardwareManagerClient')
    mock_client_class.return_value = mock_client
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'set-device-ui',
        '--rae', rae,
        '--ip', '192.168.1.100',
        '--env', 'test',
        '--net-key', net_key
    ])
    
    assert result.exit_code == 0
    mock_client.set_device_ui.assert_called_once_with(rae, '192.168.1.100', 'test')


def test_set_device_ui_cli_invalid_env(rae, net_key):
    """Test set-device-ui CLI fails with invalid env"""
    runner = CliRunner()
    result = runner.invoke(default, [
        'set-device-ui',
        '--rae', rae,
        '--ip', '192.168.1.100',
        '--env', 'INVALID',
        '--net-key', net_key
    ])
    
    assert result.exit_code != 0


def test_set_device_ui_cli_missing_rae(net_key):
    """Test set-device-ui CLI fails when RAE is missing"""
    runner = CliRunner()
    result = runner.invoke(default, [
        'set-device-ui',
        '--ip', '192.168.1.100',
        '--env', 'test',
        '--net-key', net_key
    ])
    
    assert result.exit_code != 0


# ============================================================================
# Get NTS CLI Dockerfile CLI Tests
# ============================================================================

def test_get_nts_cli_dockerfile(mocker, tmp_path):
    """Test get-nts-cli-dockerfile CLI command"""
    output_file = tmp_path / "Dockerfile"
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'get-nts-cli-dockerfile',
        '-o', str(output_file)
    ])
    
    assert result.exit_code == 0
    assert output_file.exists()
    
    # Verify Dockerfile contains expected content
    content = output_file.read_text()
    assert "FROM python:3.10-slim-bullseye" in content
    assert "pip3 install 'ntscli-client" in content


def test_get_nts_cli_dockerfile_stdout():
    """Test get-nts-cli-dockerfile CLI command runs successfully with default output"""
    # Note: CliRunner doesn't capture output written directly to file handles (sys.stdout)
    # Content validation is covered by test_get_nts_cli_dockerfile with explicit file output
    runner = CliRunner()
    result = runner.invoke(default, ['get-nts-cli-dockerfile'])
    
    assert result.exit_code == 0


# ============================================================================
# Release Device Reservation CLI Tests
# ============================================================================

def test_release_device_reservation_cli_with_net_key(esn, net_key, mocker):
    """Test release-device-reservation CLI command with NET_KEY"""
    mock_impl = mocker.patch('src.cli.release_device_impl')
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'release-device-reservation',
        '--esn', esn,
        '--net-key', net_key
    ])
    
    assert result.exit_code == 0
    mock_impl.assert_called_once()
    
    # Verify the impl was called with correct parameters
    call_kwargs = mock_impl.call_args[1]
    assert call_kwargs['esn'] == esn
    assert call_kwargs['net_key'] == net_key
    assert call_kwargs['use_netflix_access'] is False


def test_release_device_reservation_cli_with_netflix_access(esn, mocker):
    """Test release-device-reservation CLI command with Netflix Access"""
    mock_impl = mocker.patch('src.cli.release_device_impl')
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'release-device-reservation',
        '--esn', esn,
        '--use-netflix-access'
    ])
    
    assert result.exit_code == 0
    mock_impl.assert_called_once()
    
    # Verify the impl was called with correct parameters
    call_kwargs = mock_impl.call_args[1]
    assert call_kwargs['esn'] == esn
    assert call_kwargs['net_key'] is None
    assert call_kwargs['use_netflix_access'] is True


def test_release_device_reservation_cli_output_format(esn, net_key, mocker, tmp_path):
    """Test that CLI output is properly formatted JSON"""
    # Mock the implementation to write to out_file
    def mock_release_impl(esn, out_file, net_key, use_netflix_access):
        json.dump({"message": "manually released device reservation"}, out_file, indent=4)
    
    mocker.patch('src.cli.release_device_impl', side_effect=mock_release_impl)
    
    output_file = tmp_path / "output.json"
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'release-device-reservation',
        '--esn', esn,
        '--net-key', net_key,
        '-o', str(output_file)
    ])
    
    assert result.exit_code == 0
    assert output_file.exists()
    
    # Verify file contents
    with open(output_file) as f:
        output = json.load(f)
        assert output["message"] == "manually released device reservation"


def test_release_device_reservation_cli_missing_esn(net_key):
    """Test that CLI fails when ESN is missing"""
    runner = CliRunner()
    result = runner.invoke(default, [
        'release-device-reservation',
        '--net-key', net_key
    ])
    
    assert result.exit_code != 0
    assert "Missing option" in result.output or "required" in result.output.lower()


def test_release_device_reservation_cli_missing_auth():
    """Test that CLI fails when no authentication is provided"""
    runner = CliRunner()
    result = runner.invoke(default, [
        'release-device-reservation',
        '--esn', 'NFCDCH-02-1234567890'
    ])
    
    assert result.exit_code != 0
    assert "--net-key" in result.output or "--use-netflix-access" in result.output


def test_release_device_reservation_cli_with_output_file(esn, net_key, mocker, tmp_path):
    """Test release-device-reservation with output file option"""
    # Mock the implementation to write to out_file
    def mock_release_impl(esn, out_file, net_key, use_netflix_access):
        json.dump({"message": "device is not reserved"}, out_file, indent=4)
    
    mocker.patch('src.cli.release_device_impl', side_effect=mock_release_impl)
    
    output_file = tmp_path / "output.json"
    
    runner = CliRunner()
    result = runner.invoke(default, [
        'release-device-reservation',
        '--esn', esn,
        '--net-key', net_key,
        '-o', str(output_file)
    ])
    
    assert result.exit_code == 0
    assert output_file.exists()
    
    # Verify file contents
    with open(output_file) as f:
        output = json.load(f)
        assert output["message"] == "device is not reserved"


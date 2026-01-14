"""Tests for custom exceptions"""
import pytest
from src.exceptions import (
    MissingMetatronException,
    UnauthorizedException,
    ForbiddenException,
    UnclaimedDeviceException,
    DeviceAlreadyReservedException,
    DeviceIsUnavailableException
)


def test_missing_metatron_exception_default_message():
    """Test MissingMetatronException with default message"""
    exception = MissingMetatronException()
    assert "Missing Metatron module" in str(exception)
    assert "internal extras" in str(exception)


def test_missing_metatron_exception_custom_message():
    """Test MissingMetatronException with custom message"""
    custom_message = "Custom error message"
    exception = MissingMetatronException(custom_message)
    assert str(exception) == custom_message


def test_unauthorized_exception():
    """Test UnauthorizedException"""
    message = "Access denied"
    exception = UnauthorizedException(message)
    assert message in str(exception)
    assert "401" in str(exception)
    assert "Unauthorized" in str(exception)


def test_forbidden_exception():
    """Test ForbiddenException"""
    message = "Forbidden resource"
    exception = ForbiddenException(message)
    assert message in str(exception)
    assert "403" in str(exception)
    assert "Forbidden" in str(exception)


def test_unclaimed_device_exception():
    """Test UnclaimedDeviceException"""
    message = "Device not claimed"
    exception = UnclaimedDeviceException(message)
    assert message in str(exception)
    assert "Device must be claimed in HWM" in str(exception)


def test_device_already_reserved_exception():
    """Test DeviceAlreadyReservedException"""
    message = "Cannot reserve device"
    exception = DeviceAlreadyReservedException(message)
    assert message in str(exception)
    assert "already been reserved" in str(exception)


def test_device_is_unavailable_exception():
    """Test DeviceIsUnavailableException"""
    message = "Device is offline"
    exception = DeviceIsUnavailableException(message)
    assert message in str(exception)
    assert "Device is unavailable" in str(exception)


def test_all_exceptions_inherit_from_exception():
    """Test that all custom exceptions inherit from Exception"""
    assert issubclass(MissingMetatronException, Exception)
    assert issubclass(UnauthorizedException, Exception)
    assert issubclass(ForbiddenException, Exception)
    assert issubclass(UnclaimedDeviceException, Exception)
    assert issubclass(DeviceAlreadyReservedException, Exception)
    assert issubclass(DeviceIsUnavailableException, Exception)


def test_exception_can_be_caught_as_base_exception():
    """Test that custom exceptions can be caught as general Exception"""
    with pytest.raises(Exception) as exc_info:
        raise UnauthorizedException("Test error")
    
    assert isinstance(exc_info.value, UnauthorizedException)
    assert "Test error" in str(exc_info.value)

"""Pytest configuration and shared fixtures"""
import pytest
from unittest.mock import Mock


@pytest.fixture
def net_key():
    """Test NET_KEY for authentication"""
    return "test_net_key_12345"


@pytest.fixture
def esn():
    """Test ESN (Electronic Serial Number)"""
    return "TEST_ESN_12345"


@pytest.fixture
def rae():
    """Test RAE (Remote Access Equipment) identifier"""
    return "r3010203"


@pytest.fixture
def batch_id():
    """Test batch ID"""
    return "test-batch-uuid-12345"


@pytest.fixture
def marker_set_id():
    """Test marker set ID"""
    return "test-marker-set-uuid-12345"


@pytest.fixture
def mock_session_mount(mocker):
    """Mock Session.mount to avoid actual network setup"""
    return mocker.patch('requests.Session.mount')


@pytest.fixture
def mock_dump_all(mocker):
    """Mock requests_toolbelt.utils.dump.dump_all"""
    return mocker.patch('requests_toolbelt.utils.dump.dump_all')


__author__ = "tin.nguyen@paradox.ai"
__date__ = "24/06/2024 03:22"


from unittest.mock import AsyncMock, patch, MagicMock
import pytest


@pytest.fixture
def mock_aiohttp_get():
    with patch("aiohttp.ClientSession.get", new_callable=AsyncMock) as mock_get:
        yield mock_get


@pytest.fixture
def mock_request_get():
    with patch("requests.get") as mock_get:
        yield mock_get

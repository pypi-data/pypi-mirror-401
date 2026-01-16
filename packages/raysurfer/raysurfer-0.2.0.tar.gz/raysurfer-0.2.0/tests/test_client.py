"""Basic tests for RaySurfer client"""

import pytest

from raysurfer import RaySurfer, AsyncRaySurfer


def test_sync_client_init():
    client = RaySurfer(api_key="test-key", base_url="http://localhost:8000")
    assert client.api_key == "test-key"
    assert client.base_url == "http://localhost:8000"


def test_async_client_init():
    client = AsyncRaySurfer(api_key="test-key", base_url="http://localhost:8000")
    assert client.api_key == "test-key"
    assert client.base_url == "http://localhost:8000"


def test_context_manager():
    with RaySurfer(api_key="test") as client:
        assert client.api_key == "test"


@pytest.mark.asyncio
async def test_async_context_manager():
    async with AsyncRaySurfer(api_key="test") as client:
        assert client.api_key == "test"

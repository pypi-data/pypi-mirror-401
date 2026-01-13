"""
Integration tests for Pamela Python SDK.

Tests against staging API or mocked responses.
"""

import pytest
import os
from pamela import Pamela

TEST_API_URL = os.getenv("TEST_API_URL", "https://pamela-dev.up.railway.app")
TEST_API_KEY = os.getenv("TEST_API_KEY", "pk_test_placeholder")


@pytest.fixture
def sdk():
    """Create SDK instance for testing."""
    return Pamela(api_key=TEST_API_KEY, api_url=TEST_API_URL)


class TestInitialization:
    """Tests for SDK initialization."""

    def test_initialize_with_api_key(self, sdk):
        """Test SDK initializes with API key."""
        assert sdk is not None

    def test_initialize_without_api_key_raises(self):
        """Test SDK raises error without API key."""
        with pytest.raises(ValueError):
            Pamela(api_key="")


class TestCallCreation:
    """Tests for call creation."""

    @pytest.mark.asyncio
    async def test_create_call_with_required_params(self, sdk):
        """Test creates call with required parameters."""
        call = await sdk.calls.create(
            to="+1234567890",
            from_="+1987654321",
            country="US",
        )
        assert call is not None
        assert call.id is not None
        assert call.status is not None

    @pytest.mark.asyncio
    async def test_create_call_invalid_phone_number(self, sdk):
        """Test handles invalid phone numbers."""
        with pytest.raises(ValueError):
            await sdk.calls.create(
                to="invalid",
                from_="+1987654321",
                country="US",
            )


class TestCallStatus:
    """Tests for call status."""

    @pytest.mark.asyncio
    async def test_get_call_status(self, sdk):
        """Test gets call status by ID."""
        call_id = "test_call_id"
        status = await sdk.calls.get_status(call_id)
        assert status is not None
        assert status.id == call_id
        assert status.status is not None

    @pytest.mark.asyncio
    async def test_get_call_status_not_found(self, sdk):
        """Test handles non-existent call ID."""
        with pytest.raises(Exception):
            await sdk.calls.get_status("nonexistent")


class TestCallCancellation:
    """Tests for call cancellation."""

    @pytest.mark.asyncio
    async def test_cancel_call(self, sdk):
        """Test cancels in-progress call."""
        call_id = "test_call_id"
        result = await sdk.calls.cancel(call_id)
        assert result is not None
        assert result.success is True

    @pytest.mark.asyncio
    async def test_cancel_completed_call(self, sdk):
        """Test handles cancelling already completed call."""
        with pytest.raises(Exception):
            await sdk.calls.cancel("completed_call")


class TestUsage:
    """Tests for usage queries."""

    @pytest.mark.asyncio
    async def test_get_usage(self, sdk):
        """Test gets usage statistics."""
        usage = await sdk.usage.get("2024-01")
        assert usage is not None
        assert usage.call_count is not None
        assert usage.quota is not None

    @pytest.mark.asyncio
    async def test_get_usage_invalid_period(self, sdk):
        """Test handles invalid period format."""
        with pytest.raises(ValueError):
            await sdk.usage.get("invalid")


class TestErrorHandling:
    """Tests for error handling."""

    @pytest.mark.asyncio
    async def test_network_error(self):
        """Test handles network errors."""
        bad_sdk = Pamela(
            api_key=TEST_API_KEY,
            api_url="https://invalid-url.example.com",
        )
        with pytest.raises(Exception):
            await bad_sdk.calls.create(
                to="+1234567890",
                from_="+1987654321",
                country="US",
            )

    @pytest.mark.asyncio
    async def test_api_error_invalid_key(self):
        """Test handles API errors with invalid key."""
        bad_sdk = Pamela(
            api_key="invalid_key",
            api_url=TEST_API_URL,
        )
        with pytest.raises(Exception):
            await bad_sdk.calls.create(
                to="+1234567890",
                from_="+1987654321",
                country="US",
            )



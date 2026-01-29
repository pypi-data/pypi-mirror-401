"""
Tests for corrected streaming timeout fix in AsyncStream._iter_events()

These tests verify that AsyncStream properly times out when the server
stops sending data, while preserving decoder state for multi-chunk events.
"""
# pyright: reportUnknownVariableType=false, reportUnknownMemberType=false, reportUnknownArgumentType=false
import asyncio
from typing import Any, AsyncIterator
from unittest.mock import Mock, PropertyMock

import httpx
import pytest

from sgp_agents._constants import DEFAULT_TIMEOUT
from sgp_agents._streaming import SSEDecoder, AsyncStream


def create_mock_client() -> Mock:
    """Create a mock client with a real SSEDecoder."""
    mock_client = Mock()
    mock_client._make_sse_decoder.return_value = SSEDecoder()
    return mock_client


class TestStreamingTimeoutCorrected:
    """Test suite for corrected streaming timeout behavior."""

    @pytest.mark.asyncio
    async def test_timeout_extraction_from_httpx_timeout_dict(self) -> None:
        """Verify timeout is correctly extracted from httpx timeout dict."""
        mock_response = Mock()

        async def normal_chunks() -> AsyncIterator[bytes]:
            for i in range(3):
                await asyncio.sleep(0.01)
                yield f"data: chunk{i}\n\n".encode()

        mock_response.aiter_bytes = normal_chunks

        # Mock request with timeout dict (how httpx actually stores it)
        mock_request = Mock()
        timeout_dict = {'connect': 5.0, 'read': 2.0, 'write': 5.0, 'pool': 5.0}
        mock_request.extensions = {"timeout": timeout_dict}
        type(mock_response)._request = PropertyMock(return_value=mock_request)

        mock_client = create_mock_client()
        stream = AsyncStream(
            cast_to=dict,
            response=mock_response,
            client=mock_client,
        )

        # Should extract read timeout correctly without crashing
        events = []
        async for event in stream._iter_events():
            events.append(event)

        assert len(events) == 3

    @pytest.mark.asyncio
    async def test_timeout_none_means_no_timeout(self) -> None:
        """Verify that timeout dict with read=None means no timeout applied."""
        mock_response = Mock()

        async def slow_chunks() -> AsyncIterator[bytes]:
            """Chunks arrive slowly but should complete without timeout."""
            for i in range(2):
                await asyncio.sleep(0.5)  # Would timeout if 0.3s timeout applied
                yield f"data: chunk{i}\n\n".encode()

        mock_response.aiter_bytes = slow_chunks

        # Timeout dict with read=None means no read timeout
        mock_request = Mock()
        timeout_dict = {'connect': 5.0, 'read': None, 'write': 5.0, 'pool': 5.0}
        mock_request.extensions = {"timeout": timeout_dict}
        type(mock_response)._request = PropertyMock(return_value=mock_request)

        mock_client = create_mock_client()
        stream = AsyncStream(
            cast_to=dict,
            response=mock_response,
            client=mock_client,
        )

        # Should complete without timing out
        events = []
        async for event in stream._iter_events():
            events.append(event)

        assert len(events) == 2

    @pytest.mark.asyncio
    async def test_decoder_state_preserved_across_chunks(self) -> None:
        """Verify decoder buffer is maintained when events span multiple chunks."""
        mock_response = Mock()

        async def split_event_chunks() -> AsyncIterator[bytes]:
            """Simulate SSE event split across multiple chunks."""
            # First chunk: incomplete event (no \n\n terminator)
            yield b'data: {"key":'
            await asyncio.sleep(0.01)
            # Second chunk: completes the event
            yield b'"value"}\n\n'

        mock_response.aiter_bytes = split_event_chunks

        # No timeout configured
        type(mock_response)._request = PropertyMock(return_value=None)

        mock_client = create_mock_client()
        stream = AsyncStream(
            cast_to=dict,
            response=mock_response,
            client=mock_client,
        )

        # Should receive ONE complete event (decoder buffered across chunks)
        events = []
        async for event in stream._iter_events():
            events.append(event)

        assert len(events) == 1
        assert events[0].data == '{"key":"value"}'

    @pytest.mark.asyncio
    async def test_multi_byte_utf8_across_chunks(self) -> None:
        """Verify multi-byte UTF-8 characters split across chunks work correctly."""
        mock_response = Mock()

        async def split_utf8_chunks() -> AsyncIterator[bytes]:
            """Split a multi-byte UTF-8 character across chunks."""
            # Unicode character '你' (U+4F60) in UTF-8: 0xE4 0xBD 0xA0
            # Split it across chunks
            yield b'data: hello '
            yield b'\xe4'  # First byte of 你
            yield b'\xbd\xa0'  # Remaining bytes of 你
            yield b'\n\n'

        mock_response.aiter_bytes = split_utf8_chunks
        type(mock_response)._request = PropertyMock(return_value=None)

        mock_client = create_mock_client()
        stream = AsyncStream(
            cast_to=dict,
            response=mock_response,
            client=mock_client,
        )

        events = []
        async for event in stream._iter_events():
            events.append(event)

        assert len(events) == 1
        assert events[0].data == 'hello 你'

    @pytest.mark.asyncio
    async def test_timeout_raises_when_server_hangs(self) -> None:
        """Verify timeout occurs when server stops sending."""
        mock_response = Mock()

        async def hung_after_one() -> AsyncIterator[bytes]:
            yield b"data: chunk0\n\n"
            await asyncio.sleep(1000)  # Hang

        mock_response.aiter_bytes = hung_after_one

        # Short timeout dict
        mock_request = Mock()
        timeout_dict = {'connect': 5.0, 'read': 0.5, 'write': 5.0, 'pool': 5.0}
        mock_request.extensions = {"timeout": timeout_dict}
        type(mock_response)._request = PropertyMock(return_value=mock_request)

        mock_client = create_mock_client()
        stream = AsyncStream(
            cast_to=dict,
            response=mock_response,
            client=mock_client,
        )

        events = []
        with pytest.raises(httpx.ReadTimeout) as exc_info:
            async for event in stream._iter_events():
                events.append(event)

        assert len(events) == 1
        # Updated: Now catches timeout in decoder layer, not just byte layer
        error_msg = str(exc_info.value)
        assert ("Stream read timeout after 0.5s" in error_msg or
                "SSE decoder timeout after 0.5s" in error_msg)

    @pytest.mark.asyncio
    async def test_cleanup_on_timeout(self) -> None:
        """Verify cleanup happens on timeout."""
        mock_response = Mock()
        cleanup_tracker = {'aclose_called': False}

        class TrackedIterator:
            async def __anext__(self) -> bytes:
                await asyncio.sleep(1000)
                return b"never"

            async def aclose(self) -> None:
                cleanup_tracker['aclose_called'] = True

        mock_response.aiter_bytes = lambda: TrackedIterator()

        mock_request = Mock()
        timeout_dict = {'connect': 5.0, 'read': 0.3, 'write': 5.0, 'pool': 5.0}
        mock_request.extensions = {"timeout": timeout_dict}
        type(mock_response)._request = PropertyMock(return_value=mock_request)

        mock_client = create_mock_client()
        stream = AsyncStream(
            cast_to=dict,
            response=mock_response,
            client=mock_client,
        )

        with pytest.raises(httpx.ReadTimeout):
            async for _ in stream._iter_events():
                pass

        assert cleanup_tracker['aclose_called'], "Should call aclose on timeout"

    @pytest.mark.asyncio
    async def test_event_loop_responsive_during_wait(self) -> None:
        """Verify event loop can run other tasks while waiting."""
        mock_response = Mock()

        async def slow_chunks() -> AsyncIterator[bytes]:
            for i in range(3):
                await asyncio.sleep(0.3)
                yield f"data: chunk{i}\n\n".encode()

        mock_response.aiter_bytes = slow_chunks

        mock_request = Mock()
        timeout_dict = {'connect': 5.0, 'read': 2.0, 'write': 5.0, 'pool': 5.0}
        mock_request.extensions = {"timeout": timeout_dict}
        type(mock_response)._request = PropertyMock(return_value=mock_request)

        mock_client = create_mock_client()
        stream = AsyncStream(
            cast_to=dict,
            response=mock_response,
            client=mock_client,
        )

        # Track watchdog runs
        watchdog_ticks = []

        async def watchdog() -> None:
            for i in range(10):
                await asyncio.sleep(0.1)
                watchdog_ticks.append(i)

        async def consume() -> list[Any]:  # type: ignore[reportUnknownParameterType]
            events: list[Any] = []
            async for event in stream._iter_events():
                events.append(event)
            return events

        # Run both concurrently
        stream_task = asyncio.create_task(consume())
        watchdog_task = asyncio.create_task(watchdog())

        events = await stream_task
        watchdog_task.cancel()

        assert len(events) == 3
        assert len(watchdog_ticks) > 0, "Watchdog should run (event loop responsive)"

    @pytest.mark.asyncio
    async def test_no_timeout_when_extensions_missing(self) -> None:
        """Verify no timeout applied when request has no extensions."""
        mock_response = Mock()

        async def chunks() -> AsyncIterator[bytes]:
            for i in range(2):
                await asyncio.sleep(0.5)
                yield f"data: chunk{i}\n\n".encode()

        mock_response.aiter_bytes = chunks

        # No request or extensions
        type(mock_response)._request = PropertyMock(return_value=None)

        mock_client = create_mock_client()
        stream = AsyncStream(
            cast_to=dict,
            response=mock_response,
            client=mock_client,
        )

        # Should complete without timeout (no timeout configured)
        events = []
        async for event in stream._iter_events():
            events.append(event)

        assert len(events) == 2

    def test_default_timeout_is_120_seconds(self) -> None:
        """Verify that the default timeout is set to 120 seconds (2 minutes)."""
        # This test ensures that the timeout change for agent operations is preserved
        assert DEFAULT_TIMEOUT.connect == 5.0, "Connect timeout should remain 5.0s"
        assert DEFAULT_TIMEOUT.read == 120.0, "Read timeout should be 120.0s (2 minutes)"
        assert DEFAULT_TIMEOUT.write == 120.0, "Write timeout should be 120.0s (2 minutes)"
        assert DEFAULT_TIMEOUT.pool == 120.0, "Pool timeout should be 120.0s (2 minutes)"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

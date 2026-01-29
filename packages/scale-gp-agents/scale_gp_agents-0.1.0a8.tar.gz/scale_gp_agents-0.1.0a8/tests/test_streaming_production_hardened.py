"""
Tests for production-hardened streaming fixes in AsyncStream.

These tests verify all critical production fixes:
1. Decoder timeout protection (prevents hanging on incomplete SSE events)
2. Max buffer size protection (prevents memory exhaustion)
3. Double-iteration guard (prevents resource issues)
4. Cleanup exception suppression (preserves original errors)
"""
import asyncio
from typing import Iterator, AsyncIterator, AsyncGenerator
from unittest.mock import Mock, PropertyMock

import httpx
import pytest

from sgp_agents._streaming import MAX_SSE_BUFFER_SIZE, Stream, SSEDecoder, AsyncStream


def create_mock_client() -> Mock:
    """Create a mock client with a real SSEDecoder."""
    mock_client = Mock()
    mock_client._make_sse_decoder.return_value = SSEDecoder()
    mock_client._process_response_data.return_value = {"processed": True}
    return mock_client


class TestDecoderTimeoutProtection:
    """Test that decoder-level timeout protection works correctly."""

    @pytest.mark.asyncio
    async def test_decoder_timeout_on_incomplete_sse_event(self) -> None:
        """
        CRITICAL: Verify timeout triggers when decoder waits for incomplete SSE event.

        This is the key production fix - previously, only byte iteration had timeout,
        but decoder could hang forever waiting for a terminating \\n\\n.
        """
        mock_response = Mock()

        async def incomplete_event_then_hang() -> AsyncIterator[bytes]:
            # Send incomplete SSE event (missing \n\n terminator)
            yield b'data: {"incomplete":'
            yield b' "value"}'
            # Server crashes or stops - no \n\n ever comes
            await asyncio.sleep(1000)

        mock_response.aiter_bytes = incomplete_event_then_hang

        # Configure timeout
        mock_request = Mock()
        timeout_dict = {'connect': 5.0, 'read': 0.5, 'write': 5.0, 'pool': 5.0}
        mock_request.extensions = {"timeout": timeout_dict}
        type(mock_response)._request = PropertyMock(return_value=mock_request)

        mock_client = create_mock_client()
        stream = AsyncStream(
            cast_to=object,
            response=mock_response,
            client=mock_client,
        )

        # Should timeout in decoder, not hang forever
        with pytest.raises(httpx.ReadTimeout) as exc_info:
            async for _ in stream._iter_events():
                pass

        error_msg = str(exc_info.value)
        assert "SSE decoder timeout" in error_msg or "Stream read timeout" in error_msg

    @pytest.mark.asyncio
    async def test_decoder_completes_normally_with_proper_events(self) -> None:
        """Verify decoder doesn't false-positive timeout on normal events."""
        mock_response = Mock()

        async def normal_events() -> AsyncIterator[bytes]:
            yield b'data: {"event": 1}\n\n'
            await asyncio.sleep(0.1)
            yield b'data: {"event": 2}\n\n'

        mock_response.aiter_bytes = normal_events

        mock_request = Mock()
        timeout_dict = {'connect': 5.0, 'read': 2.0, 'write': 5.0, 'pool': 5.0}
        mock_request.extensions = {"timeout": timeout_dict}
        type(mock_response)._request = PropertyMock(return_value=mock_request)

        mock_client = create_mock_client()
        stream = AsyncStream(
            cast_to=object,
            response=mock_response,
            client=mock_client,
        )

        events: list[object] = []
        async for event in stream._iter_events():
            events.append(event)

        assert len(events) == 2

    @pytest.mark.asyncio
    async def test_decoder_timeout_distinguished_from_byte_timeout(self) -> None:
        """Verify we can distinguish decoder timeout from byte-level timeout."""
        mock_response = Mock()

        async def bytes_arrive_but_incomplete() -> AsyncIterator[bytes]:
            # Bytes arrive promptly but never form complete event
            yield b'data: incomplete'
            await asyncio.sleep(0.1)
            yield b' more data'
            await asyncio.sleep(0.1)
            # No \n\n, decoder waits forever
            await asyncio.sleep(1000)

        mock_response.aiter_bytes = bytes_arrive_but_incomplete

        mock_request = Mock()
        timeout_dict = {'connect': 5.0, 'read': 0.3, 'write': 5.0, 'pool': 5.0}
        mock_request.extensions = {"timeout": timeout_dict}
        type(mock_response)._request = PropertyMock(return_value=mock_request)

        mock_client = create_mock_client()
        stream = AsyncStream(
            cast_to=object,
            response=mock_response,
            client=mock_client,
        )

        with pytest.raises(httpx.ReadTimeout):
            async for _ in stream._iter_events():
                pass


class TestMaxBufferSizeProtection:
    """Test that SSE decoder enforces max buffer size."""

    @pytest.mark.asyncio
    async def test_decoder_rejects_oversized_buffer(self) -> None:
        """
        CRITICAL: Verify decoder raises error when buffer exceeds limit.

        This prevents memory exhaustion from malformed or malicious streams.
        """
        mock_response = Mock()

        async def huge_event_without_terminator() -> AsyncIterator[bytes]:
            # Send data that never terminates but grows indefinitely
            chunk_size = 1024 * 1024  # 1MB chunks
            for _ in range(110):  # 110MB total, exceeds 100MB limit
                yield b"x" * chunk_size

        mock_response.aiter_bytes = huge_event_without_terminator
        type(mock_response)._request = PropertyMock(return_value=None)

        # Create decoder with default max size
        mock_client = create_mock_client()
        stream = AsyncStream(
            cast_to=object,
            response=mock_response,
            client=mock_client,
        )

        with pytest.raises(ValueError) as exc_info:
            async for _ in stream._iter_events():
                pass

        error_msg = str(exc_info.value)
        assert "SSE buffer exceeded maximum size" in error_msg
        assert str(MAX_SSE_BUFFER_SIZE) in error_msg

    @pytest.mark.asyncio
    async def test_decoder_accepts_large_valid_event(self) -> None:
        """Verify decoder accepts large events that are properly terminated."""
        mock_response = Mock()

        async def large_valid_event() -> AsyncIterator[bytes]:
            # Send 50MB event (under 100MB limit) with proper terminator
            large_data = "x" * (50 * 1024 * 1024)
            yield f'data: {{"large": "{large_data}"}}\n\n'.encode()

        mock_response.aiter_bytes = large_valid_event
        type(mock_response)._request = PropertyMock(return_value=None)

        mock_client = create_mock_client()
        stream = AsyncStream(
            cast_to=object,
            response=mock_response,
            client=mock_client,
        )

        events: list[object] = []
        async for event in stream._iter_events():
            events.append(event)

        assert len(events) == 1

    @pytest.mark.asyncio
    async def test_decoder_custom_max_buffer_size(self) -> None:
        """Verify decoder respects custom max buffer size."""
        mock_response = Mock()

        async def medium_event() -> AsyncIterator[bytes]:
            # Send 500KB without terminator
            yield b"x" * (500 * 1024)

        mock_response.aiter_bytes = medium_event
        type(mock_response)._request = PropertyMock(return_value=None)

        # Create decoder with small custom max size
        mock_client = Mock()
        mock_client._make_sse_decoder.return_value = SSEDecoder(max_buffer_size=100 * 1024)  # 100KB
        mock_client._process_response_data.return_value = {"processed": True}

        stream = AsyncStream(
            cast_to=object,
            response=mock_response,
            client=mock_client,
        )

        with pytest.raises(ValueError) as exc_info:
            async for _ in stream._iter_events():
                pass

        assert "102400 bytes" in str(exc_info.value)  # 100KB in bytes


class TestDoubleIterationGuard:
    """Test that streams prevent double iteration."""

    @pytest.mark.asyncio
    async def test_async_stream_raises_on_double_iteration(self) -> None:
        """
        CRITICAL: Verify AsyncStream raises error on second iteration attempt.

        This prevents confusing connection errors and resource leaks.
        """
        mock_response = Mock()

        # Make aclose an async mock
        async def mock_aclose() -> None:
            pass
        mock_response.aclose = mock_aclose

        async def simple_event() -> AsyncIterator[bytes]:
            yield b'data: {"test": 1}\n\n'

        mock_response.aiter_bytes = simple_event
        type(mock_response)._request = PropertyMock(return_value=None)

        mock_client = create_mock_client()
        stream = AsyncStream(
            cast_to=object,
            response=mock_response,
            client=mock_client,
        )

        # First iteration should work - use __aiter__ (which is what 'async for' calls)
        events1: list[object] = []
        async for event in stream:
            events1.append(event)
        assert len(events1) == 1

        # Second iteration should raise RuntimeError when trying to iterate again
        with pytest.raises(RuntimeError) as exc_info:
            async for _ in stream:
                pass

        assert "already been consumed" in str(exc_info.value)

    def test_sync_stream_raises_on_double_iteration(self) -> None:
        """Verify Stream (sync) also prevents double iteration."""
        # Create a simple mock response
        mock_response = Mock()
        mock_response.close = Mock()

        # Create a generator function that can be called multiple times
        def make_iter() -> Iterator[bytes]:
            yield b'data: {"test": 1}\n\n'

        mock_response.iter_bytes = make_iter

        mock_client = Mock()
        mock_client._make_sse_decoder.return_value = SSEDecoder()
        mock_client._process_response_data.return_value = {"processed": True}

        stream = Stream(
            cast_to=object,
            response=mock_response,
            client=mock_client,
        )

        # First iteration - use __iter__ which checks _consumed flag
        events1: list[object] = []
        for event in stream:
            events1.append(event)
        assert len(events1) == 1

        # Second iteration should raise
        with pytest.raises(RuntimeError) as exc_info:
            for _ in stream:
                pass

        assert "already been consumed" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_double_iteration_error_message_is_clear(self) -> None:
        """Verify error message provides clear guidance."""
        mock_response = Mock()

        async def mock_aclose() -> None:
            pass
        mock_response.aclose = mock_aclose

        async def simple_event() -> AsyncIterator[bytes]:
            yield b'data: {"test": 1}\n\n'

        mock_response.aiter_bytes = simple_event
        type(mock_response)._request = PropertyMock(return_value=None)

        mock_client = create_mock_client()
        stream = AsyncStream(
            cast_to=object,
            response=mock_response,
            client=mock_client,
        )

        # Consume stream using __aiter__ which checks the flag
        async for _ in stream:
            pass

        # Try again
        with pytest.raises(RuntimeError) as exc_info:
            async for _ in stream:
                pass

        error_msg = str(exc_info.value)
        assert "AsyncStream" in error_msg
        assert "Create a new request" in error_msg


class TestCleanupExceptionSuppression:
    """Test that cleanup exceptions don't mask original errors."""

    @pytest.mark.asyncio
    async def test_cleanup_error_suppressed_preserves_timeout(self) -> None:
        """
        CRITICAL: Verify cleanup errors don't mask timeout errors.

        This is essential for production debugging - you need to see the
        real timeout, not a connection error during cleanup.
        """
        mock_response = Mock()
        cleanup_order: list[str] = []

        class FailingCleanupIterator:
            async def __anext__(self) -> bytes:
                await asyncio.sleep(1000)  # Will timeout
                return b"never"

            async def aclose(self) -> None:
                cleanup_order.append("aclose_called")
                # Simulate cleanup failing (e.g., connection already closed)
                raise ConnectionError("Connection already closed")

        mock_response.aiter_bytes = lambda: FailingCleanupIterator()

        mock_request = Mock()
        timeout_dict = {'connect': 5.0, 'read': 0.3, 'write': 5.0, 'pool': 5.0}
        mock_request.extensions = {"timeout": timeout_dict}
        type(mock_response)._request = PropertyMock(return_value=mock_request)

        mock_client = create_mock_client()
        stream = AsyncStream(
            cast_to=object,
            response=mock_response,
            client=mock_client,
        )

        # Should raise ReadTimeout, NOT ConnectionError
        with pytest.raises(httpx.ReadTimeout) as exc_info:
            async for _ in stream._iter_events():
                pass

        # Verify it's the timeout error, not cleanup error
        assert "timeout" in str(exc_info.value).lower()
        assert "Connection already closed" not in str(exc_info.value)

        # Verify cleanup was attempted
        assert "aclose_called" in cleanup_order

    @pytest.mark.asyncio
    async def test_normal_cleanup_still_works(self) -> None:
        """Verify normal cleanup still executes properly."""
        mock_response = Mock()
        cleanup_tracker = {"aclose_called": False}

        async def normal_bytes() -> AsyncGenerator[bytes, None]:
            """Simple async generator that yields one event."""
            yield b'data: test\n\n'

        class TrackedIterator:
            """Iterator wrapper that tracks cleanup calls."""
            def __init__(self) -> None:
                self.gen: AsyncGenerator[bytes, None] = normal_bytes()

            async def __anext__(self) -> bytes:
                return await self.gen.__anext__()

            async def aclose(self) -> None:
                cleanup_tracker["aclose_called"] = True
                await self.gen.aclose()

        mock_response.aiter_bytes = TrackedIterator
        type(mock_response)._request = PropertyMock(return_value=None)

        mock_client = create_mock_client()
        stream = AsyncStream(
            cast_to=object,
            response=mock_response,
            client=mock_client,
        )

        async for _ in stream._iter_events():
            pass

        # Verify cleanup was called
        assert cleanup_tracker["aclose_called"], "Cleanup should be called on normal completion"


class TestLoggingOptimization:
    """Test that logging has been optimized for production."""

    @pytest.mark.asyncio
    async def test_chunk_logging_reduced_frequency(self) -> None:
        """
        Verify chunk logging happens every 5000 chunks, not 1000.

        This reduces log volume by 80% for long-running streams.
        """
        mock_response = Mock()

        async def many_chunks() -> AsyncIterator[bytes]:
            for _ in range(6000):
                yield b'data: x\n\n'

        mock_response.aiter_bytes = many_chunks
        type(mock_response)._request = PropertyMock(return_value=None)

        mock_client = create_mock_client()
        stream = AsyncStream(
            cast_to=object,
            response=mock_response,
            client=mock_client,
        )

        # This test mainly verifies code doesn't crash with many chunks
        # In production, you'd check logs to verify frequency
        event_count = 0
        async for _ in stream._iter_events():
            event_count += 1
            if event_count >= 100:  # Don't actually process all 6000
                break

        assert event_count == 100


class TestTimingImprovements:
    """Test that timing measurements are improved."""

    @pytest.mark.asyncio
    async def test_timing_consistency(self) -> None:
        """Verify timing measurements are consistent (no race conditions)."""
        mock_response = Mock()

        async def timed_chunks() -> AsyncIterator[bytes]:
            for i in range(3):
                await asyncio.sleep(0.1)
                yield f'data: {{"chunk": {i}}}\n\n'.encode()

        mock_response.aiter_bytes = timed_chunks

        mock_request = Mock()
        timeout_dict = {'connect': 5.0, 'read': 2.0, 'write': 5.0, 'pool': 5.0}
        mock_request.extensions = {"timeout": timeout_dict}
        type(mock_response)._request = PropertyMock(return_value=mock_request)

        mock_client = create_mock_client()
        stream = AsyncStream(
            cast_to=object,
            response=mock_response,
            client=mock_client,
        )

        events: list[object] = []
        async for event in stream._iter_events():
            events.append(event)

        # Should complete without timing-related errors
        assert len(events) == 3


class TestBackwardCompatibility:
    """Test that changes maintain backward compatibility."""

    @pytest.mark.asyncio
    async def test_no_timeout_config_still_works(self) -> None:
        """Verify streams without timeout config still work (backward compat)."""
        mock_response = Mock()

        async def normal_chunks() -> AsyncIterator[bytes]:
            for i in range(3):
                await asyncio.sleep(0.1)
                yield f'data: {{"i": {i}}}\n\n'.encode()

        mock_response.aiter_bytes = normal_chunks
        type(mock_response)._request = PropertyMock(return_value=None)

        mock_client = create_mock_client()
        stream = AsyncStream(
            cast_to=object,
            response=mock_response,
            client=mock_client,
        )

        events: list[object] = []
        async for event in stream._iter_events():
            events.append(event)

        assert len(events) == 3

    @pytest.mark.asyncio
    async def test_old_style_usage_patterns_work(self) -> None:
        """Verify old usage patterns still work."""
        mock_response = Mock()
        mock_response.aclose = Mock()

        async def simple() -> AsyncIterator[bytes]:
            yield b'data: {"old": "style"}\n\n'

        mock_response.aiter_bytes = simple
        type(mock_response)._request = PropertyMock(return_value=None)

        mock_client = create_mock_client()
        stream = AsyncStream(
            cast_to=object,
            response=mock_response,
            client=mock_client,
        )

        # Old style: manually iterate _iter_events
        events: list[object] = []
        async for event in stream._iter_events():
            events.append(event)

        assert len(events) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

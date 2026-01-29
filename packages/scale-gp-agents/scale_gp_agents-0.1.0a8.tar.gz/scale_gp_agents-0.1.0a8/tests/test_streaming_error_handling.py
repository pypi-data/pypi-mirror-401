"""
Tests for error handling improvements in streaming module.

These tests verify that the streaming code gracefully handles:
- Invalid JSON in SSE data
- Malformed UTF-8 sequences
- RemoteProtocolError logging at INFO level
"""
# pyright: reportUnknownVariableType=false, reportUnknownMemberType=false, reportUnknownArgumentType=false
import logging
from typing import AsyncIterator
from unittest.mock import Mock, PropertyMock

import httpx
import pytest

from sgp_agents._streaming import SSEDecoder, AsyncStream, ServerSentEvent


def create_mock_client() -> Mock:
    """Create a mock client with a real SSEDecoder."""
    mock_client = Mock()
    mock_client._make_sse_decoder.return_value = SSEDecoder()
    return mock_client


class TestJSONErrorHandling:
    """Test that invalid JSON in SSE data is handled gracefully."""

    def test_json_decode_error_raises_valueerror(self) -> None:
        """Verify that invalid JSON raises ValueError with clear message."""
        sse = ServerSentEvent(
            event=None,
            data="this is not valid json {",
            id=None,
            retry=None
        )

        with pytest.raises(ValueError) as exc_info:
            sse.json()

        assert "invalid JSON" in str(exc_info.value)
        assert "Expecting" in str(exc_info.value)  # From JSONDecodeError

    def test_json_decode_error_logs_at_error_level(self, caplog: pytest.LogCaptureFixture) -> None:
        """Verify that invalid JSON is logged at ERROR level."""
        sse = ServerSentEvent(
            event=None,
            data='{"incomplete": ',
            id=None,
            retry=None
        )

        with caplog.at_level(logging.ERROR):
            try:
                sse.json()
            except ValueError:
                pass  # Expected

        # Check that error was logged
        assert any("[SSE] Invalid JSON" in record.message for record in caplog.records)

    def test_valid_json_still_works(self) -> None:
        """Verify that valid JSON parsing still works correctly."""
        sse = ServerSentEvent(
            event=None,
            data='{"key": "value", "number": 42}',
            id=None,
            retry=None
        )

        result = sse.json()
        assert result == {"key": "value", "number": 42}

    def test_json_error_includes_data_preview(self, caplog: pytest.LogCaptureFixture) -> None:
        """Verify that error log includes data preview for debugging."""
        long_data = "x" * 500 + " invalid json"
        sse = ServerSentEvent(
            event=None,
            data=long_data,
            id=None,
            retry=None
        )

        with caplog.at_level(logging.ERROR):
            try:
                sse.json()
            except ValueError:
                pass

        # Should truncate at 200 chars
        error_message = caplog.records[0].message
        assert "Data preview:" in error_message
        # Make sure it doesn't include the full 500+ char string
        assert len(error_message) < 400


class TestUTF8ErrorHandling:
    """Test that malformed UTF-8 sequences are handled gracefully."""

    @pytest.mark.asyncio
    async def test_utf8_decode_error_skips_line(self, caplog: pytest.LogCaptureFixture) -> None:
        """Verify that invalid UTF-8 line is skipped with warning."""
        mock_response = Mock()

        async def chunks_with_invalid_utf8() -> AsyncIterator[bytes]:
            # Valid SSE event with invalid UTF-8 in one line
            yield b"data: valid line\n"
            yield b"data: \xff\xfe invalid UTF-8\n"  # Invalid UTF-8 sequence
            yield b"data: another valid line\n\n"

        mock_response.aiter_bytes = chunks_with_invalid_utf8
        type(mock_response)._request = PropertyMock(return_value=None)

        mock_client = create_mock_client()
        stream = AsyncStream(
            cast_to=dict,
            response=mock_response,
            client=mock_client,
        )

        with caplog.at_level(logging.WARNING):
            events = []
            async for event in stream._iter_events():
                events.append(event)

        # Should receive 1 event (the invalid line was skipped)
        assert len(events) == 1
        assert "valid line" in events[0].data
        assert "another valid line" in events[0].data

        # Check that warning was logged
        assert any("Failed to decode line as UTF-8" in record.message for record in caplog.records)

    @pytest.mark.asyncio
    async def test_utf8_error_includes_hex_preview(self, caplog: pytest.LogCaptureFixture) -> None:
        """Verify that UTF-8 error log includes hex preview for debugging."""
        mock_response = Mock()

        async def chunks_with_invalid_utf8() -> AsyncIterator[bytes]:
            yield b"data: \xff\xfe\xfd\n\n"  # Invalid UTF-8

        mock_response.aiter_bytes = chunks_with_invalid_utf8
        type(mock_response)._request = PropertyMock(return_value=None)

        mock_client = create_mock_client()
        stream = AsyncStream(
            cast_to=dict,
            response=mock_response,
            client=mock_client,
        )

        with caplog.at_level(logging.WARNING):
            events = []
            async for event in stream._iter_events():
                events.append(event)

        # Check that hex preview is in log
        warning_message = caplog.records[0].message
        assert "hex" in warning_message.lower()
        assert "fffefd" in warning_message  # Hex representation of the invalid bytes

    def test_sync_utf8_decode_error_skips_line(self, caplog: pytest.LogCaptureFixture) -> None:
        """Verify that sync decoder also skips invalid UTF-8."""
        from typing import Iterator
        decoder = SSEDecoder()

        def chunks_with_invalid_utf8() -> Iterator[bytes]:
            yield b"data: valid\n\n"
            yield b"data: \xff\xfe\n\n"  # Invalid UTF-8
            yield b"data: also valid\n\n"

        with caplog.at_level(logging.WARNING):
            events = list(decoder.iter_bytes(chunks_with_invalid_utf8()))

        # Should receive 2 events (invalid was skipped)
        assert len(events) == 2
        assert events[0].data == "valid"
        assert events[1].data == "also valid"

        # Check warning was logged
        assert any("Failed to decode line as UTF-8" in record.message for record in caplog.records)


class TestRemoteProtocolErrorLogging:
    """Test that RemoteProtocolError is logged at INFO, not ERROR."""

    @pytest.mark.asyncio
    async def test_remote_protocol_error_logs_at_info_level(self, caplog: pytest.LogCaptureFixture) -> None:
        """Verify RemoteProtocolError is logged at INFO level in decoder."""
        mock_response = Mock()

        async def chunks_then_error() -> AsyncIterator[bytes]:
            yield b"data: chunk0\n\n"
            raise httpx.RemoteProtocolError("Server closed connection")

        mock_response.aiter_bytes = chunks_then_error
        type(mock_response)._request = PropertyMock(return_value=None)

        mock_client = create_mock_client()
        stream = AsyncStream(
            cast_to=dict,
            response=mock_response,
            client=mock_client,
        )

        with caplog.at_level(logging.INFO):
            events = []
            try:
                async for event in stream._iter_events():
                    events.append(event)
            except httpx.RemoteProtocolError:
                pass  # Expected

        # Check that it was logged at INFO, not ERROR
        info_logs = [r for r in caplog.records if r.levelname == "INFO"]
        error_logs = [r for r in caplog.records if r.levelname == "ERROR"]

        assert len(events) == 1
        assert any("Server closed connection" in r.message or "Stream ended" in r.message for r in info_logs)
        # Should NOT be in error logs
        assert not any("RemoteProtocolError" in r.message for r in error_logs)

    @pytest.mark.asyncio
    async def test_remote_protocol_error_by_class_name(self, caplog: pytest.LogCaptureFixture) -> None:
        """Verify class name check catches RemoteProtocolError."""
        # Create a mock exception with the same name but different instance
        class FakeRemoteProtocolError(Exception):
            """Fake exception with same name to test class name matching."""
            pass

        # Monkey-patch the class name
        FakeRemoteProtocolError.__name__ = "RemoteProtocolError"

        mock_response = Mock()

        async def chunks_then_error() -> AsyncIterator[bytes]:
            yield b"data: chunk0\n\n"
            raise FakeRemoteProtocolError("Fake error")

        mock_response.aiter_bytes = chunks_then_error
        type(mock_response)._request = PropertyMock(return_value=None)

        mock_client = create_mock_client()
        stream = AsyncStream(
            cast_to=dict,
            response=mock_response,
            client=mock_client,
        )

        with caplog.at_level(logging.INFO):
            try:
                async for _ in stream._iter_events():
                    pass
            except FakeRemoteProtocolError:
                pass  # Expected

        # Should be logged at INFO because class name matches
        info_logs = [r for r in caplog.records if r.levelname == "INFO"]
        assert any("Stream ended" in r.message for r in info_logs)


class TestIntegrationScenarios:
    """Test complete scenarios combining multiple error types."""

    @pytest.mark.asyncio
    async def test_stream_continues_after_invalid_utf8_line(self) -> None:
        """Verify stream continues processing after encountering invalid UTF-8."""
        mock_response = Mock()

        async def mixed_chunks() -> AsyncIterator[bytes]:
            yield b"data: {\"valid\": 1}\n\n"
            yield b"data: \xff\xfe\n"  # Invalid UTF-8 line
            yield b"data: {\"also_valid\": 2}\n\n"

        mock_response.aiter_bytes = mixed_chunks
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

        # Should successfully parse both valid events
        assert len(events) == 2
        assert events[0].json() == {"valid": 1}
        assert events[1].json() == {"also_valid": 2}


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

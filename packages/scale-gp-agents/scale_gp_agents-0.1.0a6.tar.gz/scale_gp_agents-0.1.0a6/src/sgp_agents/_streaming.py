# Note: initially copied from https://github.com/florimondmanca/httpx-sse/blob/master/src/httpx_sse/_decoders.py
from __future__ import annotations

import json
import time
import asyncio
import inspect
import logging
from types import TracebackType
from typing import TYPE_CHECKING, Any, Generic, TypeVar, Iterator, AsyncIterator, cast
from typing_extensions import Self, Protocol, TypeGuard, override, get_origin, runtime_checkable

import httpx

from ._utils import extract_type_var_from_base

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from ._client import Agents, AsyncAgents


_T = TypeVar("_T")


class Stream(Generic[_T]):
    """Provides the core interface to iterate over a synchronous stream response."""

    response: httpx.Response

    _decoder: SSEBytesDecoder

    def __init__(
        self,
        *,
        cast_to: type[_T],
        response: httpx.Response,
        client: Agents,
    ) -> None:
        self.response = response
        self._cast_to = cast_to
        self._client = client
        self._decoder = client._make_sse_decoder()
        self._iterator = self.__stream__()

    def __next__(self) -> _T:
        return self._iterator.__next__()

    def __iter__(self) -> Iterator[_T]:
        for item in self._iterator:
            yield item

    def _iter_events(self) -> Iterator[ServerSentEvent]:
        yield from self._decoder.iter_bytes(self.response.iter_bytes())

    def __stream__(self) -> Iterator[_T]:
        cast_to = cast(Any, self._cast_to)
        response = self.response
        process_data = self._client._process_response_data
        iterator = self._iter_events()

        try:
            for sse in iterator:
                yield process_data(data=sse.json(), cast_to=cast_to, response=response)
        finally:
            # CRITICAL: Always close the response to release the connection
            # This ensures cleanup happens even when:
            # - The client breaks early (doesn't consume all chunks)
            # - An exception occurs during streaming
            # - The iterator is cancelled
            response.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        """
        Close the response and release the connection.

        Automatically called if the response body is read to completion.
        """
        self.response.close()


class AsyncStream(Generic[_T]):
    """Provides the core interface to iterate over an asynchronous stream response."""

    response: httpx.Response

    _decoder: SSEDecoder | SSEBytesDecoder

    def __init__(
        self,
        *,
        cast_to: type[_T],
        response: httpx.Response,
        client: AsyncAgents,
    ) -> None:
        self.response = response
        self._cast_to = cast_to
        self._client = client
        self._decoder = client._make_sse_decoder()
        self._iterator = self.__stream__()

    async def __anext__(self) -> _T:
        return await self._iterator.__anext__()

    async def __aiter__(self) -> AsyncIterator[_T]:
        async for item in self._iterator:
            yield item

    async def _iter_events(self) -> AsyncIterator[ServerSentEvent]:
        # CRITICAL: Wrap the byte iteration with a timeout to prevent indefinite hangs
        # when the server stops sending data but doesn't close the connection.
        # We wrap the byte stream to add timeout while preserving decoder state.

        # Extract timeout from request extensions
        # httpx stores timeout as a dict: {'connect': 5.0, 'read': 2.0, 'write': 5.0, 'pool': 5.0}
        # Default to None (no timeout) unless explicitly configured
        timeout_seconds: float | None = None
        timeout_extraction_debug: dict[str, Any] = {"has_request": False, "has_extensions": False, "timeout_dict": None}

        if hasattr(self.response, '_request') and self.response._request is not None:
            timeout_extraction_debug["has_request"] = True
            if hasattr(self.response._request, 'extensions'):
                timeout_extraction_debug["has_extensions"] = True
                # extensions is MutableMapping[str, Any] from httpx, safe to access as dict
                timeout_dict: Any = self.response._request.extensions.get('timeout')  # type: ignore[reportUnknownMemberType]
                timeout_extraction_debug["timeout_dict"] = timeout_dict

                # timeout_dict is a dictionary with timeout values
                if timeout_dict is not None and isinstance(timeout_dict, dict):
                    # Extract read timeout from dict
                    timeout_dict_typed = cast("dict[str, Any]", timeout_dict)
                    read_timeout = timeout_dict_typed.get('read')
                    if read_timeout is not None and isinstance(read_timeout, (int, float)):
                        timeout_seconds = float(read_timeout)
                        logger.info(
                            f"[AsyncStream] Timeout extraction successful: read_timeout={timeout_seconds}s "
                            f"from extensions dict {timeout_dict}"
                        )
                    else:
                        logger.info(
                            f"[AsyncStream] Read timeout is None in config: {timeout_dict}. "
                            "No per-chunk timeout will be applied."
                        )
                else:
                    logger.warning(
                        f"[AsyncStream] Timeout config exists but is not a dict: "
                        f"type={type(timeout_dict)}, value={timeout_dict}"
                    )

        if timeout_seconds is None:
            logger.info(
                f"[AsyncStream] No timeout configured. Debug info: {timeout_extraction_debug}. "
                "Stream will wait indefinitely for chunks (original behavior)."
            )

        # Wrap byte iterator with timeout protection while maintaining single stream
        chunk_count = 0
        total_bytes = 0
        start_time = time.time()

        async def timeout_protected_bytes() -> AsyncIterator[bytes]:
            """Wraps byte iteration with per-chunk timeout while keeping stream continuous."""
            nonlocal chunk_count, total_bytes

            byte_iterator = self.response.aiter_bytes()
            last_chunk_time = time.time()

            try:
                while True:
                    try:
                        chunk_start = time.time()

                        if timeout_seconds is not None:
                            # Apply timeout to each chunk read
                            chunk = await asyncio.wait_for(
                                byte_iterator.__anext__(),
                                timeout=timeout_seconds
                            )
                        else:
                            # No timeout - use original behavior
                            chunk = await byte_iterator.__anext__()

                        chunk_count += 1
                        chunk_size = len(chunk)
                        total_bytes += chunk_size
                        chunk_duration = time.time() - chunk_start
                        time_since_last = time.time() - last_chunk_time
                        last_chunk_time = time.time()

                        # Log every 1000 chunks or if chunk took >10s
                        if chunk_count % 1000 == 0 or chunk_duration > 10.0:
                            logger.info(
                                f"[AsyncStream] Chunk #{chunk_count}: "
                                f"size={chunk_size}B, "
                                f"duration={chunk_duration:.2f}s, "
                                f"since_last={time_since_last:.2f}s, "
                                f"total_bytes={total_bytes}, "
                                f"timeout={timeout_seconds}s"
                            )

                        yield chunk

                    except StopAsyncIteration:
                        elapsed = time.time() - start_time
                        logger.info(
                            f"[AsyncStream] Stream completed normally: "
                            f"chunks={chunk_count}, "
                            f"total_bytes={total_bytes}, "
                            f"elapsed={elapsed:.2f}s"
                        )
                        break

                    except asyncio.TimeoutError as timeout_err:
                        elapsed_since_last = time.time() - last_chunk_time
                        total_elapsed = time.time() - start_time

                        logger.error(
                            f"[AsyncStream] TIMEOUT after {elapsed_since_last:.1f}s waiting for chunk: "
                            f"last_chunk=#{chunk_count}, "
                            f"total_bytes={total_bytes}, "
                            f"timeout_config={timeout_seconds}s, "
                            f"total_elapsed={total_elapsed:.1f}s. "
                            f"Server may have stopped sending data without closing connection."
                        )

                        # Raise httpx.ReadTimeout so application code can catch it specifically
                        raise httpx.ReadTimeout(
                            f"Stream read timeout after {timeout_seconds}s waiting for data. "
                            f"Last chunk received: #{chunk_count} ({total_bytes} bytes total). "
                            "Server may have stopped sending data without closing connection."
                        ) from timeout_err

            except Exception as e:
                if not isinstance(e, (StopAsyncIteration, httpx.ReadTimeout, asyncio.TimeoutError)):
                    logger.error(
                        f"[AsyncStream] Unexpected error in byte iterator: "
                        f"type={type(e).__name__}, "
                        f"error={e}, "
                        f"chunk_count={chunk_count}, "
                        f"total_bytes={total_bytes}"
                    )
                raise
            finally:
                # Cleanup
                if hasattr(byte_iterator, 'aclose') and callable(getattr(byte_iterator, 'aclose', None)):
                    await byte_iterator.aclose()  # type: ignore[attr-defined]
                    logger.debug(f"[AsyncStream] Byte iterator cleanup completed")

        # Pass continuous stream to decoder (preserves buffer state)
        try:
            sse_count = 0
            async for sse in self._decoder.aiter_bytes(timeout_protected_bytes()):
                sse_count += 1
                if sse_count % 1000 == 0:
                    logger.info(
                        f"[AsyncStream] Decoded SSE event #{sse_count}: "
                        f"total_chunks={chunk_count}, "
                        f"total_bytes={total_bytes}"
                    )
                yield sse

            logger.info(f"[AsyncStream] All SSE events decoded: count={sse_count}")

        except Exception as e:
            logger.error(
                f"[AsyncStream] Error during SSE decoding: "
                f"type={type(e).__name__}, "
                f"error={e}, "
                f"chunk_count={chunk_count}, "
                f"total_bytes={total_bytes}"
            )
            raise

    async def __stream__(self) -> AsyncIterator[_T]:
        cast_to = cast(Any, self._cast_to)
        response = self.response
        process_data = self._client._process_response_data
        iterator = self._iter_events()

        try:
            async for sse in iterator:
                yield process_data(data=sse.json(), cast_to=cast_to, response=response)
        finally:
            # CRITICAL: Always close the response to release the connection
            # This ensures cleanup happens even when:
            # - The client breaks early (doesn't consume all chunks)
            # - An exception occurs during streaming
            # - The iterator is cancelled
            await response.aclose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()

    async def close(self) -> None:
        """
        Close the response and release the connection.

        Automatically called if the response body is read to completion.
        """
        await self.response.aclose()


class ServerSentEvent:
    def __init__(
        self,
        *,
        event: str | None = None,
        data: str | None = None,
        id: str | None = None,
        retry: int | None = None,
    ) -> None:
        if data is None:
            data = ""

        self._id = id
        self._data = data
        self._event = event or None
        self._retry = retry

    @property
    def event(self) -> str | None:
        return self._event

    @property
    def id(self) -> str | None:
        return self._id

    @property
    def retry(self) -> int | None:
        return self._retry

    @property
    def data(self) -> str:
        return self._data

    def json(self) -> Any:
        return json.loads(self.data)

    @override
    def __repr__(self) -> str:
        return f"ServerSentEvent(event={self.event}, data={self.data}, id={self.id}, retry={self.retry})"


class SSEDecoder:
    _data: list[str]
    _event: str | None
    _retry: int | None
    _last_event_id: str | None

    def __init__(self) -> None:
        self._event = None
        self._data = []
        self._last_event_id = None
        self._retry = None

    def iter_bytes(self, iterator: Iterator[bytes]) -> Iterator[ServerSentEvent]:
        """Given an iterator that yields raw binary data, iterate over it & yield every event encountered"""
        for chunk in self._iter_chunks(iterator):
            # Split before decoding so splitlines() only uses \r and \n
            for raw_line in chunk.splitlines():
                line = raw_line.decode("utf-8")
                sse = self.decode(line)
                if sse:
                    yield sse

    def _iter_chunks(self, iterator: Iterator[bytes]) -> Iterator[bytes]:
        """Given an iterator that yields raw binary data, iterate over it and yield individual SSE chunks"""
        data = b""
        for chunk in iterator:
            for line in chunk.splitlines(keepends=True):
                data += line
                if data.endswith((b"\r\r", b"\n\n", b"\r\n\r\n")):
                    yield data
                    data = b""
        if data:
            yield data

    async def aiter_bytes(self, iterator: AsyncIterator[bytes]) -> AsyncIterator[ServerSentEvent]:
        """Given an iterator that yields raw binary data, iterate over it & yield every event encountered"""
        async for chunk in self._aiter_chunks(iterator):
            # Split before decoding so splitlines() only uses \r and \n
            for raw_line in chunk.splitlines():
                line = raw_line.decode("utf-8")
                sse = self.decode(line)
                if sse:
                    yield sse

    async def _aiter_chunks(self, iterator: AsyncIterator[bytes]) -> AsyncIterator[bytes]:
        """Given an iterator that yields raw binary data, iterate over it and yield individual SSE chunks"""
        data = b""
        async for chunk in iterator:
            for line in chunk.splitlines(keepends=True):
                data += line
                if data.endswith((b"\r\r", b"\n\n", b"\r\n\r\n")):
                    yield data
                    data = b""
        if data:
            yield data

    def decode(self, line: str) -> ServerSentEvent | None:
        # See: https://html.spec.whatwg.org/multipage/server-sent-events.html#event-stream-interpretation  # noqa: E501

        if not line:
            if not self._event and not self._data and not self._last_event_id and self._retry is None:
                return None

            sse = ServerSentEvent(
                event=self._event,
                data="\n".join(self._data),
                id=self._last_event_id,
                retry=self._retry,
            )

            # NOTE: as per the SSE spec, do not reset last_event_id.
            self._event = None
            self._data = []
            self._retry = None

            return sse

        if line.startswith(":"):
            return None

        fieldname, _, value = line.partition(":")

        if value.startswith(" "):
            value = value[1:]

        if fieldname == "event":
            self._event = value
        elif fieldname == "data":
            self._data.append(value)
        elif fieldname == "id":
            if "\0" in value:
                pass
            else:
                self._last_event_id = value
        elif fieldname == "retry":
            try:
                self._retry = int(value)
            except (TypeError, ValueError):
                pass
        else:
            pass  # Field is ignored.

        return None


@runtime_checkable
class SSEBytesDecoder(Protocol):
    def iter_bytes(self, iterator: Iterator[bytes]) -> Iterator[ServerSentEvent]:
        """Given an iterator that yields raw binary data, iterate over it & yield every event encountered"""
        ...

    def aiter_bytes(self, iterator: AsyncIterator[bytes]) -> AsyncIterator[ServerSentEvent]:
        """Given an async iterator that yields raw binary data, iterate over it & yield every event encountered"""
        ...


def is_stream_class_type(typ: type) -> TypeGuard[type[Stream[object]] | type[AsyncStream[object]]]:
    """TypeGuard for determining whether or not the given type is a subclass of `Stream` / `AsyncStream`"""
    origin = get_origin(typ) or typ
    return inspect.isclass(origin) and issubclass(origin, (Stream, AsyncStream))


def extract_stream_chunk_type(
    stream_cls: type,
    *,
    failure_message: str | None = None,
) -> type:
    """Given a type like `Stream[T]`, returns the generic type variable `T`.

    This also handles the case where a concrete subclass is given, e.g.
    ```py
    class MyStream(Stream[bytes]):
        ...

    extract_stream_chunk_type(MyStream) -> bytes
    ```
    """
    from ._base_client import Stream, AsyncStream

    return extract_type_var_from_base(
        stream_cls,
        index=0,
        generic_bases=cast("tuple[type, ...]", (Stream, AsyncStream)),
        failure_message=failure_message,
    )

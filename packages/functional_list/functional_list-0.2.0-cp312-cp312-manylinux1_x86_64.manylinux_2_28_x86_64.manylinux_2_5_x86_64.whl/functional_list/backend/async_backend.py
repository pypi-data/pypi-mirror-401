"""functional_list.backend.async_backend

Async backend implementation for ListMapper.

This backend is meant for workloads where the mapping/filtering function is an
*async* coroutine function (I/O-bound work). It uses `asyncio` to run many tasks
concurrently.

Important notes
--------------
- This is NOT a multi-process backend. It runs in a single Python process.
- Best for network/file I/O (HTTP calls, database queries, etc.).
- For CPU-bound workloads, prefer LocalBackend(mode="processes").
- ListMapper's API is synchronous, so this backend internally runs an event loop
  when you call map/filter/foreach.

Caveats
-------
- If you're already inside a running event loop (e.g. in Jupyter/async app),
  calling this backend from synchronous code may raise a RuntimeError.
  In that case you should either:
  - use another backend, or
  - call your async pipeline directly with asyncio (future extension).

Example
-------
>>> import asyncio
>>> from functional_list.list_functional_mapper import ListMapper
>>> from functional_list.backend import AsyncBackend
>>>
>>> async def fetch(x: int) -> int:
...     await asyncio.sleep(0.01)
...     return x * 2
>>>
>>> out = ListMapper[int](1, 2, 3).map(fetch, backend=AsyncBackend())
>>> out.to_list()
[2, 4, 6]
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
    List,
    Optional,
    Sequence,
    TypeVar,
    cast,
)

from functional_list.backend.base import BackendError, BaseBackend

T = TypeVar("T")
U = TypeVar("U")


async def _gather_limited(
    coros: List[Awaitable[U]],
    *,
    concurrency: Optional[int],
) -> List[U]:
    """Gather coroutines with an optional concurrency limit."""

    if concurrency is None or concurrency <= 0:
        return await asyncio.gather(*coros)

    sem = asyncio.Semaphore(concurrency)

    async def _run(coro: Awaitable[U]) -> U:
        async with sem:
            return await coro

    return await asyncio.gather(*[_run(c) for c in coros])


@dataclass(frozen=True)
class AsyncBackend(BaseBackend):
    """Asyncio-based backend for coroutine functions.

    Parameters
    ----------
    concurrency:
        Maximum number of in-flight tasks. If None, no explicit limit is applied.

    Notes
    -----
    The `func` passed to map/filter/foreach MUST be an async function.
    """

    concurrency: Optional[int] = None

    name: str = "async"

    def _run(self, coro: Awaitable[U]) -> U:
        """Run a coroutine to completion.

        Raises
        ------
        BackendError
            If called from within an already running event loop.
        """

        try:
            return asyncio.run(cast(Coroutine[Any, Any, U], coro))
        except RuntimeError as e:
            # Common case: "asyncio.run() cannot be called from a running event loop"
            raise BackendError(
                "AsyncBackend cannot be executed from within an already running event loop. "
                "Use another backend or run the coroutine pipeline directly with asyncio."
            ) from e

    def map(self, data: Sequence[T], func: Callable[[T], Any]) -> List[U]:  # type: ignore[override]
        """Map using an async function.

        Parameters
        ----------
        data:
            Input sequence.
        func:
            Async function called for each item.

        Returns
        -------
        list
            Mapped results.

        Raises
        ------
        BackendError
            If `func` is not async or if executed inside a running event loop.
        """

        if not asyncio.iscoroutinefunction(func):
            raise BackendError("AsyncBackend requires an async function for map().")

        async def _main() -> List[U]:
            coros = [func(x) for x in data]  # type: ignore[misc]
            return await _gather_limited(coros, concurrency=self.concurrency)

        return self._run(_main())

    def filter(self, data: Sequence[T], pred: Callable[[T], Any]) -> List[T]:  # type: ignore[override]
        """Filter using an async predicate."""

        if not asyncio.iscoroutinefunction(pred):
            raise BackendError("AsyncBackend requires an async function for filter().")

        async def _main() -> List[T]:
            coros = [pred(x) for x in data]  # type: ignore[misc]
            flags = await _gather_limited(coros, concurrency=self.concurrency)
            return [x for x, keep in zip(data, flags) if bool(keep)]

        return self._run(_main())

    def foreach(self, data: Sequence[T], func: Callable[[T], Any]) -> None:  # type: ignore[override]
        """Execute an async side-effecting function for each element."""

        if not asyncio.iscoroutinefunction(func):
            raise BackendError("AsyncBackend requires an async function for foreach().")

        async def _main() -> None:
            coros = [func(x) for x in data]  # type: ignore[misc]
            await _gather_limited(coros, concurrency=self.concurrency)

        _ = self._run(_main())

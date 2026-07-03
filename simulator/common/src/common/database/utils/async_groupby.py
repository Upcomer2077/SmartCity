from collections.abc import AsyncIterator, Callable
from typing import TypeVar

T = TypeVar("T")
K = TypeVar("K")


async def async_groupby(
    iterator: AsyncIterator[T],
    key_func: Callable[[T], K],
) -> AsyncIterator[tuple[K, list[T]]]:
    current_key: K | None = None
    current_group: list[T] = []

    async for item in iterator:
        item_key = key_func(item)

        if current_key is None:
            current_key = item_key

        if item_key != current_key:
            yield current_key, current_group
            current_key = item_key
            current_group = []

        current_group.append(item)

    if current_key is not None:
        yield current_key, current_group

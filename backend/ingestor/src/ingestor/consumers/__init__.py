from abc import ABC, abstractmethod
from collections.abc import AsyncIterator


class BaseConsumer(ABC):
    @abstractmethod
    async def start(self): ...

    @abstractmethod
    def __anext__(self): ...

    @abstractmethod
    def __aiter__(self) -> AsyncIterator: ...

    @abstractmethod
    async def stop(self): ...

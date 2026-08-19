from abc import ABC, abstractmethod


class ILogger(ABC):
    @abstractmethod
    def info(self, msg: str) -> None: ...

    @abstractmethod
    def error(self, msg: str, exc: Exception | None = None) -> None: ...

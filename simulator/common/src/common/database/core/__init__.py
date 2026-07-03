from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncEngine


class DBCore(ABC):
    _instance = None
    _engine: AsyncEngine

    def get_engine(self):
        return self._engine

    @abstractmethod
    def _set_async_engine(self, db_url) -> AsyncEngine:
        pass

    def __new__(cls, db_url: str):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._engine = cls._set_async_engine(cls._instance, db_url)

        return cls._instance

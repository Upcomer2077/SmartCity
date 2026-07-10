from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncEngine


class DBCore(ABC):
    """Abstract base class for managing a singleton database engine lifecycle."""

    _instance = None
    _engine: AsyncEngine

    def get_engine(self):
        """Get the initialized asynchronous database engine.

        Returns:
            AsyncEngine: The active SQLAlchemy async engine instance.
        """
        return self._engine

    @abstractmethod
    def _set_async_engine(self, db_url: str) -> AsyncEngine:
        """Abstract method to initialize and return the async database engine.

        Args:
            db_url (str): Connection string for the database.

        Returns:
            AsyncEngine: Configured SQLAlchemy async engine.
        """
        pass

    def __new__(cls, db_url: str):
        """Create or return the singleton instance and initialize the engine.

        Args:
            db_url (str): Connection string for the database.

        Returns:
            DBCore: The singleton instance of the class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._engine = cls._set_async_engine(cls._instance, db_url)

        return cls._instance

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker

from common.database.core import DBCore
from common.logger_ import mlogger


class DBManager:
    """Manager for database session lifecycle and connection pool disposal."""

    def __init__(self, db_core: DBCore) -> None:
        """Initialize the manager and create an async session factory.

        Args:
            db_core (DBCore): Database core instance holding the engine.
        """
        self._a_session_factory = async_sessionmaker(
            db_core.get_engine(), expire_on_commit=False
        )
        self.__db_core = db_core
        mlogger.info("Database manager initialized. Connection established")

    def get_session_factory(self):
        """Get the configured asynchronous session factory.

        Returns:
            async_sessionmaker: The factory for creating async database sessions.
        """
        return self._a_session_factory

    async def dispose(self):
        """Flush SQLite WAL checkpoints and dispose of the database engine."""
        mlogger.info("Disposing db engine and cleaning WAL files")
        engine = self.__db_core.get_engine()

        try:
            async with engine.connect() as conn:
                await conn.execute(text("PRAGMA wal_checkpoint(TRUNCATE);"))
                await conn.execute(text("PRAGMA journal_mode=DELETE;"))
            mlogger.info("WAL checkpoint executed successfully. Files removed")
        except Exception as e:
            mlogger.error(
                f"Could not cleanly flush WAL files: {e}. Force closing pool..."
            )

        finally:
            await engine.dispose()
            mlogger.info("Database engine fully disposed")

from common.database.core import DBCore
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


class DBCoreSqlite(DBCore):
    def _set_async_engine(self, db_url) -> AsyncEngine:
        engine = create_async_engine(
            db_url,
            echo=False,
            pool_pre_ping=True,
            connect_args={"timeout": 30},
        )
        event.listen(engine.sync_engine, "connect", self._set_sqlite_pragma)
        return engine

    def _set_sqlite_pragma(self, dbapi_connection, *_args):
        """Configures SQLite performance and safety settings on connection."""
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")  # Concurrent read/write
        cursor.execute("PRAGMA synchronous=NORMAL")  # Reduced disk syncs
        cursor.execute("PRAGMA cache_size=-20000")  # 20MB page cache
        cursor.execute("PRAGMA busy_timeout=10000")  # Lock wait timeout
        cursor.execute("PRAGMA foreign_keys=ON")  # Enforce constraints
        cursor.close()

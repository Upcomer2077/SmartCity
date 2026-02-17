from sqlalchemy import event
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


class DBManager:
    _DATABASE_URL = "sqlite+aiosqlite:///./db.db"

    _ENGINE = create_async_engine(
        _DATABASE_URL, echo=False, pool_pre_ping=True, connect_args={"timeout": 30}
    )
    ASYNC_SESSION_LOCAL = async_sessionmaker(_ENGINE, expire_on_commit=False)

    @classmethod
    def GET_ENGINE_INSTANCE(cls):
        return cls._ENGINE


@event.listens_for(DBManager.GET_ENGINE_INSTANCE().sync_engine, "connect")
def set_sqlite_pragma(dbapi_connection, _connection_record):
    """Configures SQLite performance and safety settings on connection."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")  # Concurrent read/write
    cursor.execute("PRAGMA synchronous=NORMAL")  # Reduced disk syncs
    cursor.execute("PRAGMA cache_size=-20000")  # 20MB page cache
    cursor.execute("PRAGMA busy_timeout=10000")  # Lock wait timeout
    cursor.execute("PRAGMA foreign_keys=ON")  # Enforce constraints
    cursor.close()

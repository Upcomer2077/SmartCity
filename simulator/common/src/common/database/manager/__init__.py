from common.database.core import DBCore
from common.logger_ import mlogger
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker


class DBManager:
    def __init__(self, db_core: DBCore) -> None:
        self._a_session_factory = async_sessionmaker(
            db_core.get_engine(), expire_on_commit=False
        )
        self.__db_core = db_core
        mlogger.info("Database manager initialized. Connection established")

    def get_session_factory(self):
        return self._a_session_factory

    async def dispose(self):
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

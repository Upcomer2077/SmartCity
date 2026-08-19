from unittest.mock import AsyncMock, MagicMock, Mock

import pytest
from common.database.manager import DBManager


class TestManager:
    @pytest.mark.asyncio
    async def test_db_dispose_call(self):
        engine_mock = MagicMock()
        engine_mock.dispose = AsyncMock()
        engine_mock.get_engine = MagicMock(return_value=engine_mock)

        await DBManager(engine_mock).dispose()
        engine_mock.dispose.assert_called_once()

    def test_db_get_session_factory(self, monkeypatch):
        mock = MagicMock()
        instance = DBManager(Mock())
        monkeypatch.setattr(instance, "_a_session_factory", mock)
        result = instance.get_session_factory()
        assert result == mock

from abc import ABC
from unittest.mock import Mock

import pytest
from common.database.core import DBCore
from common.database.core.sqlite import DBCoreSqlite


@pytest.fixture(params=[DBCoreSqlite])
def core(request) -> type[DBCore]:
    return request.param


class TestDBCore:
    def test_is_abstract(self):
        assert issubclass(DBCore, ABC)

    def test_is_subclass(self, core):
        assert issubclass(core, DBCore)

    def test_get_props(self, core: type[DBCore], monkeypatch: pytest.MonkeyPatch):
        mock = Mock()
        monkeypatch.setattr(core, "_set_async_engine", lambda _x, _y: mock)
        instance = core("f")
        assert instance.get_engine() == mock
        assert instance._instance is core("f")

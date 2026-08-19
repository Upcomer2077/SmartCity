from abc import ABC

import pytest
from common.logger_.impl import ILogger
from common.logger_.impl.stdlogger import PythonStdLogger


class TestLogger:
    def test_is_abstract(
        self,
    ):
        assert issubclass(ILogger, ABC)

    @pytest.mark.parametrize("lg", [PythonStdLogger])
    def test_is_subclass(self, lg):
        assert issubclass(lg, ILogger)

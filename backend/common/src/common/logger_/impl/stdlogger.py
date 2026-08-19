import logging
import sys

from common.logger_.impl import ILogger


class PythonStdLogger(ILogger):
    def __init__(self, name: str = "app", level: int = logging.INFO) -> None:
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)
        self._logger.propagate = False

        if not self._logger.handlers:
            handler = logging.StreamHandler(sys.stdout)

            formatter = logging.Formatter(
                fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

    def info(self, msg: str) -> None:
        self._logger.info(msg)

    def error(self, msg: str, exc: Exception | None = None) -> None:
        self._logger.error(msg, exc_info=exc)

import logging

from common.logger_.impl import ILogger
from common.logger_.impl.stdlogger import PythonStdLogger

mlogger: ILogger = PythonStdLogger(level=logging.INFO)


def configure_logger(custom_logger: ILogger):
    global mlogger
    mlogger = custom_logger

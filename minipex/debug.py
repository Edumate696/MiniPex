import logging
import logging as _logging
import sys as _sys
from .util import singleton as _singleton
from . import __name__ as _logger_name


@_singleton
class Logger:
    __logger = _logging.getLogger(_logger_name)
    __fomatter = logging.Formatter('[%(levelname)-7s] File %(pathname)s, line %(lineno)s ->  %(message)s')
    __handler = logging.StreamHandler(_sys.stdout)
    __handler.setFormatter(__fomatter)
    for hdlr in __logger.handlers:
        __logger.removeHandler(hdlr)
    __logger.addHandler(__handler)
    __logger.setLevel(_logging.DEBUG)

    WARNING = _logging.WARNING
    INFO = _logging.INFO
    DEBUG = _logging.DEBUG
    NOTSET = _logging.NOTSET

    def __init__(self):
        pass

    @staticmethod
    def __log(level, msg, *params):
        Logger.__logger.log(level, msg, *params, stacklevel=3)

    @staticmethod
    def log(level, msg, *params):
        if not isinstance(level, int):
            raise TypeError("level must be an integer")
        Logger.__log(level, msg, *params)

    @staticmethod
    def info(msg, *params):
        Logger.__log(Logger.INFO, msg, *params)

    @staticmethod
    def warn(msg, *params):
        Logger.__log(Logger.WARNING, msg, *params)

    @staticmethod
    def debug(msg, *params):
        Logger.__log(Logger.DEBUG, msg, *params)

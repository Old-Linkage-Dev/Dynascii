
# -*- coding: UTF-8 -*-

import logging as _logging;
import logging.handlers as _logging_handlers;

def _format_stream_message(record: _logging.LogRecord) -> str:
    _rstc = "\033[0m";
    _mtc = "\033[0;35m";
    _ptc = "\033[0;32m";
    _modc = "\033[0;33m";
    _fw = "\033[0;33m >> ";
    if record.levelno >= _logging.CRITICAL:
        _lc = "\033[1;31m";
        _mc = "\033[0;31m";
    elif record.levelno >= _logging.WARNING:
        _lc = "\033[1;33m";
        _mc = "\033[0;33m";
    elif record.levelno >= _logging.INFO:
        _lc = "\033[1;34m";
        _mc = "\033[0m";
    elif record.levelno >= _logging.DEBUG:
        _lc = "\033[1;30m";
        _mc = "\033[0m";
    else:
        _mtc = "\033[1;30m";
        _ptc = "\033[1;30m";
        _modc = "\033[1;30m";
        _fw = "\033[1;30m >> ";
        _lc = "\033[1;30m";
        _mc = "\033[1;30m";
    if record.threadName == "MainThread" and record.module in ("dynascii", "__init__", "__main__"):
        return f"{_rstc}{record.asctime} {_lc}{record.levelname:<10}{_fw}{_mtc}[Dynascii]{_fw}{_mc}{record.message}";
    elif record.threadName == "MainThread":
        return f"{_rstc}{record.asctime} {_lc}{record.levelname:<10}{_fw}{_mtc}[{record.module}]{_fw}{_mc}{record.message}";
    elif record.module in ("dynascii", "__init__", "__main__"):
        return f"{_rstc}{record.asctime} {_lc}{record.levelname:<10}{_fw}{_ptc}[{record.threadName}]{_fw}{_mc}{record.message}";
    else:
        return f"{_rstc}{record.asctime} {_lc}{record.levelname:<10}{_fw}{_ptc}[{record.threadName}]{_fw}{_modc}[{record.module}]{_fw}{_mc}{record.message}";

def _format_file_message(record: _logging.LogRecord) -> str:
    if record.module in ("dynascii", "__init__", "__main__"):
        return f"[{record.asctime}][{record.levelname:<10}][Dynascii] >> {record.message}";
    else:
        return f"[{record.asctime}][{record.levelname:<10}][{record.threadName}] >> {record.message}";

def LoggerFileHandler(file : str):
    try:
        _logger_formatter_file = _logging.Formatter(fmt="[%(asctime)s][%(levelname)s][%(threadName)s][%(module)s] >> %(message)s", datefmt="%Y-%m-%d-%H:%M:%S");
        _logger_formatter_file.formatMessage = _format_stream_message;
        _logger_ch_file = _logging_handlers.TimedRotatingFileHandler(file, when = "D", interval = 60, backupCount = 12, encoding = "utf8");
        _logger_ch_file.setLevel(_logging.DEBUG);
        _logger_ch_file.setFormatter(_logger_formatter_file);
        return _logger_ch_file;
    except:
        raise ValueError("Invalid log file: %s." % file);

def LoggerStreamLevelHandler(level : str):
    try:
        _level = getattr(_logging, level.upper(), None);
        _logger_formatter_stream = _logging.Formatter(fmt="[%(asctime)s][%(levelname)s] >> [%(threadName)s] >> [%(module)s] >> %(message)s", datefmt="%H:%M");
        _logger_formatter_stream.formatMessage = _format_stream_message;
        _logger_ch_stream = _logging.StreamHandler();
        _logger_ch_stream.setLevel(level = _level);
        _logger_ch_stream.setFormatter(_logger_formatter_stream);
        return _logger_ch_stream;
    except:
        raise ValueError("Invalid log level: %s." % level);

def set_logger_stream_handler(handler : _logging.StreamHandler):
    global _logger_stream_handler;
    if _logger_stream_handler:
        logger.removeHandler(_logger_stream_handler);
    _logger_stream_handler = handler;
    if _logger_stream_handler:
        logger.addHandler(_logger_stream_handler);

def remove_logger_stream_handler():
    set_logger_stream_handler(None);

logger = _logging.getLogger("dynascii");
logger.setLevel(_logging.DEBUG);

_logger_stream_handler = LoggerStreamLevelHandler("INFO");
logger.addHandler(_logger_stream_handler);

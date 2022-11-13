
# -*- coding: UTF-8 -*-

import argparse                         as _argparse;
import logging                          as _logging;
import logging.handlers                 as _logging_handlers;
import sys                              as _sys;
from ._logging import logger            as _logger;
from ._logging import set_stream_level  as _set_stream_level;

def _try_default(f, default):
    try:
        return f();
    except:
        return default;

def _Shell(module : str):
    try:
        return __import__(module, fromlist = ["Shell"]).Shell(**kwargs_shell);
    except:
        raise _argparse.ArgumentError(message = "Fail to load shell indicated, check shell name and shell args.");

def _uint(val):
    val = int(val);
    if val >= 0:
        return val;
    else:
        raise ValueError();

def _uint16(val):
    val = int(val);
    if val >= 0 and val <= 65535:
        return val;
    else:
        raise ValueError();

def _LoggerFile(file : str):
    try:
        _logger_formatter_file = _logging.Formatter(fmt="[%(asctime)s][%(levelname)s] >> [%(threadName)s] >> [%(module)s] >> %(message)s", datefmt="%Y-%m-%d-%H:%M:%S");
        _logger_ch_file = _logging_handlers.TimedRotatingFileHandler(file, when = "D", interval = 60, backupCount = 12, encoding = "utf8");
        _logger_ch_file.setLevel( _logging.DEBUG);
        _logger_ch_file.setFormatter(_logger_formatter_file);
        _logger.addHandler(_logger_ch_file);
        return file;
    except:
        raise ValueError(message = "Not a valid logging file.");

def _LoggerLevel(level : str):
    try:
        _level = getattr( _logging, level.upper(), None);
        if not isinstance(_level, int):
            raise ValueError("Invalid log level: %s" % level);
        _set_stream_level(_level);
        return _level;
    except:
        raise ValueError(message = "Not a valid logging level.");

_sysargs = _sys.argv[1:];
_index_arg_spliter = _try_default(lambda:_sysargs.index("--"), -1);

if (_index_arg_spliter != -1):
    _args_dynascii = _sysargs[ : _index_arg_spliter];
    _args_shell = _sysargs[_index_arg_spliter + 1 : ];
else:
    _args_dynascii = _sysargs[ : ];
    _args_shell = [];

# _parser = _argparse.ArgumentParser(description = open("./README.md", "r").read());
_parser = _argparse.ArgumentParser(description = "");
_parser.add_argument("--log",                dest = "log_file", type = _LoggerFile, default = None,                 help = "str : path to log file");
_parser.add_argument("--log-level",          dest = "log_level", type = _LoggerLevel, default = _logging.INFO,      help = "str : name of logging level");
_parser.add_argument("-6",                   dest = "use_v6", action = "store_true", default = False,               help = "flag : use of IPv6");
_parser.add_argument("--host",               dest = "host", type = str, default = "",                               help = "str : hostname of server");
_parser.add_argument("--port",               dest = "port", type = _uint16, default = 23,                           help = "uint16 : port of server");
_parser.add_argument("--blocking-io",        dest = "blocking_io", action = "store_true", default = False,          help = "bool : use of blocking IO");
_parser.add_argument("--no-blocking-io",     dest = "blocking_io", action = "store_false", default = False,         help = "bool : use of blocking IO, flagged for not using");
_parser.add_argument("--blocking-timeout",   dest = "blocking_timeout", type = _uint, default = 3,                  help = "uint : time of blocking IO timeout, 0 for no timeout");
_parser.add_argument("--no-blocking-delay",  dest = "no_blocking_delay", type = _uint, default = 1,                 help = "uint : time of non-blocking IO inter-polling delay");
_parser.add_argument("--backlogs",           dest = "backlogs", type = _uint, default = 16,                         help = "uint : backlogs of server");
_parser.add_argument("--poolsize",           dest = "pool_size", type = _uint, default = 32,                        help = "uint : size of server thread pool");
_parser.add_argument("--shell",              dest = "shell", type = _Shell, default = "dynascii.shell.nullshell",   help = "module : name of shell module");

kwargs_shell = {};
while _args_shell:
    _s = _args_shell.pop(0);
    if len(_args_shell) >= 1 and _s.startswith("--"):
        kwargs_shell[_s[2:]] = _args_shell.pop(0);

args = _parser.parse_args(_args_dynascii);

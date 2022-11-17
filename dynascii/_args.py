
# -*- coding: UTF-8 -*-

import argparse                         as _argparse;
import logging                          as _logging;
import sys                              as _sys;

from ._logging import LoggerFileHandler         as _LoggerFileHandler;
from ._logging import LoggerStreamLevelHandler  as _LoggerStreamLevelHandler;
from ._logging import set_logger_stream_handler as _set_logger_stream_handler;
from ._logging import _logger_stream_handler    as _logger_stream_handler;
from ._logging import logger                    as _logger;

def _try_default(f, default):
    try:
        return f();
    except:
        return default;

def _Shell(module : str):
    try:
        return __import__(module, fromlist = ["Shell"]).Shell(**kwargs_shell);
    except Exception as e:
        raise _argparse.ArgumentError(message = (
            "Fail to load shell indicated by %s, check shell name and shell args.\n" % module +
            "%s" % e
        ));

def _LoggerFileHandlerSetting(file : str):
    _handler = _LoggerFileHandler(file = file);
    _logger.addHandler(_handler);
    return _handler;

def _LoggerStreamLevelHandlerSetting(level : str):
    _handler = _LoggerStreamLevelHandler(level = level);
    _set_logger_stream_handler(_handler);
    return _handler;

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

_parser.add_argument(
    "--log",
    dest = "log_file", type = _LoggerFileHandlerSetting,
    default = None,
    help = "str : path to log file"
);

_parser.add_argument(
    "--log-level",
    dest = "log_level", type = _LoggerStreamLevelHandlerSetting,
    default = _logger_stream_handler,
    help = "str : name of logging level"
);

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
    if _s.startswith("--") and "=" in _s:
        _sl = _s.split("=", 1);
        kwargs_shell[_sl[0][2:]] = _sl[1];
    elif _s.startswith("--") and len(_args_shell) >= 1 :
        kwargs_shell[_s[2:]] = _args_shell.pop(0);

args = _parser.parse_args(_args_dynascii);

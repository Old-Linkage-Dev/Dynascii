#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse;
import sys;
import time;
import socket;
import threading;
import logging;
import traceback;

def formatMessage(record: logging.LogRecord) -> str:
    if record.threadName == 'MainThread':
        return f'\033[0m{record.asctime} \033[1;34m{record.levelname:<10}\033[0;33m >> \033[0;35m[Main]\033[0;33m >> \033[0m{record.message}';
    elif record.module == 'Dynascii':
        return f'\033[0m{record.asctime} \033[1;34m{record.levelname:<10}\033[0;33m >> \033[0;31m[{record.threadName}]\033[0;33m >> \033[0m{record.message}';
    else:
        return f'\033[0m{record.asctime} \033[1;34m{record.levelname:<10}\033[0;33m >> \033[0;31m[{record.threadName}]\033[0;33m >> \033[0;33m[{record.module}]\033[0;33m >> \033[0m{record.message}';

logger = logging.getLogger("dynascii");
logger.setLevel(logging.DEBUG);
logger_formatter_stream = logging.Formatter(fmt='\033[0m%(asctime)s \033[1;34m[%(levelname)s]\033[0;33m >> \033[0;35m[%(threadName)s]\033[0;33m >> \033[0m%(message)s', datefmt='%H:%M');
logger_formatter_stream.datefmt = '%H:%M';
logger_formatter_stream.formatMessage = formatMessage;
logger_ch_stream = logging.StreamHandler();
logger_ch_stream.setFormatter(logger_formatter_stream);
logger.addHandler(logger_ch_stream);



if __name__ == "__main__":

    def try_default(f, default):
        try:
            return f();
        except:
            return default;
    
    sysargs = sys.argv[1:];
    index_arg_spliter = try_default(lambda:sysargs.index("--"), -1);

    if (index_arg_spliter != -1):
        args_dynascii = sysargs[ : index_arg_spliter];
        args_shell = sysargs[index_arg_spliter + 1 : ];
    else:
        args_dynascii = sysargs[ : ];
        args_shell = [];

    kwargs_shell = {};
    while args_shell:
        s = args_shell.pop(0);
        if len(args_shell) >= 1 and s.startswith("--"):
            kwargs_shell[s[2:]] = args_shell.pop(0);
    
    def _Shell(module : str):
        try:
            return __import__(module).Shell(**kwargs_shell);
        except:
            raise argparse.ArgumentError(message = "Fail to load shell indicated, check shell name and shell args");
    
    def _LoggerLevel(level : str):
        try:
            return logging._nameToLevel[level];
        except:
            raise ValueError();

    def uint(val):
        val = int(val);
        if val >= 0:
            return val;
        else:
            raise ValueError();
    
    def uint16(val):
        val = int(val);
        if val >= 0 and val <= 65535:
            return val;
        else:
            raise ValueError();

    parser = argparse.ArgumentParser(description = open("./README.md", 'r').read());
    parser.add_argument("--log",                dest = "log_file", type = str, default = None,                          help = "str : path to log file");
    parser.add_argument("--log-level",          dest = "log_level", type = _LoggerLevel, default = logging.INFO,        help = "str : name of logging level");
    parser.add_argument("-6",                   dest = "use_v6", action = "store_true", default = False,                help = "flag : use of IPv6");
    parser.add_argument("--host",               dest = "host", type = str, default = "",                                help = "str : hostname of server");
    parser.add_argument("--port",               dest = "port", type = uint16, default = 23,                             help = "uint16 : port of server");
    parser.add_argument("--blocking-io",        dest = "blocking_io", action = "store_true", default = False,           help = "bool : use of blocking IO");
    parser.add_argument("--blocking-timeout",   dest = "blocking_timeout", type = uint, default = 3,                    help = "uint : time of blocking IO timeout, 0 for no timeout");
    parser.add_argument("--no-blocking-delay",  dest = "no_blocking_delay", type = uint, default = 1,                   help = "uint : time of non-blocking IO inter-polling delay");
    parser.add_argument("--backlogs",           dest = "backlogs", type = uint, default = 16,                           help = "uint : backlogs of server");
    parser.add_argument("--poolsize",           dest = "pool_size", type = uint, default = 32,                          help = "uint : size of server thread pool");
    parser.add_argument("--shell",              dest = "shell", type = _Shell, default = "nullshell",                   help = "module : name of shell module");

    args = parser.parse_args(args_dynascii);

    if args.log_file:
        _logger_formatter_file = logging.Formatter(fmt='[%(asctime)s][%(levelname)s] >> [%(threadName)s] >> [%(module)s] >> %(message)s', datefmt='%Y-%m-%d-%H:%M:%S');
        _logger_ch_file = logging.FileHandler(args.log_file, encoding = 'utf8');
        _logger_ch_file.setLevel(logging.DEBUG);
        _logger_ch_file.setFormatter(_logger_formatter_file);
        logger.addHandler(_logger_ch_file);

    logger_ch_stream.setLevel(args.log_level);

    logger.info(
        'Parametered with \n' +
        '  - LOG_FILE        = %s\n' % args.log_file +
        '  - HOST            = %s\n' % args.host +
        '  - PORT            = %d\n' % args.port +
        '  - BACKLOG         = %d\n' % args.backlogs +
        '  - POOL_SIZE       = %d\n' % args.pool_size +
        '  - SHELL           = %s\n' % args.shell +
        '  --\n' +
        '\n'.join(['  - ' + str(key).upper().ljust(16) + '= ' + str(val) for key, val in kwargs_shell.items()]) +
        '.');

    logger.info("Creating server ...");

    server = (
        socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not args.use_v6 else socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    );
    server.bind((args.host, args.port));
    server.listen(args.backlogs);
    if args.blocking_io:
        server.setblocking(True);
        if args.blocking_timeout > 0:
            server.settimeout(args.blocking_timeout);
    pool = [];

    logger.info("Creating thread pool ...");

    class PoolThread(threading.Thread):
        def __init__(self, poolid):
            super().__init__();
            self.running = True;
            self.poolid = poolid;
            self.name = 'PoolThread#%d(%s)' % (self.poolid, hex(id(self)));
            self.daemon = True;
        def run(self):
            logger.debug('%s started.' % thread.name);
            while self.running:
                try:
                    conn, addr = server.accept();
                    logger.debug('%s calling a shell.' % thread.name);
                    args.shell(conn, addr);
                except BlockingIOError:
                    if args.no_blocking_delay > 0:
                        time.sleep(args.no_blocking_delay);
                    continue;
                except TimeoutError:
                    continue;
                except Exception as err:
                    logger.error(err);
                    logger.debug(traceback.format_exc());
                    logger.critical('%s run into an exception.' % thread.name);
                    break;

    logger.info('Starting tasks...');

    for poolid in range(args.pool_size):
        thread = PoolThread(poolid = poolid);
        logger.debug("%s starting..." % thread.name);
        pool.append(thread);
        thread.start();

    logger.info('Running...');

    try:
        while True:
            time.sleep(60);
            for poolid in range(args.pool_size):
                if not pool[poolid].is_alive():
                    logger.debug("Restarting PoolThread#%d ..." % poolid);
                    thread = PoolThread(poolid = poolid);
                    logger.debug("%s starting..." % thread.name);
                    pool[poolid] = thread;
                    thread.start();
    except KeyboardInterrupt:
        logger.info("Ending...");
        for poolid in range(args.pool_size):
            if pool[poolid].is_alive():
                logger.debug("Terminating PoolThread#%d ..." % poolid);
                pool[poolid].running = False;
        if not args.blocking_io or args.blocking_timeout > 0:
            for poolid in range(args.pool_size):
                if pool[poolid].is_alive():
                    logger.debug("Waiting PoolThread#%d ..." % poolid);
                    pool[poolid].join();
        logger.info("Ended.");

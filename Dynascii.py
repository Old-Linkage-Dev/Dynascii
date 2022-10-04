#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse;

import sys;
import time;
import socket;
import logging;

if __name__ == "__main__":

    from numpy import uint, uint16;

    def _PoolThread(module : str):
        return __import__(module).PoolThread;

    def _Shell(module : str):
        return __import__(module).Shell;

    def try_default(f, default):
        try:
            return f();
        except:
            return default;

    sysargs = sys.argv[1:];
    index_pool_thread = try_default(lambda:sysargs.index("--"), -1);
    index_shell = try_default(lambda:sysargs.index("---"), -1);

    if (index_pool_thread != -1 and index_shell != -1):
        args_dynascii = sysargs[ : min(index_pool_thread, index_shell)];
        if (index_pool_thread < index_shell):
            args_pool_thread = sysargs[index_pool_thread + 1 : index_shell];
            args_shell = sysargs[index_shell + 1 : ];
        else:
            args_pool_thread = sysargs[index_shell + 1 : index_pool_thread];
            args_shell = sysargs[index_pool_thread + 1 : ];
    elif (index_pool_thread == -1 and index_shell != -1):
        args_dynascii = sysargs[ : index_shell];
        args_pool_thread = [];
        args_shell = sysargs[index_shell + 1 : ];
    elif (index_pool_thread != -1 and index_shell == -1):
        args_dynascii = sysargs[ : index_pool_thread];
        args_pool_thread = sysargs[index_pool_thread + 1 : ];
        args_shell = [];
    else:
        args_dynascii = sysargs[ : ];
        args_pool_thread = [];
        args_shell = [];

    parser = argparse.ArgumentParser(description = open("./README.md", 'r').read());
    parser.add_argument("-l", "--log",  dest = "log_file", type = str, default = None,                          help = "str : path to log file");
    parser.add_argument("-6",           dest = "use_v6", action = "store_true", default = False,                help = "flag : use IPv6");
    parser.add_argument("-h", "--host", dest = "host", type = str, default = "",                                help = "str : server hostname");
    parser.add_argument("-p", "--port", dest = "port", type = uint16, default = 23,                             help = "server port");
    parser.add_argument("--backlogs",   dest = "backlogs", type = uint, default = 16,                           help = "server backlogs");
    parser.add_argument("--poolsize",   dest = "pool_size", type = uint, default = 32,                          help = "server thread pool size");
    parser.add_argument("--pthread",    dest = "class_pool_thread", type = _PoolThread, default = "poolthread", help = "module : thread in pool");
    parser.add_argument("--shell",      dest = "class_shell", type = _Shell, default = "nullshell",             help = "module : shell");

    args = parser.parse_args(args_dynascii);

    kwargs = {};
    while args_pool_thread:
        s = args_pool_thread.pop(0);
        if len(args_pool_thread) >= 1 and s.startswith("--"):
            kwargs[s[2:]] = args_pool_thread.pop(0);
    while args_pool_thread:
        s = args_pool_thread.pop(0);
        if len(args_pool_thread) >= 1 and s.startswith("--"):
            kwargs[s[2:]] = args_pool_thread.pop(0);
    
    _logger_formatter_file = logging.Formatter(fmt='[%(asctime)s][%(levelname)s] >> [%(threadName)s] >> %(message)s', datefmt='%Y-%m-%d-%H:%M:%S');
    _logger_ch_file = logging.FileHandler(args.log_file, encoding = 'utf8') if args.log_file else None;
    _logger_ch_file.setLevel(logging.DEBUG);
    _logger_ch_file.setFormatter(_logger_formatter_file);

    _logger_root = logging.getLogger("dynascii");
    _logger_root.setLevel(logging.DEBUG);
    _logger_root.addHandler(_logger_ch_file) if args.log_file else ...;



    _logger_formatter_scrn = logging.Formatter(fmt='\033[0m%(asctime)s \033[1;34m[%(levelname)s]\033[0;33m >> \033[0;35m[%(threadName)s]\033[0;33m >> \033[0m%(message)s', datefmt='%H:%M');
    _logger_ch_scrn = logging.StreamHandler();
    _logger_ch_scrn.setLevel(logging.INFO);
    _logger_ch_scrn.setFormatter(_logger_formatter_scrn);

    logger = logging.getLogger("dynascii").getChild("main");
    logger.addHandler(_logger_ch_scrn);



    logger.info(
        'Parametered with \n' +
        '  - LOG_FILE        = %s\n' % args.log_file +
        '  - HOST            = %s\n' % args.host +
        '  - PORT            = %d\n' % args.port +
        '  - BACKLOG         = %d\n' % args.backlogs +
        '  - POOL_SIZE       = %d\n' % args.pool_size +
        '  - PTHREAD         = %s\n' % args.class_pool_thread +
        '  - SHELL           = %s\n' % args.class_shell +
        '\n'.join(['  - ' + str(key).upper().ljust(16) + '= ' + str(val) for key, val in KWARGS.items()]) +
        '.');
    logger.info('Running...');

    server = (
        socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not args.use_v6 else socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    );
    server.bind((args.host, args.port));
    server.listen(args.backlogs);
    server.setblocking(True);
    pool = [];

    for poolid in range(args.pool_size):
        pthread = args.class_pool_thread(poolid = poolid, server = server, Shell = args.class_shell, **kwargs);
        logger.info("Pool thread [%s] starting..." % pthread.name);
        pool.append(pthread);
        pthread.start();

    try:
        while True:
            time.sleep(60);
            for poolid in range(args.pool_size):
                if not pool[poolid].is_alive():
                    pthread = args.class_pool_thread(poolid = poolid, server = server, Shell = args.class_shell, **kwargs);
                    logger.info("Pool thread [%s] is dead, restarting [%s]..." % (pool[poolid].name, pthread.name));
                    pool[poolid] = pthread;
                    pthread.start();
    except KeyboardInterrupt:
        logger.info("Ending...");
        for poolid in range(args.pool_size):
            if pool[poolid].is_alive():
                pool[poolid].running = False;
        if not server.getblocking():
            for poolid in range(args.pool_size):
                if pool[poolid].is_alive():
                    pool[poolid].join();
            logger.info("Ended.");

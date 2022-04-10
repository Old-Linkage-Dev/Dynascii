#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

LOG_FILE = './telnet_cast.log';

HOST = '127.0.0.1'
PORT = 23;

BACKLOG = 16;
POOL_SIZE = 32;
SHELL = __import__("nullshell").Shell;

import sys;
import socket;
import logging;
import traceback;

logger = logging.getLogger(__name__);
logger.setLevel(logging.DEBUG);



_logger_formatter_file = logging.Formatter(fmt='[%(asctime)s][%(levelname)s] >> [%(threadName)s] >> %(message)s', datefmt='%Y-%m-%d-%H:%M:%S');
_logger_ch_file = logging.FileHandler(LOG_FILE, encoding = 'utf8');
_logger_ch_file.setLevel(logging.DEBUG);
_logger_ch_file.setFormatter(_logger_formatter_file);

_logger_root = logging.getLogger("dynascii");
_logger_root.setLevel(logging.DEBUG);
_logger_root.addHandler(_logger_ch_file);



_logger_formatter_scrn = logging.Formatter(fmt='\033[0m%(asctime)s \033[1;34m[%(levelname)s]\033[0;33m >> \033[0;35m[%(threadName)s]\033[0;33m >> \033[0m%(message)s', datefmt='%H:%M');
_logger_ch_scrn = logging.StreamHandler();
_logger_ch_scrn.setLevel(logging.INFO);
_logger_ch_scrn.setFormatter(_logger_formatter_scrn);

logger = logging.getLogger("dynascii").getChild("main");
logger.addHandler(_logger_ch_scrn);

KWARGS = {};
args = sys.argv[1:];
while args:
    s = args.pop(0);
    if len(args) >= 1 and s.lower() == "--log":
        LOG_FILE = args.pop(0);
    elif len(args) >= 1 and s.lower() == "--host":
        HOST = args.pop(0);
    elif len(args) >= 1 and s.lower() == "--port":
        PORT = int(args.pop(0));
    elif len(args) >= 1 and s.lower() == "--backlog":
        BACKLOG = int(args.pop(0));
    elif len(args) >= 1 and s.lower() == "--poolsize":
        POOL_SIZE = int(args.pop(0));
    elif len(args) >= 1 and s.lower() == "--shell":
        SHELL = __import__(args.pop(0)).Shell;
    elif len(args) >= 1 and s.startswith("--"):
        KWARGS[s[2:]] = args.pop(0);

logger.info(
    'Parametered with \n' +
    '  - LOG_FILE        = %s\n' % LOG_FILE +
    '  - HOST            = %s\n' % HOST +
    '  - PORT            = %d\n' % PORT +
    '  - BACKLOG         = %d\n' % BACKLOG +
    '  - POOL_SIZE       = %d\n' % POOL_SIZE +
    '  - SHELL           = %s\n' % SHELL +
    '\n'.join(['  - ' + str(key).upper().ljust(16) + '= ' + str(val) for key, val in KWARGS.items()]) +
    '.');
logger.info('Running...');

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
server.bind((HOST, PORT));
server.listen(BACKLOG);
server.setblocking(True);
userpool = [];

while True:
    try:
        conn, addr = server.accept();
        rl = [];
        ipps = {addr[0] : 0};
        tps = 0;
        for ip, port, user in userpool:
            if user.is_alive():
                tps += 1;
                if (ip in ipps):
                    ipps[ip] += 1;
                else:
                    ipps[ip] = 1;
            else:
                rl.append((ip, port, user));
        for userdata in rl:
            userpool.remove(userdata);
        if (tps < TOTAL_POOL_SIZE and ipps[addr[0]] < IP_POOL_SIZE):
            user = SHELL(conn = conn, logger = logger, **ARGS);
            userdata = (*addr, user);
            userpool.append(userdata);
            logger.info('User new [%s] @%s:%d.' % (user.name, *addr));
            user.start();
        else:
            user = SHELL_REJECT(conn = conn, logger = logger);
            logger.info('User pool overflow [%s] @%s:%d.' % (user.name, *addr));
            user.start();
    except BlockingIOError:
        continue;
    except Exception as err:
        logger.error(err);
        logger.debug(traceback.format_exc());
        logger.critical('Main Loop run into an exception.');
        break;


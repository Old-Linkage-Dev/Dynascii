#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

LOG_FILE = './telnet_cast.log';

HOST = '127.0.0.1'
PORT = 23;

BACKLOGS = 16;
POOL_SIZE = 32;

PTHREAD = __import__("poolthread").PoolThread;
SHELL = __import__("nullshell").Shell;

import sys;
import time;
import socket;
import logging;



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
    elif len(args) >= 1 and s.lower() == "--backlogs":
        BACKLOGS = int(args.pop(0));
    elif len(args) >= 1 and s.lower() == "--poolsize":
        POOL_SIZE = int(args.pop(0));
    elif len(args) >= 1 and s.lower() == "--poolthread":
        PTHREAD = __import__(args.pop(0)).PoolThread;
    elif len(args) >= 1 and s.lower() == "--shell":
        SHELL = __import__(args.pop(0)).Shell;
    elif len(args) >= 1 and s.startswith("--"):
        KWARGS[s[2:]] = args.pop(0);

logger.info(
    'Parametered with \n' +
    '  - LOG_FILE        = %s\n' % LOG_FILE +
    '  - HOST            = %s\n' % HOST +
    '  - PORT            = %d\n' % PORT +
    '  - BACKLOG         = %d\n' % BACKLOGS +
    '  - POOL_SIZE       = %d\n' % POOL_SIZE +
    '  - SHELL           = %s\n' % SHELL +
    '\n'.join(['  - ' + str(key).upper().ljust(16) + '= ' + str(val) for key, val in KWARGS.items()]) +
    '.');
logger.info('Running...');

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
server.bind((HOST, PORT));
server.listen(BACKLOGS);
server.setblocking(True);
pool = [];

for poolid in range(POOL_SIZE):
    pthread = PTHREAD(poolid = poolid, server = server, Shell = SHELL, **KWARGS);
    logger.info("Pool thread [%s] starting..." % pthread.name);
    pool.append(pthread);
    pthread.start();

try:
    while True:
        time.sleep(60);
        for poolid in range(POOL_SIZE):
            if not pool[poolid].is_alive():
                pthread = PTHREAD(poolid = poolid, server = server, Shell = SHELL, **KWARGS);
                logger.info("Pool thread [%s] is dead, restarting [%s]..." % (pool[poolid].name, pthread.name));
                pool[poolid] = pthread;
                pthread.start();
except KeyboardInterrupt:
    logger.info("Ending...");
    for poolid in range(POOL_SIZE):
        if pool[poolid].is_alive():
            pool[poolid].running = False;
    server.setblocking(False);
    for poolid in range(POOL_SIZE):
        if pool[poolid].is_alive():
            pool[poolid].join();
    logger.info("Ended.");
    
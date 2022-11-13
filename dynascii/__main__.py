#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import time;
import socket;
import threading;
import traceback;

from ._logging import logger;
from ._args import kwargs_shell;
from ._args import args;

class _PoolThread(threading.Thread):
    def __init__(self, poolid):
        super().__init__();
        logger.debug("Initing a thread of pool id %d..." % poolid);
        self.running = True;
        self.poolid = poolid;
        self.name = "PoolThread#%d" % self.poolid;
        self.daemon = True;
        logger.debug("Inited a thread of pool id %d." % poolid);
    def run(self):
        logger.info("%s started." % self.name);
        while self.running:
            try:
                conn, addr = server.accept();
                logger.debug("%s calling a shell." % self.name);
            except BlockingIOError:
                if args.no_blocking_delay > 0:
                    time.sleep(args.no_blocking_delay);
                continue;
            except (TimeoutError, socket.timeout):
                continue;
            except Exception as err:
                logger.error(err);
                logger.debug(traceback.format_exc());
                logger.critical("%s run into an exception listening." % self.name);
                break;
            try:
                args.shell(conn, addr);
                logger.debug("%s closing connection." % self.name);
                conn.close();
                logger.debug("%s closed connection." % self.name);
            except Exception as err:
                logger.error(err);
                logger.debug(traceback.format_exc());
                logger.critical("%s run into an exception running." % self.name);
                break;
        logger.info("%s ended." % self.name);

if __name__ == "__main__":

    logger.info(
        "Parametered with \n" +
        "  - LOG_FILE        = %s\n" % args.log_file +
        "  - HOST            = %s\n" % args.host +
        "  - PORT            = %d\n" % args.port +
        "  - BLOCKING-IO     = %s\n" % args.blocking_io +
        "  - BACKLOG         = %d\n" % args.backlogs +
        "  - POOL_SIZE       = %d\n" % args.pool_size +
        "  - SHELL           = %s\n" % args.shell +
        "  --\n" +
        "\n".join(["  - " + str(key).upper().ljust(16) + "= " + str(val) for key, val in kwargs_shell.items()]) +
        ".");

    logger.info("Creating server...");

    server_args = (socket.SOCK_STREAM,); # Considering socket.SO_REUSEADDR, socket.SO_REUSEPORT
    server = (
        socket.socket(socket.AF_INET, *server_args)
        if not args.use_v6
        else socket.socket(socket.AF_INET6, *server_args)
    );
    server.bind((args.host, args.port));
    server.listen(args.backlogs);
    server.setblocking(args.blocking_io);
    if args.blocking_io:
        if args.blocking_timeout > 0:
            server.settimeout(args.blocking_timeout);
    pool = [];

    logger.info("Creating thread pool...");

    logger.info("Starting tasks...");

    for poolid in range(args.pool_size):
        thread = _PoolThread(poolid = poolid);
        logger.debug("%s starting..." % thread.name);
        pool.append(thread);
        thread.start();

    logger.info("Running...");

    try:
        while True:
            time.sleep(60);
            for poolid in range(args.pool_size):
                if not pool[poolid].is_alive():
                    logger.debug("Restarting PoolThread#%d..." % poolid);
                    thread = _PoolThread(poolid = poolid);
                    logger.debug("%s starting..." % thread.name);
                    pool[poolid] = thread;
                    thread.start();
    except KeyboardInterrupt:
        logger.info("Ending...");
        for poolid in range(args.pool_size):
            if pool[poolid].is_alive():
                logger.debug("Terminating PoolThread#%d..." % poolid);
                pool[poolid].running = False;
        if not args.blocking_io or args.blocking_timeout > 0:
            for poolid in range(args.pool_size):
                if pool[poolid].is_alive():
                    logger.debug("Waiting PoolThread#%d..." % poolid);
                    pool[poolid].join();
        logger.info("Ended.");

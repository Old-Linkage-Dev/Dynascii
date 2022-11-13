#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import threading;
import logging;

logger = logging.getLogger("dynascii").getChild(__name__);

def Shell(iplimit : int = 8, shell_reject : str = "dynamic.shell.contrib.rejshell", shell_accept : str = "dynamic.shell.nullshell", *args, **kwargs):

    logger.debug("Initing IP Limit Wrapper Shell...");
    ip_pool = {};
    ip_pool_lock = threading.Lock();
    iplimit = int(iplimit);
    logger.debug("Importing accept shell and reject shell for IP Limit Wrapper Shell...");
    shell_accept = __import__(shell_accept, fromlist = ["Shell"]).Shell(**kwargs);
    shell_reject = __import__(shell_reject, fromlist = ["Shell"]).Shell(**kwargs);

    def run(conn, addr):
        logger.info("Running ip limit wrapper shell...");
        ip = addr[0];
        n = 0;
        with ip_pool_lock:
            if ip in ip_pool:
                ip_pool[ip] += 1;
            else:
                ip_pool[ip] = 1;
            n = ip_pool[ip];
        logger.debug("IP %s simultaneously link %d." % (addr[0], n));
        if (n <= iplimit):
            logger.info("User new @%s:%d." % addr[:2]);
            shell_accept(conn, addr);
            logger.info("User ended @%s:%d." % addr[:2]);
        else:
            logger.info("Request flood in @%s:%d." % addr[:2]);
            shell_reject(conn, addr);
            conn.close();
            logger.info("Request rejected in @%s:%d." % addr[:2]);
        with ip_pool_lock:
            if ip in ip_pool:
                ip_pool[ip] -= 1;
                if ip_pool[ip] == 0:
                    ip_pool.pop(ip);

    for arg in args:
        logger.debug("Unrecognized arg : %s." % arg);
    for key in kwargs:
        logger.debug("Unrecognized arg : %s : %s." % (key, kwargs[key]));
    logger.debug("Inited IP Limit Wrapper Shell.");
    return run;
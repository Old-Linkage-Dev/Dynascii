#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import logging;

logger = logging.getLogger("dynascii").getChild(__name__);

def Shell(*args, **kwargs):
    
    logger.debug("Initing Null Shell...");
    def run(conn, addr) -> None:
        logger.info("Running null shell...");

    for arg in args:
        logger.warning("Unrecognized arg : %s." % arg);
    for key in kwargs:
        logger.warning("Unrecognized arg : %s : %s." % (key, kwargs[key]));
    logger.debug("Inited Null Shell.");
    return run;

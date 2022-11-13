#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import logging;
from .. import lineshell as _ls;

logger = logging.getLogger("dynascii").getChild(__name__);

def Shell(line = None, *args, **kwargs):

    logger.debug("Initing Reject Shell...");
    _lines = [line] if line else [
        "非常抱歉，想来玩的人太多了，您可能要等一等了。",
        "It is of my most sorrow that there are too many visit. It may require a wait for it to be available.",
    ];

    for arg in args:
        logger.debug("Unrecognized arg : %s." % arg);
    for key in kwargs:
        logger.debug("Unrecognized arg : %s : %s." % (key, kwargs[key]));

    _run = _ls.Shell(lines = _lines);
    logger.debug("Inited Reject Shell.");

    return _run;

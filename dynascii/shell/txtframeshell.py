#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import time;
import logging;
import traceback;

logger = logging.getLogger("dynascii").getChild(__name__);

def Shell(txtframefile : str, interval : float = 0.125, *args, **kwargs):

    interval = float(interval);
    try:
        with open(txtframefile, mode = "r") as _fp:
            lines = _fp.readlines();
    except Exception as err:
        logger.error(err);
        logger.debug(traceback.format_exc());
        logger.critical("Shell init failed.");
        return lambda conn, addr : logger.info("No frame to play.");

    def run(conn, addr) -> None:
        logger.info("Running text frame shell...");
        try:
            _sends = b"\x1Bc\x1B[H";
            _t = time.time();
            _f = 0;
            logger.info("Frame play to start.");
            for line in lines:
                if line == "$FRAME_END$\n":
                    _f += 1;
                    while time.time() - _t < _f * interval:
                        time.sleep(0.01);
                    conn.send(_sends);
                    _sends = b"\x1Bc\x1B[H";
                    if _f % 200 == 0:
                        logger.info("Frame played #%d." % _f);
                else:
                    _sends += line[:-1].encode("utf8") + b"\r\n";
            logger.info("Frame play ended.");
        except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError) as err:
            logger.info("User connection aborted.");
        except Exception as err:
            logger.error(err);
            logger.debug(traceback.format_exc());
            logger.critical("Shell failed.");

        logger.info("User ended.");
        return;
    
    for arg in args:
        logger.warning("Unrecognized arg : %s." % arg);
    for key in kwargs:
        logger.warning("Unrecognized arg : %s : %s." % (key, kwargs[key]));
    return run;

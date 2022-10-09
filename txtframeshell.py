#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import time;
import socket;
import logging;
import traceback;

logger = logging.getLogger("dynascii").getChild(__name__);

def Shell(txtframefile : str, interval : float = 0.125, *args, **kwargs):

    interval = float(interval);

    def run(conn, addr) -> None:
        logger.info('Running text frame shell...');
        try:
            with open(txtframefile, mode = 'r') as _fp:
                _sends = b'\x1Bc\x1B[H';
                _t = time.time();
                _f = 0;
                logger.info('Frame play to start.');
                for line in _fp.readlines():
                    if line == '$FRAME_END$\n':
                        _f += 1;
                        while time.time() - _t < _f * interval:
                            time.sleep(0.01);
                        conn.send(_sends);
                        _sends = b'\x1Bc\x1B[H';
                        if _f % 200 == 0:
                            logger.info('Frame play #%d' % _f);
                    else:
                        _sends += line[:-1].encode('utf8') + b'\r\n';
                logger.info('Frame play ended.');
            conn.shutdown(socket.SHUT_RDWR);
            conn.close();
        except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError) as err:
            conn.close();
            logger.info('User connection aborted.');
        except Exception as err:
            conn.close();
            logger.error(err);
            logger.debug(traceback.format_exc());
            logger.critical('Shell failed.');
        logger.info('User ended.');
        return;
    
    for arg in args:
        logger.warning('Unrecognized arg : %s' % arg);
    for key in kwargs:
        logger.warning("Unrecognized arg : %s : %s" % (key, kwargs[key]));
    return run;

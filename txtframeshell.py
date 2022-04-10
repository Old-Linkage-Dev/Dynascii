#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import time;
import socket;
import threading;
import logging;
import traceback;

_logger_formatter_scrn = logging.Formatter(fmt='\033[0m%(asctime)s \033[1;34m[%(levelname)s]\033[0;33m >> [%(threadName)s] >> \033[0m%(message)s', datefmt='%H:%M');
_logger_ch_scrn = logging.StreamHandler();
_logger_ch_scrn.setLevel(logging.INFO);
_logger_ch_scrn.setFormatter(_logger_formatter_scrn);

logger = logging.getLogger("dynascii").getChild(__name__);
logger.addHandler(_logger_ch_scrn);



class Shell(threading.Thread):

    def __init__(self, conn, txtframefile, interval = 0.125, *args, **kwargs) -> None:
        super().__init__();
        self.name = 'TXTFrameShell(%s)' % hex(id(self));
        self.conn = conn;
        self.txtframefile = str(txtframefile);
        self.interval = float(interval);
        return;

    def run(self) -> None:
        logger.info('Running text frame shell...');
        try:
            with open(self.txtframefile, mode = 'r') as _fp:
                _sends = b'\x1Bc\x1B[H';
                _t = time.time();
                _f = 0;
                logger.info('Frame play to start.');
                for line in _fp.readlines():
                    if line == '$FRAME_END$\n':
                        _f += 1;
                        while time.time() - _t < _f * self.interval:
                            time.sleep(0.01);
                        self.conn.send(_sends);
                        _sends = b'\x1Bc\x1B[H';
                        if _f % 200 == 0:
                            logger.info('Frame play #%d' % _f);
                    else:
                        _sends += line[:-1].encode('utf8') + b'\r\n';
                logger.info('Frame play ended.');
            self.conn.shutdown(socket.SHUT_RDWR);
            time.sleep(2);
        except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError) as err:
            self.conn.close();
            logger.info('User connection aborted.');
        except Exception as err:
            self.conn.close();
            logger.error(err);
            logger.debug(traceback.format_exc());
            logger.critical('Shell failed.');
        logger.info('User ended.');
        return;

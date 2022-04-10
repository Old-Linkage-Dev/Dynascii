#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import socket;
import threading;
import traceback;
import time;

class Shell(threading.Thread):

    def __init__(self, conn, logger, txtframefile, interval = 0.125) -> None:
        super().__init__();
        self.name = '%s.%s' % (__name__, hex(id(self)));
        self.conn = conn;
        self.logger = logger;
        self.txtframefile = str(txtframefile);
        self.interval = float(interval);
        return;

    def run(self) -> None:
        self.logger.info('[%s] >> Running text frame shell...' % self.name);
        try:
            with open(self.txtframefile, mode = 'r') as _fp:
                _sends = b'\x1Bc\x1B[H';
                _t = time.time();
                _f = 0;
                _l = 0;
                for line in _fp.readlines():
                    if line == '$FRAME_END$\n':
                        _f += 1;
                        while time.time() - _t < _f * self.interval:
                            time.sleep(0.01);
                        self.conn.send(_sends);
                        _sends = b'\x1Bc\x1B[H';
                        _l = 0;
                    else:
                        _sends += line[:-1].encode('utf8') + b'\r\n';
            self.conn.shutdown(socket.SHUT_RDWR);
            time.sleep(2);
        except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError) as err:
            self.conn.close();
            self.logger.info('[%s] >> User connection aborted.' % self.name);
        except Exception as err:
            self.conn.close();
            self.logger.error(err);
            self.logger.debug(traceback.format_exc());
            self.logger.critical('[%s] >> Shell failed.' % self.name);
        self.logger.info('[%s] >> User ended.' % self.name);
        return;

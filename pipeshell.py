#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import socket;
import subprocess;
import threading;
import traceback;

class Shell(threading.Thread):

    def __init__(self, conn, logger, pipeshell) -> None:
        super().__init__();
        self.name = '%s.%s' % (__name__, hex(id(self)));
        self.conn = conn;
        self.logger = logger;
        self.pipeshell = pipeshell;
        return;

    def run(self) -> None:
        self.logger.info('[%s] >> Running pipe shell...' % self.name);
        try:
            _proc = subprocess.Popen(
                self.pipeshell,
                stdin = subprocess.DEVNULL,
                stdout = subprocess.PIPE,
                stderr = subprocess.DEVNULL,
                shell=True
            );
            _pipe = _proc.stdout;
        except Exception as err:
            self.conn.close();
            _proc = None;
            _pipe = None;
            self.logger.debug(err);
            self.logger.debug(traceback.format_exc());
            self.logger.critical('[%s] >> Shell start failed.' % self.name);
            return;
        try:
            _chrs = b'\x00';
            #self.conn.send(b'\033[0;33m');
            while _proc.poll() == None and _chrs != b'':
                _chrs = _pipe.read(1);
                self.conn.send(_chrs);
            self.conn.shutdown(socket.SHUT_RDWR);
            _pipe.close();
            _proc.kill();
        except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError) as err:
            self.conn.close();
            _pipe.close();
            _proc.kill();
            self.logger.info('[%s] >> User connection aborted.' % self.name);
        except Exception as err:
            self.conn.close();
            _pipe.close();
            _proc.kill();
            self.logger.error(err);
            self.logger.debug(traceback.format_exc());
            self.logger.critical('[%s] >> Shell failed.' % self.name);
        self.logger.info('[%s] >> User ended.' % self.name);
        return;

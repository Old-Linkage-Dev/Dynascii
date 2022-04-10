#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import socket;
import subprocess;
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

    def __init__(self, conn, logger, pipeshell) -> None:
        super().__init__();
        self.name = '%s.%s' % (__name__, hex(id(self)));
        self.conn = conn;
        self.pipeshell = pipeshell;
        return;

    def run(self) -> None:
        logger.info('Running pipe shell...');
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
            logger.debug(err);
            logger.debug(traceback.format_exc());
            logger.critical('Shell start failed.');
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
            logger.info('User connection aborted.');
        except Exception as err:
            self.conn.close();
            _pipe.close();
            _proc.kill();
            logger.error(err);
            logger.debug(traceback.format_exc());
            logger.critical('Shell failed.');
        logger.info('User ended.');
        return;

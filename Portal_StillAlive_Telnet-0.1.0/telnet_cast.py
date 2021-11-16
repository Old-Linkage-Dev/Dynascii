#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

LOG_FILE = './telnet_cast.log';

HOST = '127.0.0.1';
PORT = 23;
#PORT = 6023;

BACKLOG = 16;

SHELL = 'python ./still_alive_credit_fortelnet.py';




# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# The copyright for song <Still Alive> belongs to Jonathan Coulton and Valve Software
# The copyright for code <still_alive_credit.py> belongs to LHF (BD4SUP)
# Contact me if there's copyright violation and if deletion of the content is needed.
#
#
#
# telnet_cast.py by Tarcadia
# November 2021
#


import socket;
import subprocess;
import threading;
import logging;
import traceback;

logger = logging.getLogger(__name__);
logger.setLevel(logging.DEBUG);

_logger_formatter_scrn = logging.Formatter(fmt='\033[0m%(asctime)s \033[1;34m[%(levelname)s]\033[0;33m >> \033[0m%(message)s', datefmt='%H:%M');
_logger_ch_scrn = logging.StreamHandler();
_logger_ch_scrn.setLevel(logging.INFO);
_logger_ch_scrn.setFormatter(_logger_formatter_scrn);

_logger_formatter_file = logging.Formatter(fmt='[%(asctime)s][%(levelname)s] >> %(message)s', datefmt='%Y-%m-%d-%H:%M:%S');
_logger_ch_file = logging.FileHandler(LOG_FILE, encoding = 'utf8');
_logger_ch_file.setLevel(logging.DEBUG);
_logger_ch_file.setFormatter(_logger_formatter_file);

logger.addHandler(_logger_ch_scrn);
logger.addHandler(_logger_ch_file);

logger.info('Running...');



class shell(threading.Thread):

    def __init__(self, shell, conn) -> None:
        super().__init__();
        self.shell = shell;
        self.conn = conn;
        return;

    def run(self) -> None:
        logger.info('User [%s] running...' % hex(id(self)));
        _conn = self.conn;
        try:
            _proc = subprocess.Popen(
                self.shell,
                stdin = subprocess.DEVNULL,
                stdout = subprocess.PIPE,
                stderr = subprocess.DEVNULL,
                shell=True
            );
            _pipe = _proc.stdout;
        except Exception as err:
            _conn.close();
            _proc = None;
            _pipe = None;
            logger.debug(err);
            logger.debug(traceback.format_exc());
            logger.critical('Shell start failed.');
            return;
        try:
            _chrs = b'\x00';
            _conn.send(b'\033[0;33m');
            while _proc.poll() == None and _chrs != b'':
                _chrs = _pipe.read(1);
                _conn.send(_chrs);
            _conn.shutdown(socket.SHUT_RDWR);
            _pipe.close();
            _proc.kill();
        except BrokenPipeError or ConnectionAbortedError or ConnectionResetError as err:
            _conn.close();
            _pipe.close();
            _proc.kill();
            logger.info('User %s connection aborted.' % hex(id(self)));
        except Exception as err:
            _conn.close();
            _pipe.close();
            _proc.kill();
            logger.error(err);
            logger.debug(traceback.format_exc());
            logger.critical('Shell failed.');
        logger.info('User %s ended.' % hex(id(self)));
        return;



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
server.bind((HOST, PORT));
server.listen(BACKLOG);
server.setblocking(False);

while True:
    try:
        conn, addr = server.accept();
        user = shell(shell = SHELL, conn = conn);
        logger.info('User new [%s] @%s:%d.' % (hex(id(user)), *addr));
        user.start();
    except BlockingIOError:
        continue;
    except Exception as err:
        logger.error(err);
        logger.debug(traceback.format_exc());
        logger.critical('Main Loop run into an exception.');
        break;


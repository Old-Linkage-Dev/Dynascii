#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

LOG_FILE = './telnet_cast.log';

HOST = '127.0.0.1'
#PORT = 23;
PORT = 6024;

BACKLOG = 16;

interval = 0.125;




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
# The copyright for song <Bad Apple> belongs to Zun
# The copyright for song <Bad Apple!! feat.nomico> belongs to Alstroemeria Records
# The copyright for MV <Bad Apple> belongs to Μμ
# Contact me if there's copyright violation and if deletion of the content is needed.
#
#
#
# telnet_cast.py by Tarcadia
# November 2021
# Application can be found on telnet://dynascii.tarcadia.site:6024


import socket;
import threading;
import logging;
import traceback;
import time;

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

    def __init__(self, conn, addr) -> None:
        super().__init__();
        self.conn = conn;
        self.addr = addr;
        return;

    def run(self) -> None:
        logger.info('User [%s] running...' % hex(id(self)));
        _conn = self.conn;
        _addr = self.addr;
        try:
            with open('badapple.txt', mode = 'r') as _fp:
                _sends = b'\x1Bc\x1B[H';
                _t = time.time();
                _f = 0;
                _l = 0;
                for line in _fp.readlines():
                    if line == '$FRAME_END$\n':
                        _f += 1;
                        while time.time() - _t < _f * interval:
                            time.sleep(0.01);
                        _conn.send(_sends);
                        _sends = b'\x1Bc\x1B[H';
                        _l = 0;
                    else:
                        _sends += line[:-1].encode('ascii') + b'\r\n';
            _conn.shutdown(socket.SHUT_RDWR);
            time.sleep(2);
        except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError) as err:
            _conn.close();
            logger.info('User %s connection aborted.' % hex(id(self)));
        except Exception as err:
            _conn.close();
            logger.error(err);
            logger.debug(traceback.format_exc());
            logger.critical('Shell failed.');
        logger.info('User %s ended.' % hex(id(self)));
        return;



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
server.bind((HOST, PORT));
server.listen(BACKLOG);
server.setblocking(True);

while True:
    try:
        conn, addr = server.accept();
        user = shell(conn = conn, addr = addr);
        logger.info('User new [%s] @%s:%d.' % (hex(id(user)), *addr));
        user.start();
    except BlockingIOError:
        continue;
    except Exception as err:
        logger.error(err);
        logger.debug(traceback.format_exc());
        logger.critical('Main Loop run into an exception.');
        break;



import threading;
import logging;
import traceback;

_logger_formatter_scrn = logging.Formatter(fmt='\033[0m%(asctime)s \033[1;34m[%(levelname)s]\033[0;33m >> \033[0;31m[%(threadName)s]\033[0;33m >> \033[0m%(message)s', datefmt='%H:%M');
_logger_ch_scrn = logging.StreamHandler();
_logger_ch_scrn.setLevel(logging.INFO);
_logger_ch_scrn.setFormatter(_logger_formatter_scrn);

logger = logging.getLogger("dynascii").getChild("pool");
logger.addHandler(_logger_ch_scrn);



class PoolThread(threading.Thread):

    ippool = {};
    ippool_lock = threading.Lock();

    def __init__(self, poolid, server, Shell, kwargs_shell, iplimit = 8, *args, **kwargs):
        super().__init__();
        self.running = True;
        self.poolid = poolid;
        self.server = server;
        self.Shell = Shell;
        self.kwargs_shell =  kwargs_shell;
        self.iplimit = int(iplimit);
        self.name = 'PoolThread#%d(%s)' % (self.poolid, hex(id(self)));
        self.setDaemon(True);
    
    def run(self):
        while self.running:
            try:
                conn, addr = self.server.accept();
                ip = addr[0];
                n = 0;
                with PoolThread.ippool_lock:
                    if ip in PoolThread.ippool:
                        PoolThread.ippool[ip] += 1;
                    else:
                        PoolThread.ippool[ip] = 1;
                    n = PoolThread.ippool[ip];
                if (n <= self.iplimit):
                    user = self.Shell(conn = conn, **self.kwargs_shell);
                    user.setDaemon(False);
                    logger.info('User new [%s] @%s:%d.' % (user.name, *addr[:2]));
                    user.start();
                    user.join();
                else:
                    logger.info('Request flood in @%s:%d.' % addr[:2]);
                    conn.send(b'\x1Bc\x1B[H');
                    conn.send('It is my sorrow that this program detected some flood in request from this IP.\r\n'.encode("utf8"));
                    conn.send('It may be a wrong detection but I have to block you outside.\r\n'.encode("utf8"));
                    conn.send('You may visit later and that may help.\r\n'.encode("utf8"));
                    conn.close();
                with PoolThread.ippool_lock:
                    if ip in PoolThread.ippool:
                        PoolThread.ippool[ip] -= 1;
                        if PoolThread.ippool[ip] == 0:
                            PoolThread.ippool.pop(ip);
            except BlockingIOError:
                continue;
            except Exception as err:
                logger.error(err);
                logger.debug(traceback.format_exc());
                logger.critical('Run into an exception.');
                break;
        logger.info('Ended.');

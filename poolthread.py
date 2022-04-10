
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
    iplimit = 8;
    ippool_lock = threading.Lock();

    def __init__(self, poolid, server, Shell, *args, **kwargs):
        super().__init__();
        self.running = True;
        self.poolid = poolid;
        self.server = server;
        self.Shell = Shell;
        self.kwargs = kwargs;
        self.name = 'PoolThread#%d(%s)' % (self.poolid, hex(id(self)));
    
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
                if (n <= PoolThread.iplimit):
                    user = self.Shell(conn = conn, **self.kwargs);
                    logger.info('User new [%s] @%s:%d.' % (user.name, *addr));
                    user.start();
                    user.join();
                else:
                    logger.info('Request flood in @%s:%d.' % addr);
                    conn.send(b'\x1Bc\x1B[H');
                    conn.send("非常抱歉，想来玩的人太多了，您可能要等一等了。\r\n".encode("utf8"));
                    conn.send("It is of my most sorrow that there are too many visit. It may require a wait for it to be available.\r\n".encode("utf8"));
                    ##conn.send("It is of my most sorrow that there are too many visit. It may require a wait for it to be available.\n".encode("utf8"));
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


import threading;
import logging;

_logger_formatter_scrn = logging.Formatter(fmt='\033[0m%(asctime)s \033[1;34m[%(levelname)s]\033[0;33m >> \033[0;31m[%(threadName)s]\033[0;33m >> \033[0m%(message)s', datefmt='%H:%M');
_logger_ch_scrn = logging.StreamHandler();
_logger_ch_scrn.setLevel(logging.INFO);
_logger_ch_scrn.setFormatter(_logger_formatter_scrn);

logger = logging.getLogger("dynascii").getChild("pool");
logger.addHandler(_logger_ch_scrn);



def IplimitWrapperShell(iplimit : int = 8, shell_reject : str = "rejshell", shell_accept : str = "nullshell", *args, **kwargs):

    ip_pool = {};
    ip_pool_lock = threading.Lock();
    shell_accept = __import__(shell_accept).Shell(**kwargs);
    shell_reject = __import__(shell_reject).Shell(**kwargs);

    def run(conn, addr):
        ip = addr[0];
        n = 0;
        with ip_pool_lock:
            if ip in ip_pool:
                ip_pool[ip] += 1;
            else:
                ip_pool[ip] = 1;
            n = ip_pool[ip];
        if (n <= iplimit):
            logger.info('User new @%s:%d.' % addr[:2]);
            shell_accept(conn, addr);
            conn.close();
        else:
            logger.info('Request flood in @%s:%d.' % addr[:2]);
            shell_reject(conn, addr);
            conn.close();
        with ip_pool_lock:
            if ip in ip_pool:
                ip_pool[ip] -= 1;
                if ip_pool[ip] == 0:
                    ip_pool.pop(ip);

    return run;
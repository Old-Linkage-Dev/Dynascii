
import threading;
import logging;

logger = logging.getLogger("dynascii").getChild(__name__);

def Shell(iplimit : int = 8, shell_reject : str = "rejshell", shell_accept : str = "nullshell", *args, **kwargs):

    ip_pool = {};
    ip_pool_lock = threading.Lock();
    iplimit = int(iplimit);
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

    for arg in args:
        logger.warning('Unrecognized arg : %s' % arg);
    for key in kwargs:
        logger.warning("Unrecognized arg : %s : %s" % (key, kwargs[key]));
    return run;
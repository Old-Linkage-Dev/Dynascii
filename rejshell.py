
import logging;

_logger_formatter_scrn = logging.Formatter(fmt='\033[0m%(asctime)s \033[1;34m[%(levelname)s]\033[0;33m >> [%(threadName)s] >> \033[0m%(message)s', datefmt='%H:%M');
_logger_ch_scrn = logging.StreamHandler();
_logger_ch_scrn.setLevel(logging.INFO);
_logger_ch_scrn.setFormatter(_logger_formatter_scrn);

logger = logging.getLogger("dynascii").getChild(__name__);
logger.addHandler(_logger_ch_scrn);



def Shell(*args, **kwargs):

    def run(conn, addr) -> None:
        logger.info("Rejecting...");
        conn.send(b'\x1Bc\x1B[H');
        conn.send("非常抱歉，想来玩的人太多了，您可能要等一等了。\r\n".encode("utf8"));
        conn.send("It is of my most sorrow that there are too many visit. It may require a wait for it to be available.\r\n".encode("utf8"));
        ##conn.send("It is of my most sorrow that there are too many visit. It may require a wait for it to be available.\n".encode("utf8"));
        conn.close();

    for arg in args:
        logger.debug('Unrecognized arg : %s' % arg);
    for key in kwargs:
        logger.debug("Unrecognized arg : %s : %s" % (key, kwargs[key]));
    return run;

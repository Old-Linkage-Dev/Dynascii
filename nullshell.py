
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
    
    def __init__(self, conn, *args, **kargs) -> None:
        super().__init__();
        self.name = "NullShell(%s)" % hex(id(self));
        self.conn = conn;
        return;

    def run(self) -> None:
        logger.info("Running null shell...");
        self.conn.close();

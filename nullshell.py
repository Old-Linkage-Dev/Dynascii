
import threading;

class Shell(threading.Thread):
    
    def __init__(self, conn, logger, *args, **kargs) -> None:
        super().__init__();
        self.name = '[%s.%s]' % (__name__, hex(id(self)));
        self.conn = conn;
        self.logger = logger;
        return;

    def run(self) -> None:
        self.logger.info('[%s] >> Running null shell...' % hex(id(self)));
        self.conn.close();

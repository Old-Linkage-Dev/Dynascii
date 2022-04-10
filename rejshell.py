
import threading;

class Shell(threading.Thread):
    
    def __init__(self, conn, logger) -> None:
        super().__init__();
        self.name = '[%s.%s]' % (__name__, hex(id(self)));
        self.conn = conn;
        self.logger = logger;
        return;

    def run(self) -> None:
        self.logger.info('[%s] >> Rejecting...' % hex(id(self)));
        self.conn.send(b'\x1Bc\x1B[H');
        self.conn.send("非常抱歉，想来玩的人太多了，您可能要等一等了。\r\n".encode("utf8"));
        self.conn.send("It is of my most sorrow that there are too many visit. It may require a wait for it to be available.\r\n".encode("utf8"));
        ##self.conn.send("It is of my most sorrow that there are too many visit. It may require a wait for it to be available.\n".encode("utf8"));
        self.conn.close();

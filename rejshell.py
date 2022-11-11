
import logging;

logger = logging.getLogger("dynascii").getChild(__name__);

def Shell(line = None, *args, **kwargs):

    logger.debug("Initing Reject Shell...");
    lines = [line] if line else [
        "非常抱歉，想来玩的人太多了，您可能要等一等了。",
        "It is of my most sorrow that there are too many visit. It may require a wait for it to be available.",
    ];
    def run(conn, addr) -> None:
        logger.info("Rejecting...");
        conn.send(b'\x1Bc\x1B[H');
        for line in lines:
            logger.info("Sending: %s" % line);
            conn.send((line+"\n\r").encode("utf8"));
        ##conn.send("It is of my most sorrow that there are too many visit. It may require a wait for it to be available.\n".encode("utf8"));

    for arg in args:
        logger.debug('Unrecognized arg : %s' % arg);
    for key in kwargs:
        logger.debug("Unrecognized arg : %s : %s" % (key, kwargs[key]));
    logger.debug("Inited Reject Shell.");
    return run;

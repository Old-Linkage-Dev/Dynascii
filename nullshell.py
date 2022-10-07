
import logging;

logger = logging.getLogger("dynascii").getChild(__name__);

def Shell(*args, **kwargs):
    
    def run(conn, addr) -> None:
        logger.info("Running null shell...");
        conn.close();

    for arg in args:
        logger.warning('Unrecognized arg : %s' % arg);
    for key in kwargs:
        logger.warning("Unrecognized arg : %s : %s" % (key, kwargs[key]));
    return run;

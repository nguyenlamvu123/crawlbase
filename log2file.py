import logging
##from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler
from logging import Formatter


def begi(logfilename: str):
    ##logging.basicConfig(filename = 'example.log', xlevel=logging.DEBUG)
    formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('RotatingFileHandler')

    # Split log at 0h everyday
##    handler = TimedRotatingFileHandler(logfilename, when="midnight", interval=1)
    handler = RotatingFileHandler(logfilename, maxBytes=20, backupCount=10)
    handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    ##logger.basicConfig(filename='log_filename.log', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    ##logger.debug('This is a debug log message.')
    ##logger.info('This is a info log message.')
    ##logger.warning('This is a warning log message.')
    ##logger.error('This is a error log message.')
    ##logger.critical('This is a critical log message.')
    return logger


def priiiiiint(noidung, logger=None):
    print(noidung)
    if logger is not None:
        logger.debug(str(noidung))


if __name__ == '__main__':
    for i in range(5):
        priiiiiint(i)
    input()
    for i in range(5):
        priiiiiint(i)

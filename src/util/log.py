import logging
import os

from src.const.constants import PATH_LOG, PRINTING_LEVEL


class Logger(object):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    
    __main_logger = logging.getLogger('tripmaker')
    __hdlr = logging.FileHandler(os.path.join(PATH_LOG, "main.log"))
    __hdlr.setFormatter(formatter)
    __main_logger.addHandler(__hdlr)
    __main_logger.setLevel(logging.DEBUG)

    @staticmethod
    def debug(message):
        Logger.__main_logger.debug(message)
        if PRINTING_LEVEL <= 2:
            print(message)

    @staticmethod
    def info(message):
        Logger.__main_logger.info(message)
        if PRINTING_LEVEL <= 3:
            print(message)

    @staticmethod
    def error(message):
        Logger.__main_logger.error(message)
        if PRINTING_LEVEL <= 4:
            print(message)

    @staticmethod
    def system(message):
        Logger.__main_logger.fatal(message)
        if PRINTING_LEVEL <= 5:
            print(message)

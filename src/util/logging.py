import logging
import os

from src.const.constants import PATH_DATA_LOG


class Logger(object):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    
    __main_logger = logging.getLogger('tripmaker')
    __hdlr = logging.FileHandler(os.path.join(PATH_DATA_LOG, "main.log"))
    __hdlr.setFormatter(formatter)
    __main_logger.addHandler(__hdlr)
    __main_logger.setLevel(logging.DEBUG)

    @staticmethod
    def debug(message):
        Logger.__main_logger.debug(message)

    @staticmethod
    def info(message):
        Logger.__main_logger.info(message)
        print(message)

    @staticmethod
    def error(message):
        Logger.__main_logger.error(message)
        print(message)

    @staticmethod
    def system(message):
        Logger.__main_logger.fatal(message)
        print(message)

import logging
import os
from datetime import datetime

from src.const.constants import PATH_LOG, PRINTING_LEVEL, PRINT_ROUTES_TO_CONSOLE, DATE_TIME_FORMAT


class Logger(object):
    # @staticmethod
    # def crunch_logs(default_path):
    #     postfix = "logs_{}".format(datetime.strftime(datetime.now(), DATE_TIME_FORMAT))
    #     path = os.path.join(default_path, postfix)
    #     path_graphs = os.path.join(default_path, 'graphs')
    #     path_maps = os.path.join(default_path, 'maps')
    #     if not os.path.exists(path_graphs):
    #         os.makedirs(directory)'graphs'

    @staticmethod
    def crunch_logs(file_name):
        Logger.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        Logger.__main_logger = logging.getLogger('tripmaker')

        Logger.__hdlr = logging.FileHandler(os.path.join(PATH_LOG, file_name))
        Logger.__hdlr.setFormatter(Logger.formatter)

        Logger.__main_logger.addHandler(Logger.__hdlr)
        Logger.__main_logger.setLevel(logging.DEBUG)

    date = datetime.strftime(datetime.now(), DATE_TIME_FORMAT)
    main_name = "main_{}.log".format(date)
    separate_name = "separate_{}.log".format(date)

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    __main_logger = logging.getLogger('tripmaker')
    __hdlr = logging.FileHandler(os.path.join(PATH_LOG, main_name))
    __hdlr.setFormatter(formatter)
    __main_logger.addHandler(__hdlr)
    __main_logger.setLevel(logging.DEBUG)

    separate_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    __separate_logger = logging.getLogger('tripmaker_separate')
    __separate_hdlr = logging.FileHandler(os.path.join(PATH_LOG, separate_name))
    __separate_hdlr.setFormatter(separate_formatter)
    __separate_logger.addHandler(__hdlr)
    __separate_logger.setLevel(logging.DEBUG)

    # formatter = None
    # __main_logger = None
    # __hdlr = None

    @staticmethod
    def debug(message, is_separate=False):
        if is_separate:  # FIXME refactor this 'separate' shit!
            Logger.__separate_logger.debug(message)
        Logger.__main_logger.debug(message)
        if PRINTING_LEVEL <= 2:
            print(message)

    @staticmethod
    def info(message, is_separate=False, is_route=False):
        if is_separate:
            Logger.__separate_logger.info(message)
        Logger.__main_logger.info(message)
        if PRINTING_LEVEL <= 3:
            if is_route:
                if not PRINT_ROUTES_TO_CONSOLE:
                    return
            print(message)

    @staticmethod
    def error(message, is_separate=False):
        if is_separate:
            Logger.__separate_logger.error(message)
        Logger.__main_logger.error(message)
        if PRINTING_LEVEL <= 4:
            print(message)

    @staticmethod
    def system(message):
        Logger.__main_logger.fatal(message)
        if PRINTING_LEVEL <= 5:
            print(message)

Logger.info("Configured logger; main file name: {}; separate file name: {}".format(Logger.main_name,
                                                                                   Logger.separate_name))

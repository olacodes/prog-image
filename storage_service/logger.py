import logging
import sys
from logging.handlers import TimedRotatingFileHandler

FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE = "storage_service/logs/storage_service.log"


class Logger:
    def __init__(self, logger_name, log_file=LOG_FILE, formatter=FORMATTER):
        self.logger_name = logger_name
        self.log_file = log_file
        self.formatter = formatter

    def console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        return console_handler

    def file_handler(self):
        file_handler = TimedRotatingFileHandler(self.log_file, when='midnight')
        file_handler.setFormatter(self.formatter)
        return file_handler

    def log(self):
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.console_handler())
        logger.addHandler(self.file_handler())
        logger.propagate = False
        return logger

# Copilot prompt: "write me a logger class which logs in the following format: log type (error, info), timestamp, service, method name, log message"
import logging
import sys

class SimLogger:
    def __init__(self, log_file):
        self.logger = logging.getLogger(self.__class__.__name__)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter('%(levelname)10s | %(asctime)s | %(message)s'))
        self.logger.addHandler(file_handler)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter('%(levelname)10s | %(asctime)s | %(message)s'))
        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.DEBUG)

    def log_error(self, message):
        self.logger.error(message)

    def log_info(self, message):
        self.logger.info(message)

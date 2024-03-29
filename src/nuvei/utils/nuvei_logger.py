# Copilot prompt: "write me a logger class which logs in the following format: log type (error, info), timestamp, service, method name, log message"


import logging
import sys

class NuveiLogger:
    def __init__(self, log_file):
        self.logger = logging.getLogger(self.__class__.__name__)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter('%(levelname)10s | %(asctime)s | %(service)20s | %(method_name)30s | %(transaction_id)36s | %(message)s'))
        self.logger.addHandler(file_handler)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter('%(levelname)10s | %(asctime)s | %(service)20s | %(method_name)30s | %(transaction_id)36s | %(message)s'))
        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.DEBUG)

    def log_error(self, service, method_name, transaction_id, message):
        self.logger.error(message, extra={'service': service, 'method_name': method_name, 'transaction_id': transaction_id})

    def log_info(self, service, method_name, transaction_id, message):
        self.logger.info(message, extra={'service': service, 'method_name': method_name, 'transaction_id': transaction_id})

# Usage example:

#import uuid
#logger = NuveiLogger('/Users/stefan/Work/Pyenvs/Yukinoaru/logs/file.log')
#logger.log_error('service_name', 'method_name', uuid.uuid4(), 'This is an error message')
#logger.log_info('service_name', 'method_name', uuid.uuid4(), 'This is an info message')

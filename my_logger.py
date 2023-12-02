import logging
from abc import abstractmethod


class My_log:

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s')
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler("example.log")
        console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger




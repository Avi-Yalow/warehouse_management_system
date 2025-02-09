import logging
import os


class Logger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Create file handler which logs even debug messages
        remove_log_file()
        fh = logging.FileHandler('warehouse.log')
        fh.setLevel(logging.DEBUG)

        # Create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s  - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(fh)

    def get_logger(self):
        return self.logger
    
def remove_log_file():
    if os.path.exists("warehouse.log"):
        os.remove("warehouse.log")
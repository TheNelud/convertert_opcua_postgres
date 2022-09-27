import logging
from parse_config import ParserXML


class LogginMyApp():
    def __init__(self):

        self.pXML = ParserXML().parser()
        self._log_format = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"

    def get_file_handler(self):
        self.file_handler = logging.FileHandler(self.pXML['ather_setting']['path_log_file'])
        self.file_handler.setLevel(logging.WARNING)
        self.file_handler.setFormatter(logging.Formatter(self._log_format))
        return self.file_handler

    def get_stream_handler(self):
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setLevel(logging.INFO)
        self.stream_handler.setFormatter(logging.Formatter(self._log_format))
        return self.stream_handler

    def get_logger(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.get_file_handler())
        self.logger.addHandler(self.get_stream_handler())
        return self.logger
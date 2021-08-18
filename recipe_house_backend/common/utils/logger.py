import logging


def get_logger(logger_name=None):
    if logger_name:
        return logging.getLogger(logger_name)
    return logging.getLogger("django")

# from flask import current_app
# import logging
# from source.settings import *
# from werkzeug.local import LocalProxy
# import logging.config
from logging.handlers import RotatingFileHandler


def util_logger_handler(file_name):
    return RotatingFileHandler(file_name, maxBytes=102400, delay=False,
                               encoding='UTF-8', backupCount=15)

# def log_config(file_name, level=logging.DEBUG):
#    current_app.logging.basicConfig(filename=file_name, level=level,
#                                    format='% (asctime)s % (levelname)s % (
#                                    name)s % (threadName)s: % (message)s')


# def log(data, level='info'):
#     logger = LocalProxy(lambda: current_app.logger)
#     if level == 'info':
#         logger.info(data)
#     elif level == 'debug':
#         logger.debug(data)
#     elif level == 'warning':
#         logger.warning(data)

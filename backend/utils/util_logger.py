# from flask import current_app
# import logging
# from source.settings import *
# from werkzeug.local import LocalProxy
import logging.config
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

# def setBasicLogger():
#     logging.config.dictConfig(
#         {
#             "version": 1,
#             "disable_existing_loggers": False,
#             "formatters": {
#                 "simple": {
#                     "format": "%(asctime)s - %(module)s - %(filename)s - %(funcName)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s"}
#             },
#             "handlers": {
#                 "console": {
#                     "class": "logging.StreamHandler",
#                     "level": "DEBUG",
#                     "formatter": "simple",
#                     "stream": "ext://sys.stdout",
#                 },
#                 "info_file_handler": {
#                     "class": "logging.handlers.RotatingFileHandler",
#                     "level": "INFO",
#                     "formatter": "simple",
#                     "filename": "info.log",
#                     "maxBytes": 10485760,
#                     "backupCount": 50,
#                     "encoding": "utf8",
#                 },
#                 "error_file_handler": {
#                     "class": "logging.handlers.RotatingFileHandler",
#                     "level": "ERROR",
#                     "formatter": "simple",
#                     "filename": "error.log",
#                     "maxBytes": 10485760,
#                     "backupCount": 20,
#                     "encoding": "utf8",
#                 },
#                 "debug_file_handler": {
#                     "class": "logging.handlers.RotatingFileHandler",
#                     "level": "DEBUG",
#                     "formatter": "simple",
#                     "filename": "debug.log",
#                     "maxBytes": 10485760,
#                     "backupCount": 50,
#                     "encoding": "utf8",
#                 },
#             },
#             "loggers": {
#                 "error_logger": {"level": "ERROR", "handlers": ["console", "error_file_handler"], "propagate": "no"},
#                 "info_logger": {"level": "INFO", "handlers": ["console", "info_file_handler"], "propagate": "no"},
#                 "debug_logger": {"level": "DEBUG", "handlers": ["console", "debug_file_handler"], "propagate": "no"},
#             },
#             "root": {
#                 "level": "DEBUG",
#                 "handlers": ["console", "debug_file_handler", "info_file_handler", "error_file_handler"],
#             },
#         }
#     )
import os
import sys
import multiprocessing


class BaseConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret string'

    @staticmethod
    def init_app(app):
        pass

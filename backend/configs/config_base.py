import os
# import sys


class BaseConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret string'

    # Searching Config
    SEARCH_IGNORE_CASE = True
    SEARCH_EXACT = False
    SEARCH_LIKE = True
    SEARCH_SLICE = False
    DATA_FORMAT = "dict"

    @staticmethod
    def init_app(app):
        pass

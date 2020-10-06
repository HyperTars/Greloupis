import os
from source.configs import DevConfig, TestConfig, ProdConfig

basedir = os.path.abspath(os.path.dirname(__file__))

class config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret string'
    @staticmethod
    def init_app(app):
        pass


config = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
    'default': DevConfig
}
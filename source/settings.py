from source.configs.config_dev import DevConfig
from source.configs.config_prod import ProdConfig
from source.configs.config_test import TestConfig
import os

basedir = os.path.abspath(os.path.dirname(__file__))


config = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
    'default': DevConfig
}

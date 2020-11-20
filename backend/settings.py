from configs.config_base import BaseConfig
from configs.config_dev import DevConfig
from configs.config_prod import ProdConfig
from configs.config_test import TestConfig
import os

basedir = os.path.abspath(os.path.dirname(__file__))


config = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
    'base': BaseConfig,
    'default': DevConfig
}

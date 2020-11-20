from configs.config_base import BaseConfig
from configs.config_dev import DevConfig
from configs.config_prod import ProdConfig
from configs.config_test import TestConfig
import os

basedir = os.path.abspath(os.path.dirname(__file__))
CONF = os.environ.get("CONF", "dev")

config = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
    'base': BaseConfig,
    'default': DevConfig
}

if CONF == 'test':
    config['default'] = TestConfig
elif CONF == "prod":
    config['default'] = ProdConfig

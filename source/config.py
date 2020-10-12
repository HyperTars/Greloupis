from source.configs.config_dev import *
from source.configs.config_prod import *
from source.configs.config_test import *

basedir = os.path.abspath(os.path.dirname(__file__))


config = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
    'default': DevConfig
}

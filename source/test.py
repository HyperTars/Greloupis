import unittest
from source.settings import config
# from source.tests.unit.test_models import TestModels
from source.tests.unit.test_routes import TestRoutes
from source.tests.unit.test_app import TestApp
from source.tests.unit.test_apiv1 import TestApiV1


if __name__ == '__main__':
    conf = config['test']

    # TestApp()
    # TestApiV1()
    # TestModels()
    # TestRoutes()
    # unittest.main()


"""
dev param

from source.settings import config
from source.db.mongo import *

conf = config['dev']
db = get_db(conf)
"""

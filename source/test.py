import unittest
from source.settings import config
# from source.tests.unit.test_models import TestModels
from source.tests.unit.test_routes import TestRoutes
from source.tests.unit.test_app import TestApp
from source.tests.unit.test_apiv1 import TestApiV1
from source.tests.unit.test_db import *

if __name__ == '__main__':
    conf = config['test']
    db = get_db(conf)

    TestApp()
    TestApiV1()
    # TestModels()
    TestRoutes()
    TestQueryUser()
    unittest.main()


"""
dev param

from source.settings import config
from source.db.mongo import *

conf = config['dev']
db = get_db(conf)
"""

import unittest
from source.settings import *
from source.tests.unit.test_models import TestModels


if __name__ == '__main__':
    conf = config['test']
    TestModels()
    unittest.main()

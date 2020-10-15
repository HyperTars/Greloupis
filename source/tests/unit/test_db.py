import unittest
from source.settings import *
from source.db.mongo import get_db
from source.tests.unit.test_load_data import *
from source.db.query_user import *
import random


class TestUser(unittest.TestCase):
    def setUp(self):
        self.data = util_load_test_data()

    def test_user_create(self):
        user_name = "dev_user_temp"
        user_email = "dev_temp@gmail.com"
        user_password = "dev"
        self.assertEqual(query_user_create(user_name=user_name, user_email=user_email,
                                           user_password=user_password).user_name, user_name)


class TestVideo(unittest.TestCase):
    def setUp(self):
        self.data = util_load_test_data()


class TestVideoOp(unittest.TestCase):
    def setUp(self):
        self.data = util_load_test_data()


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.data = util_load_test_data()


if __name__ == "__main__":
    db = get_db(TestConfig)
    unittest.main()

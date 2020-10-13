import unittest
from source.settings import *
from source.db.mongo import get_db
from source.db.query_user import *
from source.db.query_video import *
from source.db.query_video_op import *
from source.utils.util_load_test_data import *


class TestUser(unittest.TestCase):
    def setUp(self):
        self.data = util_load_test_data()


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

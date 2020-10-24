import unittest
from source.utils.util_hash import *
from source.utils.util_validator import *
from source.utils.util_request_filter import *


class TestUtilErrorHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass


class TestUtilHash(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_util_hash_encode(self):
        test_str = "kkk"
        self.assertEqual(util_hash_encode(test_str), util_hash_sha512(test_str))

    def test_util_md5_with_salt(self):
        test_str = "kkk"
        salt = util_hash_create_salt()
        test_encode = util_hash_md5_with_salt(test_str, salt)
        self.assertEqual(test_encode, util_hash_md5_with_salt(test_str, salt))


class TestUtilPattern(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass


class TestUtilRequestFilter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_util_request_filter_xss(self):
        util_request_filter_xss()

    def test_util_request_filter_malicious_ip(self):
        util_request_filter_malicious_ip()


class TestUtilSerializer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass


class TestUtilTime(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass


class TestValidator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_util_validator(self):
        test_id_1 = "5f88f883e6ac4f89900ac983"
        test_id_2 = "5f88f883e6ac4f89900ac98"
        self.assertEqual(is_valid_id(test_id_1), True)
        self.assertEqual(is_valid_id(test_id_2), False)


if __name__ == '__main__':
    unittest.main()

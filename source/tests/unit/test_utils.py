import unittest
from source.utils.util_hash import *
from source.utils.util_validator import *
from source.utils.util_request_filter import *
from source.utils.util_logger import *
from source.utils.util_error_handler import *
from source.utils.util_pattern import *


class TestUtilErrorHandler(unittest.TestCase):
    def test_util_error_handler_mongo_error(self):
        with self.assertRaises(MongoError) as e:
            raise MongoError(ErrorCode.MONGODB_USER_NOT_FOUND)
        self.assertEqual(util_error_handler(e.exception).status_code, 404)

        with self.assertRaises(MongoError) as e:
            raise MongoError(ErrorCode.MONGODB_STR_EXPECTED)
        self.assertEqual(util_error_handler(e.exception).status_code, 500)

    def test_util_error_handler_service_error(self):
        with self.assertRaises(ServiceError) as e:
            raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)
        self.assertEqual(util_error_handler(e.exception).status_code, 400)

    def test_util_error_handler_route_error(self):
        with self.assertRaises(RouteError) as e:
            raise RouteError(ErrorCode.ROUTE_INVALID_REQUEST_PARAM)
        self.assertEqual(util_error_handler(e.exception).status_code, 404)

    def test_util_error_handler_exception(self):
        with self.assertRaises(Exception) as e:
            raise Exception
        self.assertEqual(util_error_handler(e.exception).status_code, 500)

    def test_util_error_handler_else(self):
        with self.assertRaises(KeyError) as e:
            raise KeyError
        self.assertEqual(util_error_handler(e.exception).status_code, 503)


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


class TestUtilLogger(unittest.TestCase):

    def test_util_logger_handler(self):
        file_name = "logs.txt"
        self.assertEqual(type(handler(file_name)), RotatingFileHandler)


class TestUtilPattern(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_util_pattern_format_param(self):
        temp_str = "111"

        kw = util_pattern_format_param(service="user", _id=temp_str)
        self.assertEqual(kw['user_id'], temp_str)

        kw = util_pattern_format_param(service="user", id=temp_str)
        self.assertEqual(kw['user_id'], temp_str)

        kw = util_pattern_format_param(service="user", password=temp_str)
        self.assertEqual(kw['user_password'], temp_str)

        kw = util_pattern_format_param(service="user", email=temp_str)
        self.assertEqual(kw['user_email'], temp_str)

        kw = util_pattern_format_param(service="user", reg_date=temp_str)
        self.assertEqual(kw['user_reg_date'], temp_str)

        kw = util_pattern_format_param(service="video", _id=temp_str)
        self.assertEqual(kw['video_id'], temp_str)

        kw = util_pattern_format_param(service="video", id=temp_str)
        self.assertEqual(kw['video_id'], temp_str)

        kw = util_pattern_format_param(service="video", tag=temp_str)
        self.assertEqual(kw['video_tag'], temp_str)

        kw = util_pattern_format_param(service="video", category=temp_str)
        self.assertEqual(kw['video_category'], temp_str)

        kw = util_pattern_format_param(service="video", content=temp_str)
        self.assertEqual(kw['video_raw_content'], temp_str)

        kw = util_pattern_format_param(service="video", raw_content=temp_str)
        self.assertEqual(kw['video_raw_content'], temp_str)

        kw = util_pattern_format_param(service="video_op", id=temp_str)
        self.assertEqual(kw['video_op_id'], temp_str)

        kw = util_pattern_format_param(service="video_op", _id=temp_str)
        self.assertEqual(kw['video_op_id'], temp_str)

        kw = util_pattern_format_param(service="video_op", comment=temp_str)
        self.assertEqual(kw['video_op_comment'], temp_str)

    def test_util_test_pattern_build(self):
        test_str = "111"
        kw = util_pattern_build(user_reg_date=test_str, exact=False)
        self.assertEqual(kw['user_reg_date'], re.compile('.*' + test_str + '.*'))

        kw = util_pattern_build(video_tag=test_str, exact=False)
        self.assertEqual(kw['video_tag'], re.compile('.*' + test_str + '.*'))

        kw = util_pattern_build(video_category=test_str, exact=False)
        self.assertEqual(kw['video_category'], re.compile('.*' + test_str + '.*'))

        kw = util_pattern_build(video_op_comment=test_str, exact=False)
        self.assertEqual(kw['video_op_comment'], re.compile('.*' + test_str + '.*'))

        with self.assertRaises(UtilError) as e:
            util_pattern_build(nonsense=test_str)
        self.assertEqual(e.exception.error_code, ErrorCode.UTIL_INVALID_PATTERN_PARAM)


class TestUtilRequestFilter(unittest.TestCase):
    def test_util_request_filter_xss(self):
        util_request_filter_xss()

    def test_util_request_filter_malicious_ip(self):
        util_request_filter_malicious_ip()


class TestUtilSerializer(unittest.TestCase):
    def test_util_serializer_dict_to_json_ymd_hms(self):
        data = {"time": "2020-09-26 17:56:42"}
        js = util_serializer_dict_to_json(data)
        self.assertEqual(js, '{"time": "2020-09-26 17:56:42"}')

    def test_util_serializer_dict_to_json_ymd(self):
        data = {"time": "2020-09-26"}
        js = util_serializer_dict_to_json(data)
        self.assertEqual(js, '{"time": "2020-09-26"}')

    def test_util_serializer_dict_to_json(self):
        data = {"time": "1-2-3"}
        js = util_serializer_dict_to_json(data)
        self.assertEqual(js, '{"time": "1-2-3"}')


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

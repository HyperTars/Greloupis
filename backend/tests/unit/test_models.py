import unittest
import imp
from utils.util_tests import util_tests_python_version, \
    util_tests_load_data
from models.model_user import User
from models.model_errors import ErrorCode, MongoError, ServiceError, \
    RouteError, UtilError


class TestUserModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.data = util_tests_load_data()
        if util_tests_python_version() is False:
            exit()

    def test_user_model_load(self):
        temp_user = self.data['temp_user'][2]
        user = User(**temp_user)
        self.assertEqual(user.user_name, temp_user['user_name'])
        self.assertEqual(user.user_detail.user_first_name,
                         temp_user['user_detail']['user_first_name'])
        self.assertEqual(user.user_login[0].user_login_time,
                         temp_user['user_login'][0]['user_login_time'])
        self.assertEqual(user.user_follower, temp_user['user_follower'])


class TestErrorModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if util_tests_python_version() is False:
            exit()

    def test_error_class(self):
        imp.load_source('__main__', 'models/model_errors.py')

    def test_error_code(self):
        # ErrorCode Class
        self.assertEqual(ErrorCode.MONGODB_CONNECTION_FAILURE.get_code(), 4000)
        self.assertEqual(ErrorCode.MONGODB_CONNECTION_FAILURE.get_msg(),
                         "MongoDB Connection Failure")

    def test_mongo_error(self):
        # Raise normal MongoError successfully
        with self.assertRaises(MongoError) as e:
            raise MongoError(ErrorCode.MONGODB_USER_NOT_FOUND)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_USER_NOT_FOUND)

        # Wrong MongoError Param
        with self.assertRaises(MongoError) as e:
            MongoError(4000)
        self.assertEqual(e.exception.error_code, ErrorCode.ERR_INCORRECT_CODE)
        self.assertEqual(e.__str__(), e.__str__())

        # Get code & msg
        with self.assertRaises(MongoError) as e:
            raise MongoError(ErrorCode.MONGODB_CONNECTION_FAILURE)
        self.assertEqual(e.exception.get_code(),
                         ErrorCode.MONGODB_CONNECTION_FAILURE.get_code())
        self.assertEqual(e.exception.get_msg(),
                         ErrorCode.MONGODB_CONNECTION_FAILURE.get_msg())

    def test_service_error(self):
        # Raise normal ServiceError successfully
        with self.assertRaises(ServiceError) as e:
            raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Wrong ServiceError Param
        with self.assertRaises(ServiceError) as e:
            ServiceError(4000)
        self.assertEqual(e.exception.error_code, ErrorCode.ERR_INCORRECT_CODE)
        self.assertEqual(e.__str__(), e.__str__())

        # Get code & msg
        with self.assertRaises(ServiceError) as e:
            raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)
        self.assertEqual(e.exception.get_code(),
                         ErrorCode.SERVICE_MISSING_PARAM.get_code())
        self.assertEqual(e.exception.get_msg(),
                         ErrorCode.SERVICE_MISSING_PARAM.get_msg())

    def test_route_error(self):
        # Raise normal ServiceError successfully
        with self.assertRaises(RouteError) as e:
            raise RouteError(ErrorCode.ROUTE_INVALID_REQUEST_PARAM)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.ROUTE_INVALID_REQUEST_PARAM)

        # Wrong ServiceError Param
        with self.assertRaises(RouteError) as e:
            RouteError(4000)
        self.assertEqual(e.exception.error_code, ErrorCode.ERR_INCORRECT_CODE)
        self.assertEqual(e.__str__(), e.__str__())

        # Get code & msg
        with self.assertRaises(RouteError) as e:
            raise RouteError(ErrorCode.ROUTE_INVALID_REQUEST_PARAM)
        self.assertEqual(e.exception.get_code(),
                         ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_code())
        self.assertEqual(e.exception.get_msg(),
                         ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg())

    def test_util_error(self):
        # Raise normal ServiceError successfully
        with self.assertRaises(UtilError) as e:
            raise UtilError(ErrorCode.UTIL_INVALID_PATTERN_PARAM)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.UTIL_INVALID_PATTERN_PARAM)

        # Wrong ServiceError Param
        with self.assertRaises(UtilError) as e:
            UtilError(4000)
        self.assertEqual(e.exception.error_code, ErrorCode.ERR_INCORRECT_CODE)
        self.assertEqual(e.__str__(), e.__str__())

        # Get code & msg
        with self.assertRaises(UtilError) as e:
            raise UtilError(ErrorCode.UTIL_INVALID_PATTERN_PARAM)
        self.assertEqual(e.exception.get_code(),
                         ErrorCode.UTIL_INVALID_PATTERN_PARAM.get_code())
        self.assertEqual(e.exception.get_msg(),
                         ErrorCode.UTIL_INVALID_PATTERN_PARAM.get_msg())


"""
if __name__ == '__main__':
    unittest.main()
"""

import unittest
import imp
from source.tests.unit.test_load_data import *
from source.models.model_user import *
from source.models.model_errors import *


class TestUserModel(unittest.TestCase):
    data = util_load_test_data()

    def setUp(self):
        pass

    def test_user_model_load(self):
        temp_user = self.data['temp_user'][2]
        user = User(**temp_user)
        self.assertEqual(user.user_name, temp_user['user_name'])
        self.assertEqual(user.user_detail.user_first_name, temp_user['user_detail']['user_first_name'])
        self.assertEqual(user.user_login[0].user_login_time, temp_user['user_login'][0]['user_login_time'])
        self.assertEqual(user.user_follower, temp_user['user_follower'])


class TestErrorModel(unittest.TestCase):

    def test_error_class(self):
        imp.load_source('__main__', 'source/models/model_errors.py')

    def test_error_code(self):
        # ErrorCode Class
        self.assertEqual(ErrorCode.MONGODB_CONNECTION_FAILURE.get_code(), 4000)
        self.assertEqual(ErrorCode.MONGODB_CONNECTION_FAILURE.get_msg(), "MongoDB Connection Failure")

    def test_mongo_error(self):
        # Raise normal MongoError successfully
        with self.assertRaises(MongoError) as e:
            raise MongoError(ErrorCode.MONGODB_USER_NOT_FOUND)
        self.assertEqual(e.exception.error_code, ErrorCode.MONGODB_USER_NOT_FOUND)

        # Wrong MongoError Param
        with self.assertRaises(MongoError) as e:
            MongoError(4000)
        self.assertEqual(e.exception.error_code, ErrorCode.ERR_INCORRECT_CODE)
        self.assertEqual(e.__str__(), e.__str__())

        # Get code & msg
        with self.assertRaises(MongoError) as e:
            raise MongoError(ErrorCode.MONGODB_CONNECTION_FAILURE)
        self.assertEqual(e.exception.get_code(), ErrorCode.MONGODB_CONNECTION_FAILURE.get_code())
        self.assertEqual(e.exception.get_msg(), ErrorCode.MONGODB_CONNECTION_FAILURE.get_msg())
        # print(e.exception.get_code())
        # print(e.exception.get_msg())

        # usage:
        try:
            raise MongoError(ErrorCode.ERR_INCORRECT_CODE)
        except MongoError as e:
            print(e.get_code())
            print(e.get_msg())


if __name__ == '__main__':
    unittest.main()

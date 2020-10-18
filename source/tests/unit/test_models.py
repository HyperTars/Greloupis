import unittest
from source.tests.unit.test_load_data import *
from source.models.model_user import *


class TestModels(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()

import unittest
from source.tests.unit.test_load_data import *
from source.models.model_user import *


class TestModels(unittest.TestCase):
    def setUp(self):
        self.data = util_load_test_data()

    def test_user_model_load(self):
        test_load_data = self.data['temp_user'][0]
        user = User(**test_load_data)
        self.assertEqual(user.user_name, 'temp_user', msg='Test User Name Loading Result')
        self.assertEqual(user.user_email, 'temp_test_user@gmail.com', msg='Test User Email Loading Result')

if __name__ == '__main__':
    unittest.main()

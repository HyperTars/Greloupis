import unittest
from source.utils.util_load_test_data import *
from source.models.model_user import *


class TestModels(unittest.TestCase):
    def setUp(self):
        self.data = util_load_test_data()

    def test_user_model_load(self):
        test_load_data = self.data['user'][0] 
        user = User(**test_load_data)
        self.assertEqual(user.user_name, 'hypertars', msg='Test Model Loading Result')
        self.assertEqual(user.user_detail.first_name, 'Brian',  msg='Test Model Loading Result')
        self.assertEqual(user.user_recent_login[0].login_time, {'$date': {'$numberLong': '1601195652000'}},
                         msg='Test Model Loading Result')


if __name__ == '__main__':
    unittest.main()

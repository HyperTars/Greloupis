import unittest
from source.settings import *
from source.db.mongo import get_db
from source.tests.unit.test_load_data import *
from source.db.query_user import *
from source.models.model_errors import MongoError


class TestQueryUser(unittest.TestCase):

    data = util_load_test_data()

    const_user_0 = data['const_user'][0]
    const_user_1 = data['const_user'][1]
    const_user_2 = data['const_user'][2]

    temp_user_0 = data['temp_user'][0]
    temp_user_1 = data['temp_user'][1]

    def setUp(self):
        pass

    def test_a_user_create(self):
        # Create successfully
        self.assertEqual(query_user_create(user_name=self.temp_user_0['user_name'],
                                           user_email=self.temp_user_0['user_email'],
                                           user_password=self.temp_user_0['user_password']).user_name,
                         self.temp_user_0['user_name'])

        # Raise Error: ErrorCode.MONGODB_USER_NAME_TAKEN
        with self.assertRaises(MongoError) as e1:
            query_user_create(user_name=self.temp_user_0['user_name'], user_email="NotImportantEmail",
                              user_password="NotImportantPassword")
        self.assertEqual(e1.exception.error_code, ErrorCode.MONGODB_USER_NAME_TAKEN)

        # Raise Error: ErrorCode.MONGODB_USER_EMAIL_TAKEN
        with self.assertRaises(MongoError) as e2:
            query_user_create(user_name="NotImportantName", user_email=self.temp_user_0['user_email'],
                              user_password="NotImportantPassword")
        self.assertEqual(e2.exception.error_code, ErrorCode.MONGODB_USER_EMAIL_TAKEN)

    def test_b_user_get_by_name(self):
        # Get successfully
        temp_model = query_user_get_by_name(self.const_user_0['user_name'])[0]
        self.assertEqual(temp_model.user_email, self.const_user_0['user_email'])

    def test_c_user_get_by_email(self):
        pass

    def test_d_user_get_by_id(self):
        pass

    def test_e_user_update_status(self):
        pass

    def test_f_user_add_follow(self):
        pass

    def test_g_user_delete_follow(self):
        pass

    def test_h_user_update_name(self):
        pass

    def test_i_user_update_password(self):
        pass

    def test_j_user_update_thumbnail(self):
        pass

    def test_k_user_update_details(self):
        pass

    def test_l_user_add_login(self):
        pass

    def test_m_user_delete_by_id(self):
        temp_model = query_user_get_by_name(self.temp_user_0['user_name'])[0].to_dict()
        self.assertEqual(query_user_delete_by_id(temp_model['user_id']), 1)

    def test_n_user_delete_by_name(self):
        pass

    def test_o_user_search_by_contains(self):
        pass

    def test_p_user_search_by_pattern(self):
        pass

    def test_q_user_search_by_aggregate(self):
        pass


class TestQueryVideo(unittest.TestCase):
    def setUp(self):
        self.data = util_load_test_data()


class TestQueryVideoOp(unittest.TestCase):
    def setUp(self):
        self.data = util_load_test_data()


class TestQuerySearch(unittest.TestCase):
    def setUp(self):
        self.data = util_load_test_data()


if __name__ == "__main__":
    db = get_db(TestConfig)
    unittest.main()

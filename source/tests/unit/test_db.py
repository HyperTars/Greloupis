import unittest
from source.settings import *
from source.db.mongo import get_db
from source.tests.unit.test_load_data import *
from source.db.query_user import *
from source.models.model_errors import MongoError
from source.utils.util_pattern import *


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

        self.assertEqual(query_user_create(user_name=self.temp_user_1['user_name'],
                                           user_email=self.temp_user_1['user_email'],
                                           user_password=self.temp_user_1['user_password'],
                                           user_ip=self.temp_user_1['user_reg_ip']).user_name,
                         self.temp_user_1['user_name'])

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
        # Get successfully
        temp_model = query_user_get_by_email(self.const_user_0['user_email'])[0]
        self.assertEqual(temp_model.user_name, self.const_user_0['user_name'])

    def test_d_user_get_by_id(self):
        # Get successfully
        temp_model = query_user_get_by_name(self.const_user_0['user_name'])[0]
        temp_model_1 = query_user_get_by_id(temp_model.to_dict()['user_id'])[0]
        self.assertEqual(temp_model_1.user_name, self.const_user_0['user_name'])

    def test_e_user_update_status(self):
        # Update successfully
        temp_model = query_user_get_by_name(self.const_user_0['user_name'])[0]
        temp_user_id = temp_model.to_dict()['user_id']
        query_user_update_status(temp_user_id, "private")
        self.assertEqual(query_user_get_by_id(temp_user_id)[0].user_status, "private")
        query_user_update_status(temp_user_id, "public")
        self.assertEqual(query_user_get_by_id(temp_user_id)[0].user_status, "public")

    def test_f_user_add_follow(self):
        # Update successfully
        temp_model_1 = query_user_get_by_name(self.temp_user_0['user_name'])[0]
        temp_model_2 = query_user_get_by_name(self.temp_user_1['user_name'])[0]
        temp_user_id_1 = temp_model_1.to_dict()['user_id']
        temp_user_id_2 = temp_model_2.to_dict()['user_id']
        query_user_add_follow(temp_user_id_1, temp_user_id_2)
        temp_model_1_updated = query_user_get_by_id(temp_user_id_1)[0]
        temp_model_2_updated = query_user_get_by_id(temp_user_id_2)[0]
        self.assertIn(temp_user_id_2, temp_model_1_updated.to_dict()['user_following'])
        self.assertIn(temp_user_id_1, temp_model_2_updated.to_dict()['user_follower'])

    def test_g_user_delete_follow(self):
        # Update successfully
        temp_model_1 = query_user_get_by_name(self.temp_user_0['user_name'])[0]
        temp_model_2 = query_user_get_by_name(self.temp_user_1['user_name'])[0]
        temp_user_id_1 = temp_model_1.to_dict()['user_id']
        temp_user_id_2 = temp_model_2.to_dict()['user_id']
        self.assertIn(temp_user_id_2, temp_model_1.to_dict()['user_following'])
        self.assertIn(temp_user_id_1, temp_model_2.to_dict()['user_follower'])
        query_user_delete_follow(temp_user_id_1, temp_user_id_2)
        temp_model_1_updated = query_user_get_by_id(temp_user_id_1)[0]
        temp_model_2_updated = query_user_get_by_id(temp_user_id_2)[0]
        self.assertNotIn(temp_user_id_2, temp_model_1_updated.to_dict()['user_following'])
        self.assertNotIn(temp_user_id_1, temp_model_2_updated.to_dict()['user_follower'])

    def test_h_user_update_name(self):
        # Update successfully
        old_name = self.temp_user_0['user_name']
        new_name = "JustANewName"
        temp_model = query_user_get_by_name(old_name)[0]
        temp_user_id = temp_model.to_dict()['user_id']

        query_user_update_name(temp_user_id, new_name)
        self.assertEqual(query_user_get_by_id(temp_user_id)[0].user_name, new_name)

        query_user_update_name(temp_user_id, old_name)
        self.assertEqual(query_user_get_by_id(temp_user_id)[0].user_name, old_name)

    def test_i_user_update_password(self):
        # Update successfully
        old_pass = self.temp_user_0['user_password']
        new_pass = "JustANewPass"
        temp_user_id = query_user_get_by_name(self.temp_user_0['user_name'])[0].to_dict()['user_id']

        query_user_update_password(temp_user_id, new_pass)
        self.assertEqual(query_user_get_by_id(temp_user_id)[0].user_password, new_pass)

        query_user_update_password(temp_user_id, old_pass)
        self.assertEqual(query_user_get_by_id(temp_user_id)[0].user_password, old_pass)

    def test_j_user_update_thumbnail(self):
        # Update successfully
        temp_model = query_user_get_by_name(self.temp_user_0['user_name'])[0].to_dict()
        temp_user_id = temp_model['user_id']
        old_thumbnail = temp_model['user_thumbnail']
        new_thumbnail = "https://s3.amazon.com/just_a_new_thumbnail.png"

        query_user_update_thumbnail(temp_user_id, new_thumbnail)
        self.assertEqual(query_user_get_by_id(temp_user_id)[0].user_thumbnail, new_thumbnail)

        query_user_update_password(temp_user_id, old_thumbnail)
        self.assertEqual(query_user_get_by_id(temp_user_id)[0].user_password, old_thumbnail)

    def test_k_user_update_details(self):
        pass

    def test_l_user_add_login(self):
        # Add successfully
        temp_model = query_user_get_by_name(self.temp_user_0['user_name'])[0].to_dict()
        temp_user_id = temp_model['user_id']
        temp_ip = "777.777.777.777"
        temp_time = get_time_now_utc()
        temp_login = {'user_login_ip': temp_ip, 'user_login_time': temp_time}
        query_user_add_login(temp_user_id, temp_ip, temp_time)

        self.assertIn(temp_login, query_user_get_by_id(temp_user_id)[0].to_dict()['user_login'])

    def test_m_user_delete_by_id(self):
        # Delete successfully
        temp_model_0 = query_user_get_by_name(self.temp_user_0['user_name'])[0].to_dict()
        self.assertEqual(query_user_delete_by_id(temp_model_0['user_id']), 1)

    def test_n_user_delete_by_name(self):
        # Delete successfully
        self.assertEqual(query_user_delete_by_name(self.temp_user_1['user_name']), 1)

    def test_o_user_search_by_contains(self):
        # Search successfully
        search_user_name = self.const_user_0['user_name']
        self.assertEqual(query_user_search_by_contains(user_name=search_user_name[1:2])[0].user_name, search_user_name)

    def test_p_user_search_by_pattern(self):
        search_user_name = self.const_user_0['user_name']

        # Search exact fail
        pattern_exact_fail = util_pattern_compile(search_user_name[1:2], exact=True, ignore_case=True)
        self.assertEqual(len(query_user_search_by_pattern(pattern_name=pattern_exact_fail)), 0)

        # Search exact successfully
        pattern_exact_success = util_pattern_compile(search_user_name, exact=True, ignore_case=True)
        self.assertEqual(query_user_search_by_pattern(pattern_name=pattern_exact_success)[0].user_name,
                         search_user_name)

        # Search case fail
        pattern_case_fail = util_pattern_compile(search_user_name[1:2].upper(), exact=False, ignore_case=False)
        self.assertEqual(len(query_user_search_by_pattern(pattern_name=pattern_case_fail)), 0)

        # Search case successfully
        pattern_case_success = util_pattern_compile(search_user_name[1:2].upper(), exact=False, ignore_case=True)
        self.assertEqual(query_user_search_by_pattern(pattern_name=pattern_case_success)[0].user_name,
                         search_user_name)

    def test_q_user_search_by_aggregate(self):
        # Search successfully
        pipeline1 = [
            {
                "$match":
                {
                    "user_name": {"$regex": "l"},
                    "user_status": "public"
                }
            }
        ]
        pipeline2 = [
            {"$unwind": "$user_detail"},
            {
                "$match":
                {
                    "user_detail.user_street1": {"$regex": "343"},
                    "user_status": "public"
                }
            }
        ]
        self.assertEqual(query_user_search_by_aggregate(pipeline1)[0]['user_name'], "milvus")
        self.assertEqual(query_user_search_by_aggregate(pipeline2)[0]['user_name'], "hypertars")


class TestQueryVideo(unittest.TestCase):
    def setUp(self):
        self.data = util_load_test_data()


class TestQueryVideoOp(unittest.TestCase):
    def setUp(self):
        self.data = util_load_test_data()


if __name__ == "__main__":
    db = get_db(TestConfig)
    unittest.main()

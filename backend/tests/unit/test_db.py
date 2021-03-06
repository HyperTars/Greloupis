import unittest
from flask import Flask, g
from settings import config
from utils.util_tests import util_tests_load_data, \
    util_tests_python_version, util_tests_clean_database
from utils.util_pattern import util_pattern_compile
from db.query_user import query_user_get_by_id, \
    query_user_update_details, query_user_create, query_user_delete_by_name, \
    query_user_get_by_name, query_user_get_by_email, \
    query_user_update_status, query_user_add_follow, \
    query_user_delete_follow, query_user_update_name, \
    query_user_update_password, query_user_update_thumbnail, \
    query_user_add_login, query_user_delete_by_id, \
    query_user_search_by_contains, query_user_search_by_pattern, \
    query_user_search_by_aggregate, query_user_update_email
from db.query_video import query_video_get_by_user_id, \
    query_video_cnt_incr_by_one, query_video_update, query_video_delete, \
    query_video_search_by_pattern, query_video_create, \
    query_video_get_by_title, query_video_search_by_aggregate, \
    query_video_cnt_decr_by_one, query_video_search_by_contains, \
    query_video_get_by_video_id
from db.query_video_op import query_video_op_create, \
    query_video_op_get_by_user_video, query_video_op_get_by_op_id, \
    query_video_op_update_process, query_video_op_update_comment, \
    query_video_op_update_like, query_video_op_update_dislike, \
    query_video_op_update_star, query_video_op_search_comment_by_contains, \
    query_video_op_search_comment_by_pattern, query_video_op_get_by_user_id, \
    query_video_op_get_by_video_id, query_video_op_delete
from db.mongo import init_db
from models.model_errors import MongoError, ErrorCode
from utils.util_time import get_time_now_utc
from utils.util_hash import util_hash_encode
import bson


app = Flask(__name__)
app.config.from_object(config['test'])

with app.app_context():
    if 'db' not in g:
        g.db = init_db()


class TestQueryUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.data = util_tests_load_data()
        util_tests_clean_database() if util_tests_python_version() else exit()

    def test_a_user_create(self):
        # Create successfully
        user_created = query_user_create(
            user_name=self.data['temp_user'][0]['user_name'],
            user_email=self.data['temp_user'][0]['user_email'],
            user_password=self.data['temp_user'][0]['user_password'])
        self.assertEqual(user_created.user_name,
                         self.data['temp_user'][0]['user_name'])

        user_created = query_user_create(
            user_name=self.data['temp_user'][1]['user_name'],
            user_email=self.data['temp_user'][1]['user_email'],
            user_password=self.data['temp_user'][1]['user_password'],
            user_ip=self.data['temp_user'][1]['user_reg_ip'])
        self.assertEqual(user_created.user_name,
                         self.data['temp_user'][1]['user_name'])

        # Raise Error: ErrorCode.MONGODB_STR_EXPECTED
        with self.assertRaises(MongoError) as e:
            query_user_create(123, 123, 123)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_STR_EXPECTED)

        # Raise Error: ErrorCode.MONGODB_USER_NAME_TAKEN
        with self.assertRaises(MongoError) as e1:
            query_user_create(user_name=self.data['temp_user'][0]['user_name'],
                              user_email="NotImportantEmail",
                              user_password="NotImportantPassword")
        self.assertEqual(e1.exception.error_code,
                         ErrorCode.MONGODB_USER_NAME_TAKEN)

        # Raise Error: ErrorCode.MONGODB_USER_EMAIL_TAKEN
        with self.assertRaises(MongoError) as e2:
            query_user_create(
                user_name="NotImportantName",
                user_email=self.data['temp_user'][0]['user_email'],
                user_password="NotImportantPassword")
        self.assertEqual(e2.exception.error_code,
                         ErrorCode.MONGODB_USER_EMAIL_TAKEN)

    def test_b_user_get_by_name(self):
        # Get successfully
        temp_model = query_user_get_by_name(
            self.data['const_user'][0]['user_name'])[0]
        self.assertEqual(temp_model.user_email,
                         self.data['const_user'][0]['user_email'])

        # Raise Error: ErrorCode.MONGODB_STR_EXPECTED
        with self.assertRaises(MongoError) as e:
            query_user_get_by_name(123)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_STR_EXPECTED)

    def test_c_user_get_by_email(self):
        # Get successfully
        temp_model = query_user_get_by_email(
            self.data['const_user'][0]['user_email'])[0]
        self.assertEqual(temp_model.user_name,
                         self.data['const_user'][0]['user_name'])

        # Raise Error: ErrorCode.MONGODB_STR_EXPECTED
        with self.assertRaises(MongoError) as e:
            query_user_get_by_email(123)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_STR_EXPECTED)

    def test_d_user_get_by_id(self):
        # Get successfully
        temp_model = query_user_get_by_name(
            self.data['const_user'][0]['user_name'])[0]
        temp_model_1 = query_user_get_by_id(temp_model.to_dict()['user_id'])[0]
        self.assertEqual(temp_model_1.user_name,
                         self.data['const_user'][0]['user_name'])

        # Raise Error: ErrorCode.MONGODB_STR_EXPECTED
        with self.assertRaises(MongoError) as e:
            query_user_get_by_id(bson.ObjectId("123412341234123412341234"))
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_STR_EXPECTED)

    def test_e_user_update_status(self):
        # Update successfully
        temp_model = query_user_get_by_name(
            self.data['const_user'][0]['user_name'])[0]
        temp_user_id = temp_model.to_dict()['user_id']
        query_user_update_status(temp_user_id, "private")
        self.assertEqual(
            query_user_get_by_id(temp_user_id)[0].user_status, "private")
        query_user_update_status(temp_user_id, "public")
        self.assertEqual(
            query_user_get_by_id(temp_user_id)[0].user_status, "public")

        # Raise Error: ErrorCode.MONGODB_STR_EXPECTED
        with self.assertRaises(MongoError) as e:
            query_user_update_status(123, "private")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_STR_EXPECTED)

        # Raise Error: ErrorCode.MONGODB_USER_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_user_update_status("123412341234123412341234", "private")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_USER_NOT_FOUND)

        # Raise Error: ErrorCode.MONGODB_USER_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_user_update_status(temp_user_id, "open")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_USER_INVALID_STATUS)

    def test_f_user_add_follow(self):
        # Update successfully
        temp_model_1 = query_user_get_by_name(
            self.data['temp_user'][0]['user_name'])[0]
        temp_model_2 = query_user_get_by_name(
            self.data['temp_user'][1]['user_name'])[0]
        temp_user_id_1 = temp_model_1.to_dict()['user_id']
        temp_user_id_2 = temp_model_2.to_dict()['user_id']
        query_user_add_follow(temp_user_id_1, temp_user_id_2)
        temp_model_1_updated = query_user_get_by_id(temp_user_id_1)[0]
        temp_model_2_updated = query_user_get_by_id(temp_user_id_2)[0]
        self.assertIn(temp_user_id_2,
                      temp_model_1_updated.to_dict()['user_following'])
        self.assertIn(temp_user_id_1,
                      temp_model_2_updated.to_dict()['user_follower'])

        # Raise Error: ErrorCode.MONGODB_STR_EXPECTED
        with self.assertRaises(MongoError) as e:
            query_user_add_follow(123, 123)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_STR_EXPECTED)

        # Raise Error: ErrorCode.MONGODB_FOLLOWER_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_user_add_follow("123456781234567812345678", temp_user_id_1)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_FOLLOWER_NOT_FOUND)

        # Raise Error: ErrorCode.MONGODB_FOLLOWED_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_user_add_follow(temp_user_id_2, "123456781234567812345678")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_FOLLOWED_NOT_FOUND)

        # Raise Error: ErrorCode.MONGODB_FOLLOW_REL_EXISTS
        with self.assertRaises(MongoError) as e:
            query_user_add_follow(temp_user_id_1, temp_user_id_2)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_FOLLOW_REL_EXISTS)

    def test_g_user_delete_follow(self):
        # Update successfully
        temp_model_1 = query_user_get_by_name(
            self.data['temp_user'][0]['user_name'])[0]
        temp_model_2 = query_user_get_by_name(
            self.data['temp_user'][1]['user_name'])[0]
        temp_user_id_1 = temp_model_1.to_dict()['user_id']
        temp_user_id_2 = temp_model_2.to_dict()['user_id']
        self.assertIn(temp_user_id_2, temp_model_1.to_dict()['user_following'])
        self.assertIn(temp_user_id_1, temp_model_2.to_dict()['user_follower'])
        query_user_delete_follow(temp_user_id_1, temp_user_id_2)
        temp_model_1_updated = query_user_get_by_id(temp_user_id_1)[0]
        temp_model_2_updated = query_user_get_by_id(temp_user_id_2)[0]
        self.assertNotIn(temp_user_id_2,
                         temp_model_1_updated.to_dict()['user_following'])
        self.assertNotIn(temp_user_id_1,
                         temp_model_2_updated.to_dict()['user_follower'])

        # Raise Error: ErrorCode.MONGODB_STR_EXPECTED
        with self.assertRaises(MongoError) as e:
            query_user_delete_follow(123, 123)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_STR_EXPECTED)

        # Raise Error: ErrorCode.MONGODB_FOLLOWER_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_user_delete_follow("123456781234567812345678",
                                     temp_user_id_1)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_FOLLOWER_NOT_FOUND)

        # Raise Error: ErrorCode.MONGODB_FOLLOWED_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_user_delete_follow(temp_user_id_2,
                                     "123456781234567812345678")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_FOLLOWED_NOT_FOUND)

    def test_h_user_update_name(self):
        # Update successfully
        old_name = self.data['temp_user'][0]['user_name']
        new_name = "JustANewName"
        temp_model = query_user_get_by_name(old_name)[0]
        temp_user_id = temp_model.to_dict()['user_id']

        query_user_update_name(temp_user_id, new_name)
        self.assertEqual(query_user_get_by_id(temp_user_id)[0].user_name,
                         new_name)

        query_user_update_name(temp_user_id, old_name)
        self.assertEqual(query_user_get_by_id(temp_user_id)[0].user_name,
                         old_name)

        # Raise Error: ErrorCode.MONGODB_STR_EXPECTED
        with self.assertRaises(MongoError) as e:
            query_user_update_name(123, 123)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_STR_EXPECTED)

        # Raise Error: ErrorCode.MONGODB_USER_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_user_update_name("123456781234567812345678", "kkk")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_USER_NOT_FOUND)

        # Raise Error: ErrorCode.MONGODB_USER_UPDATE_SAME_NAME
        with self.assertRaises(MongoError) as e:
            query_user_update_name(temp_user_id, old_name)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_UPDATE_SAME_NAME)

        # Raise Error: ErrorCode.MONGODB_USER_UPDATE_NAME_TAKEN
        with self.assertRaises(MongoError) as e:
            query_user_update_name(temp_user_id,
                                   self.data['temp_user'][1]['user_name'])
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_USER_NAME_TAKEN)

    def test_i_user_update_password(self):
        # Update successfully
        old_pass = self.data['temp_user'][0]['user_password']
        new_pass = "JustANewPass"
        temp_user_id = \
            query_user_get_by_name(self.data['temp_user'][0]['user_name'])[
                0].to_dict()['user_id']

        query_user_update_password(temp_user_id, new_pass)
        self.assertEqual(query_user_get_by_id(temp_user_id)[0].user_password,
                         util_hash_encode(new_pass))

        query_user_update_password(temp_user_id, old_pass)
        self.assertEqual(query_user_get_by_id(temp_user_id)[0].user_password,
                         util_hash_encode(old_pass))

        # Raise Error: ErrorCode.MONGODB_STR_EXPECTED
        with self.assertRaises(MongoError) as e:
            query_user_update_password(123, 123)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_STR_EXPECTED)

        # Raise Error: ErrorCode.MONGODB_USER_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_user_update_password("123456781234567812345678", "kkk")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_USER_NOT_FOUND)

        # Raise Error: ErrorCode.MONGODB_USER_UPDATE_SAME_NAME
        with self.assertRaises(MongoError) as e:
            query_user_update_password(temp_user_id, old_pass)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_UPDATE_SAME_PASS)

    def test_j_user_update_email(self):
        old_email = self.data['temp_user'][0]['user_email']
        new_email = "somenewemail@gmail.com"
        users = query_user_get_by_name(self.data['temp_user'][0]['user_name'])
        temp_id = users[0].to_dict()['user_id']
        query_user_update_email(temp_id, new_email)
        self.assertEqual(query_user_get_by_id(temp_id)[0].user_email,
                         new_email)
        query_user_update_email(temp_id, old_email)
        self.assertEqual(query_user_get_by_id(temp_id)[0].user_email,
                         old_email)
        # Raise Error: ErrorCode.MONGODB_STR_EXPECTED
        with self.assertRaises(MongoError) as e:
            query_user_update_email(123, 123)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_STR_EXPECTED)
        # Raise Error: ErrorCode.MONGODB_USER_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_user_update_email("123456781234567812345678", "kkk")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_USER_NOT_FOUND)

    def test_k_user_update_thumbnail(self):

        # Update successfully
        users = query_user_get_by_name(self.data['temp_user'][0]['user_name'])
        temp_user_id = users[0].to_dict()['user_id']
        old_thumbnail = users[0].to_dict()['user_thumbnail']
        new_thumbnail = "https://s3.amazon.com/just_a_new_thumbnail.png"

        query_user_update_thumbnail(temp_user_id, new_thumbnail)
        self.assertEqual(query_user_get_by_id(temp_user_id)[0].user_thumbnail,
                         new_thumbnail)

        query_user_update_thumbnail(temp_user_id, old_thumbnail)
        self.assertEqual(query_user_get_by_id(temp_user_id)[0].user_thumbnail,
                         old_thumbnail)

        # Raise Error: ErrorCode.MONGODB_STR_EXPECTED
        with self.assertRaises(MongoError) as e:
            query_user_update_thumbnail(123, 123)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_STR_EXPECTED)

        # Raise Error: ErrorCode.MONGODB_USER_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_user_update_thumbnail("123456781234567812345678", "kkk")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_USER_NOT_FOUND)

    def test_l_user_update_details(self):
        temp_model = \
            query_user_get_by_name(self.data['temp_user'][0]['user_name'])[
                0].to_dict()
        temp_user_id = temp_model['user_id']

        new_user_first_name = "new first name"
        new_user_last_name = "new last name"
        new_user_phone = "+451313445665"
        new_user_street1 = "str1"
        new_user_street2 = "str2"
        new_user_city = "new city"
        new_user_state = "new state"
        new_user_country = "new country"
        new_user_zip = "46961"
        query_user_update_details(user_id=temp_user_id,
                                  user_first_name=new_user_first_name,
                                  user_last_name=new_user_last_name,
                                  user_phone=new_user_phone,
                                  user_street1=new_user_street1,
                                  user_street2=new_user_street2,
                                  user_city=new_user_city,
                                  user_state=new_user_state,
                                  user_country=new_user_country,
                                  user_zip=new_user_zip)

        new_model = query_user_get_by_id(temp_user_id)[0].to_dict()
        self.assertEqual(new_model['user_detail']['user_first_name'],
                         new_user_first_name)
        self.assertEqual(new_model['user_detail']['user_last_name'],
                         new_user_last_name)
        self.assertEqual(new_model['user_detail']['user_phone'],
                         new_user_phone)
        self.assertEqual(new_model['user_detail']['user_street1'],
                         new_user_street1)
        self.assertEqual(new_model['user_detail']['user_street2'],
                         new_user_street2)
        self.assertEqual(new_model['user_detail']['user_city'], new_user_city)
        self.assertEqual(new_model['user_detail']['user_state'],
                         new_user_state)
        self.assertEqual(new_model['user_detail']['user_country'],
                         new_user_country)
        self.assertEqual(new_model['user_detail']['user_zip'], new_user_zip)

        # Raise Error: ErrorCode.MONGODB_MISSING_USER_ID
        with self.assertRaises(MongoError) as e:
            query_user_update_details()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_MISSING_USER_ID)

        # Raise Error: ErrorCode.MONGODB_STR_EXPECTED
        with self.assertRaises(MongoError) as e:
            query_user_update_details(user_id=123)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_STR_EXPECTED)

        # Raise Error: ErrorCode.MONGODB_STR_EXPECTED
        with self.assertRaises(MongoError) as e:
            query_user_update_details(user_id=temp_user_id, user_city=123)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_STR_EXPECTED)

        # Raise Error: ErrorCode.MONGODB_USER_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_user_update_details(user_id="123456781234567812345678")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_USER_NOT_FOUND)

    def test_m_user_add_login(self):
        # Add successfully
        temp_model = \
            query_user_get_by_name(self.data['temp_user'][0]['user_name'])[
                0].to_dict()
        temp_user_id = temp_model['user_id']
        temp_ip = "777.777.777.777"
        temp_time = get_time_now_utc()
        temp_login = {'user_login_ip': temp_ip, 'user_login_time': temp_time}
        query_user_add_login(temp_user_id, temp_ip, temp_time)

        self.assertIn(temp_login,
                      query_user_get_by_id(temp_user_id)[0].to_dict()[
                          'user_login'])

        # Raise Error: ErrorCode.MONGODB_STR_EXPECTED
        with self.assertRaises(MongoError) as e:
            query_user_add_login(123)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_STR_EXPECTED)

        # Raise Error: ErrorCode.MONGODB_USER_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_user_add_login("123456781234567812345678")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_USER_NOT_FOUND)

    def test_n_user_delete_by_id(self):
        # Delete successfully
        temp_model_0 = \
            query_user_get_by_name(self.data['temp_user'][0]['user_name'])[
                0].to_dict()
        self.assertEqual(query_user_delete_by_id(temp_model_0['user_id']), 1)

        # Raise Error: ErrorCode.MONGODB_STR_EXPECTED
        with self.assertRaises(MongoError) as e:
            query_user_delete_by_id(123)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_STR_EXPECTED)

        # Raise Error: ErrorCode.MONGODB_USER_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_user_delete_by_id("123456781234567812345678")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_USER_NOT_FOUND)

    def test_o_user_delete_by_name(self):
        # Delete successfully
        self.assertEqual(
            query_user_delete_by_name(self.data['temp_user'][1]['user_name']),
            1)

        # Raise Error: ErrorCode.MONGODB_STR_EXPECTED
        with self.assertRaises(MongoError) as e:
            query_user_delete_by_name(123)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_STR_EXPECTED)

        # Raise Error: ErrorCode.MONGODB_USER_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_user_delete_by_name("123456781234567812345678")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_USER_NOT_FOUND)

    def test_p_user_search_by_contains(self):
        # Search successfully
        search_user_id = self.data['const_user'][0]['_id']['$oid']
        self.assertEqual(
            str(query_user_search_by_contains(user_id=search_user_id)[0].id),
            search_user_id)

        search_user_name = self.data['const_user'][0]['user_name']
        self.assertEqual(
            query_user_search_by_contains(user_name=search_user_name[1:4])[
                0].user_name, search_user_name)

        search_user_email = self.data['const_user'][0]['user_email']
        self.assertEqual(
            query_user_search_by_contains(user_email=search_user_email[2:8])[
                0].user_email,
            search_user_email)

        search_user_first_name = self.data['const_user'][0]['user_detail'][
            'user_first_name']
        search_result = query_user_search_by_contains(
            user_first_name=search_user_first_name[0:2])[0]
        self.assertEqual(search_result.user_detail.user_first_name,
                         search_user_first_name)

        search_user_last_name = self.data['const_user'][0]['user_detail'][
            'user_last_name']
        search_result = query_user_search_by_contains(
            user_last_name=search_user_last_name[0:2])[0]
        self.assertEqual(search_result.user_detail.user_last_name,
                         search_user_last_name)

        search_user_phone = self.data['const_user'][0]['user_detail'][
            'user_phone']
        self.assertEqual(
            query_user_search_by_contains(user_phone=search_user_phone[1:5])
            [0].user_detail.user_phone, search_user_phone)

        search_user_street1 = self.data['const_user'][0]['user_detail'][
            'user_street1']
        self.assertEqual(
            query_user_search_by_contains(
                user_street1=search_user_street1[1:2])
            [0].user_detail.user_street1, search_user_street1)

        search_user_street2 = self.data['const_user'][0]['user_detail'][
            'user_street2']
        self.assertEqual(
            query_user_search_by_contains(
                user_street2=search_user_street2[0:2])
            [0].user_detail.user_street2, search_user_street2)

        search_user_city = self.data['const_user'][0]['user_detail'][
            'user_city']
        self.assertEqual(
            query_user_search_by_contains(user_city=search_user_city)
            [0].user_detail.user_city, search_user_city)

        search_user_state = self.data['const_user'][0]['user_detail'][
            'user_state']
        self.assertEqual(
            query_user_search_by_contains(user_state=search_user_state)
            [0].user_detail.user_state, search_user_state)

        search_user_country = self.data['const_user'][0]['user_detail'][
            'user_country']
        self.assertEqual(
            query_user_search_by_contains(
                user_country=search_user_country[1:2])
            [0].user_detail.user_country, search_user_country)

        search_user_zip = self.data['const_user'][0]['user_detail']['user_zip']
        self.assertEqual(
            query_user_search_by_contains(user_zip=search_user_zip[1:2])
            [0].user_detail.user_zip, search_user_zip)

        search_user_status = self.data['const_user'][0]['user_status']
        self.assertEqual(
            query_user_search_by_contains(user_status=search_user_status[1:2])
            [0].user_status, search_user_status)

        # Raise Error: ErrorCode.MONGODB_EMPTY_PARAM
        with self.assertRaises(MongoError) as e:
            query_user_search_by_contains()
        self.assertEqual(e.exception.error_code, ErrorCode.MONGODB_EMPTY_PARAM)

        # Raise Error: ErrorCode.MONGODB_STR_EXPECTED
        with self.assertRaises(MongoError) as e:
            query_user_search_by_contains(user_city=123)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_STR_EXPECTED)

        # Raise Error: ErrorCode.MONGODB_INVALID_SEARCH_PARAM
        with self.assertRaises(MongoError) as e:
            query_user_search_by_contains(user_lmao="lmao")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_INVALID_SEARCH_PARAM)

    def test_q_user_search_by_pattern(self):
        search_user_name = self.data['const_user'][0]['user_name']

        # PATTERN NAME #
        # Search exact fail
        pattern_exact_fail = util_pattern_compile(search_user_name[1:2],
                                                  exact=True, ignore_case=True)
        self.assertEqual(
            len(query_user_search_by_pattern(pattern_name=pattern_exact_fail)),
            0)

        # Search exact successfully
        pattern_exact_success = util_pattern_compile(search_user_name,
                                                     exact=True,
                                                     ignore_case=True)
        self.assertEqual(
            query_user_search_by_pattern(pattern_name=pattern_exact_success)[
                0].user_name,
            search_user_name)

        # Search case fail
        pattern_case_fail = util_pattern_compile(search_user_name[1:2].upper(),
                                                 exact=False,
                                                 ignore_case=False)
        self.assertEqual(
            len(query_user_search_by_pattern(pattern_name=pattern_case_fail)),
            0)

        # Search case successfully
        pattern_case_success = util_pattern_compile(
            search_user_name[1:2].upper(), exact=False, ignore_case=True)
        self.assertEqual(
            query_user_search_by_pattern(pattern_name=pattern_case_success)[
                0].user_name,
            search_user_name)

        # PATTERN EMAIL #
        search_user_email = self.data['const_user'][0]['user_email']
        pattern_email = util_pattern_compile(search_user_email[1:5],
                                             exact=False, ignore_case=True)
        self.assertEqual(
            query_user_search_by_pattern(pattern_email=pattern_email)[
                0].user_email,
            search_user_email)

        # PATTERN FIRST NAME #
        search_user_first_name = self.data['const_user'][0]['user_detail'][
            'user_first_name']
        pattern_first_name = util_pattern_compile(search_user_first_name[0:3],
                                                  exact=False,
                                                  ignore_case=True)
        self.assertEqual(
            query_user_search_by_pattern(pattern_first_name=pattern_first_name)
            [0].user_detail.user_first_name, search_user_first_name)

        # PATTERN LAST NAME #
        search_user_last_name = self.data['const_user'][0]['user_detail'][
            'user_last_name']
        pattern_last_name = util_pattern_compile(search_user_last_name[0:3],
                                                 exact=False, ignore_case=True)
        self.assertEqual(
            query_user_search_by_pattern(pattern_last_name=pattern_last_name)
            [0].user_detail.user_last_name, search_user_last_name)

        # PATTERN PHONE #
        search_user_phone = self.data['const_user'][0]['user_detail'][
            'user_phone']
        pattern_phone = util_pattern_compile(search_user_phone[0:3],
                                             exact=False, ignore_case=True)
        self.assertEqual(
            query_user_search_by_pattern(pattern_phone=pattern_phone)[
                0].user_detail.user_phone,
            search_user_phone)

        # PATTERN STREET1 #
        search_user_street1 = self.data['const_user'][0]['user_detail'][
            'user_street1']
        pattern_street1 = util_pattern_compile(search_user_street1[0:3],
                                               exact=False, ignore_case=True)
        self.assertEqual(
            query_user_search_by_pattern(pattern_street1=pattern_street1)[
                0].user_detail.user_street1,
            search_user_street1)

        # PATTERN STREET2 #
        search_user_street2 = self.data['const_user'][0]['user_detail'][
            'user_street2']
        pattern_street2 = util_pattern_compile(search_user_street2[0:2],
                                               exact=False, ignore_case=True)
        self.assertEqual(
            query_user_search_by_pattern(pattern_street2=pattern_street2)[
                0].user_detail.user_street2,
            search_user_street2)

        # PATTERN CITY #
        search_user_city = self.data['const_user'][0]['user_detail'][
            'user_city']
        pattern_city = util_pattern_compile(search_user_city[1:3], exact=False,
                                            ignore_case=True)
        self.assertEqual(
            query_user_search_by_pattern(pattern_city=pattern_city)[
                0].user_detail.user_city,
            search_user_city)

        # PATTERN STATE #
        search_user_state = self.data['const_user'][0]['user_detail'][
            'user_state']
        pattern_state = util_pattern_compile(search_user_state[1:4],
                                             exact=False, ignore_case=True)
        self.assertEqual(
            query_user_search_by_pattern(pattern_state=pattern_state)[
                0].user_detail.user_state,
            search_user_state)

        # PATTERN COUNTRY #
        search_user_country = self.data['const_user'][0]['user_detail'][
            'user_country']
        pattern_country = util_pattern_compile(search_user_country[1:3],
                                               exact=False, ignore_case=True)
        self.assertEqual(
            query_user_search_by_pattern(pattern_country=pattern_country)[
                0].user_detail.user_country,
            search_user_country)

        # PATTERN ZIP #
        search_user_zip = self.data['const_user'][0]['user_detail']['user_zip']
        pattern_zip = util_pattern_compile(search_user_zip[2:5], exact=False,
                                           ignore_case=True)
        search_res = query_user_search_by_pattern(pattern_zip=pattern_zip)[0]
        self.assertEqual(search_res.user_detail.user_zip, search_user_zip)

        # PATTERN STATUS #
        search_user_status = self.data['const_user'][0]['user_status']
        pattern_status = util_pattern_compile(search_user_status[0:3],
                                              exact=False, ignore_case=True)
        self.assertEqual(
            query_user_search_by_pattern(pattern_status=pattern_status)[
                0].user_status,
            search_user_status)

        # Raise Error: ErrorCode.MONGODB_EMPTY_PARAM
        with self.assertRaises(MongoError) as e:
            query_user_search_by_pattern()
        self.assertEqual(e.exception.error_code, ErrorCode.MONGODB_EMPTY_PARAM)

        # Raise Error: ErrorCode.MONGODB_RE_PATTERN_EXPECTED
        with self.assertRaises(MongoError) as e:
            query_user_search_by_pattern(user_city="1234")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_RE_PATTERN_EXPECTED)

        # Raise Error: ErrorCode.MONGODB_INVALID_SEARCH_PARAM
        with self.assertRaises(MongoError) as e:
            query_user_search_by_pattern(user_lmao=pattern_email)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_INVALID_SEARCH_PARAM)

    def test_r_user_search_by_aggregate(self):
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
        self.assertEqual(
            query_user_search_by_aggregate(pipeline1)[0]['user_name'],
            "milvus")
        self.assertEqual(
            query_user_search_by_aggregate(pipeline2)[0]['user_name'],
            "hypertars")

        # Raise Error: ErrorCode.MONGODB_LIST_EXPECTED
        with self.assertRaises(MongoError) as e:
            query_user_search_by_aggregate("lol")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_LIST_EXPECTED)


class TestQueryVideo(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.data = util_tests_load_data()
        util_tests_clean_database()

    def test_a_query_video_create(self):
        temp_data = self.data['temp_video'][0]
        vid = query_video_create(temp_data['user_id'])
        title = temp_data['video_title']
        query_video_update(vid, video_title=title)
        self.assertEqual(type(vid), str)
        self.assertEqual(len(vid), 24)

        # Raise Error: ErrorCode.MONGODB_USER_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_video_create("123456781234567812345678")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_USER_NOT_FOUND)

    def test_b_query_video_get_by_video_id(self):
        result = query_video_get_by_video_id(
            str(self.data['const_video'][0]['_id']['$oid']))[0]
        self.assertEqual(result.video_title,
                         self.data['const_video'][0]['video_title'])

    def test_c_query_video_get_by_user_id(self):
        self.assertEqual(
            len(query_video_get_by_user_id(
                self.data['temp_video'][0]['user_id'])), 1)

    def test_d_query_video_get_by_title(self):
        self.assertEqual(
            query_video_get_by_title(
                self.data['temp_video'][0]['video_title'])[
                0].user_id,
            self.data['temp_video'][0]['user_id'])

    def test_e_query_video_cnt_incr_by_one(self):
        temp_model = \
            query_video_get_by_title(
                self.data['temp_video'][0]['video_title'])[
                0].to_dict()
        temp_video_id = temp_model['video_id']
        temp_video_view = temp_model['video_view']
        temp_video_comment = temp_model['video_comment']
        temp_video_like = temp_model['video_like']
        temp_video_dislike = temp_model['video_dislike']
        temp_video_star = temp_model['video_star']
        temp_video_share = temp_model['video_share']

        query_video_cnt_incr_by_one(temp_video_id, "video_view")
        self.assertEqual(
            query_video_get_by_video_id(temp_video_id)[0].video_view,
            temp_video_view + 1)
        query_video_cnt_incr_by_one(temp_video_id, "video_comment")
        self.assertEqual(
            query_video_get_by_video_id(temp_video_id)[0].video_view,
            temp_video_comment + 1)
        query_video_cnt_incr_by_one(temp_video_id, "video_like")
        self.assertEqual(
            query_video_get_by_video_id(temp_video_id)[0].video_view,
            temp_video_like + 1)
        query_video_cnt_incr_by_one(temp_video_id, "video_dislike")
        self.assertEqual(
            query_video_get_by_video_id(temp_video_id)[0].video_view,
            temp_video_dislike + 1)
        query_video_cnt_incr_by_one(temp_video_id, "video_star")
        self.assertEqual(
            query_video_get_by_video_id(temp_video_id)[0].video_view,
            temp_video_star + 1)
        query_video_cnt_incr_by_one(temp_video_id, "video_share")
        self.assertEqual(
            query_video_get_by_video_id(temp_video_id)[0].video_view,
            temp_video_share + 1)

        # Raise Error: ErrorCode.MONGODB_VIDEO_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_video_cnt_incr_by_one("123456781234567812345678",
                                        "video_view")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_VIDEO_NOT_FOUND)

        # Raise Error: ErrorCode.MONGODB_VIDEO_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_video_cnt_incr_by_one(temp_video_id, "video_lol")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_INVALID_VIDEO_CNT_PARAM)

    def test_f_query_video_cnt_decr_by_one(self):
        temp_model = \
            query_video_get_by_title(
                self.data['temp_video'][0]['video_title'])[
                0].to_dict()
        temp_video_id = temp_model['video_id']
        temp_video_view = temp_model['video_view']
        temp_video_comment = temp_model['video_comment']
        temp_video_like = temp_model['video_like']
        temp_video_dislike = temp_model['video_dislike']
        temp_video_star = temp_model['video_star']
        temp_video_share = temp_model['video_share']

        query_video_cnt_decr_by_one(temp_video_id, "video_view")
        self.assertEqual(
            query_video_get_by_video_id(temp_video_id)[0].video_view,
            temp_video_view - 1)
        query_video_cnt_decr_by_one(temp_video_id, "video_comment")
        self.assertEqual(
            query_video_get_by_video_id(temp_video_id)[0].video_view,
            temp_video_comment - 1)
        query_video_cnt_decr_by_one(temp_video_id, "video_like")
        self.assertEqual(
            query_video_get_by_video_id(temp_video_id)[0].video_view,
            temp_video_like - 1)
        query_video_cnt_decr_by_one(temp_video_id, "video_dislike")
        self.assertEqual(
            query_video_get_by_video_id(temp_video_id)[0].video_view,
            temp_video_dislike - 1)
        query_video_cnt_decr_by_one(temp_video_id, "video_star")
        self.assertEqual(
            query_video_get_by_video_id(temp_video_id)[0].video_view,
            temp_video_star - 1)
        query_video_cnt_decr_by_one(temp_video_id, "video_share")
        self.assertEqual(
            query_video_get_by_video_id(temp_video_id)[0].video_view,
            temp_video_share - 1)

        # Down to Zero Without Overflow
        while query_video_cnt_decr_by_one(temp_video_id, "video_view") != 0:
            query_video_cnt_decr_by_one(temp_video_id, "video_view")
        query_video_cnt_decr_by_one(temp_video_id, "video_view")
        self.assertEqual(
            query_video_get_by_video_id(temp_video_id)[0].video_view, 0)

        while query_video_cnt_decr_by_one(temp_video_id, "video_comment") != 0:
            query_video_cnt_decr_by_one(temp_video_id, "video_comment")
        query_video_cnt_decr_by_one(temp_video_id, "video_comment")
        self.assertEqual(
            query_video_get_by_video_id(temp_video_id)[0].video_view, 0)

        while query_video_cnt_decr_by_one(temp_video_id, "video_like") != 0:
            query_video_cnt_decr_by_one(temp_video_id, "video_like")
        query_video_cnt_decr_by_one(temp_video_id, "video_like")
        self.assertEqual(
            query_video_get_by_video_id(temp_video_id)[0].video_view, 0)

        while query_video_cnt_decr_by_one(temp_video_id, "video_dislike") != 0:
            query_video_cnt_decr_by_one(temp_video_id, "video_dislike")
        query_video_cnt_decr_by_one(temp_video_id, "video_dislike")
        self.assertEqual(
            query_video_get_by_video_id(temp_video_id)[0].video_view, 0)

        while query_video_cnt_decr_by_one(temp_video_id, "video_star") != 0:
            query_video_cnt_decr_by_one(temp_video_id, "video_star")
        query_video_cnt_decr_by_one(temp_video_id, "video_star")
        self.assertEqual(
            query_video_get_by_video_id(temp_video_id)[0].video_view, 0)

        while query_video_cnt_decr_by_one(temp_video_id, "video_share") != 0:
            query_video_cnt_decr_by_one(temp_video_id, "video_share")
        query_video_cnt_decr_by_one(temp_video_id, "video_share")
        self.assertEqual(
            query_video_get_by_video_id(temp_video_id)[0].video_view, 0)

        # Raise Error: ErrorCode.MONGODB_VIDEO_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_video_cnt_decr_by_one("123456781234567812345678",
                                        "video_view")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_VIDEO_NOT_FOUND)

        # Raise Error: ErrorCode.MONGODB_VIDEO_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_video_cnt_decr_by_one(temp_video_id, "video_lol")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_INVALID_VIDEO_CNT_PARAM)

    def test_g_query_video_update(self):
        temp_video_id = \
            query_video_get_by_title(
                self.data['temp_video'][0]['video_title'])[
                0].to_dict()['video_id']

        old_title = self.data['temp_video'][0]['video_title']
        new_title = "new_title"
        new_raw_content = "some new content uri"
        new_raw_status = "streaming"
        new_raw_size = 123.45
        new_duration = 777
        new_channel = "tc"
        new_tag = ["lol", "ooo"]
        new_category = ["movie"]
        new_description = "dessss"
        new_language = "alien lan"
        new_status = "public"
        new_thumbnail = "https://thumbnail.jpg"
        new_uri_low = "https://uri_low.mp4"
        new_uri_mid = "https://uri_mid.mp4"
        new_uri_high = "https://uri_high.mp4"

        query_video_update(temp_video_id, video_title=new_title,
                           video_raw_content=new_raw_content,
                           video_raw_status=new_raw_status,
                           video_raw_size=new_raw_size,
                           video_duration=new_duration,
                           video_channel=new_channel, video_tag=new_tag,
                           video_category=new_category,
                           video_description=new_description,
                           video_language=new_language,
                           video_status=new_status,
                           video_thumbnail=new_thumbnail,
                           video_uri_low=new_uri_low,
                           video_uri_mid=new_uri_mid,
                           video_uri_high=new_uri_high)

        new_model = query_video_get_by_video_id(temp_video_id)[0]
        self.assertEqual(new_model.video_title, new_title)
        self.assertEqual(new_model.video_raw_content, new_raw_content)
        self.assertEqual(new_model.video_raw_status, new_raw_status)
        self.assertEqual(new_model.video_raw_size, new_raw_size)
        self.assertEqual(new_model.video_duration, new_duration)
        self.assertEqual(new_model.video_channel, new_channel)
        self.assertEqual(new_model.video_tag, new_tag)
        self.assertEqual(new_model.video_category, new_category)
        self.assertEqual(new_model.video_description, new_description)
        self.assertEqual(new_model.video_language, new_language)
        self.assertEqual(new_model.video_status, new_status)
        self.assertEqual(new_model.video_thumbnail, new_thumbnail)
        self.assertEqual(new_model.video_uri.video_uri_low, new_uri_low)
        self.assertEqual(new_model.video_uri.video_uri_mid, new_uri_mid)
        self.assertEqual(new_model.video_uri.video_uri_high, new_uri_high)

        query_video_update(temp_video_id, video_title=old_title)
        self.assertEqual(
            query_video_get_by_video_id(temp_video_id)[0].video_title,
            old_title)

        # Raise Error: ErrorCode.MONGODB_VIDEO_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_video_update("123456781234567812345678")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_VIDEO_NOT_FOUND)

        # Raise Error: ErrorCode.MONGODB_LIST_EXPECTED
        with self.assertRaises(MongoError) as e:
            query_video_update(temp_video_id, video_tag="test")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_LIST_EXPECTED)

        # Raise Error: ErrorCode.MONGODB_LIST_EXPECTED
        with self.assertRaises(MongoError) as e:
            query_video_update(temp_video_id, video_category="test")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_LIST_EXPECTED)

        # Raise Error: ErrorCode.MONGODB_VIDEO_INVALID_STATUS
        with self.assertRaises(MongoError) as e:
            query_video_update(temp_video_id, video_status="test")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_VIDEO_INVALID_STATUS)

        # Raise Error: ErrorCode.MONGODB_VIDEO_INVALID_STATUS
        with self.assertRaises(MongoError) as e:
            query_video_update(temp_video_id, video_raw_status="test")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_VIDEO_INVALID_STATUS)

    def test_h_query_video_delete(self):
        temp_title = self.data['temp_video'][0]['video_title']
        temp_video = query_video_get_by_title(temp_title)
        temp_video_id_0 = temp_video[0].to_dict()['video_id']
        self.assertEqual(query_video_delete(temp_video_id_0), 1)

        # Raise Error: ErrorCode.MONGODB_VIDEO_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_video_delete("123456781234567812345678")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_VIDEO_NOT_FOUND)

    def test_i_query_video_search_by_contains(self):
        video = query_video_search_by_contains(
            video_id=self.data['const_video'][0]['_id']['$oid'])[
            0]  # exact video_id
        self.assertEqual(video.video_title,
                         self.data['const_video'][0]['video_title'])

        video = query_video_search_by_contains(
            user_id=self.data['const_video'][0]['user_id'])[0]  # exact user_id
        self.assertEqual(video.video_title,
                         self.data['const_video'][0]['video_title'])

        video = query_video_search_by_contains(
            video_title=self.data['const_video'][0]['video_title'][1:2])[0]
        self.assertEqual(video.video_title,
                         self.data['const_video'][0]['video_title'])

        video = query_video_search_by_contains(
            video_channel=self.data['const_video'][0]['video_channel'])[0]
        self.assertEqual(video.video_title,
                         self.data['const_video'][0]['video_title'])

        video = query_video_search_by_contains(
            video_category=self.data['const_video'][0]['video_category'][0])[0]
        self.assertEqual(video.video_title,
                         self.data['const_video'][0]['video_title'])

        video = query_video_search_by_contains(
            video_tag=self.data['const_video'][0]['video_tag'][0])[0]
        self.assertEqual(video.video_title,
                         self.data['const_video'][0]['video_title'])

        desc = self.data['const_video'][0]['video_description'][2:3]
        video = query_video_search_by_contains(video_description=desc)[0]
        self.assertEqual(video.video_title,
                         self.data['const_video'][0]['video_title'])

        # Raise Error: ErrorCode.MONGODB_EMPTY_PARAM
        with self.assertRaises(MongoError) as e:
            query_video_search_by_contains()
        self.assertEqual(e.exception.error_code, ErrorCode.MONGODB_EMPTY_PARAM)

        # Raise Error: ErrorCode.MONGODB_STR_EXPECTED
        with self.assertRaises(MongoError) as e:
            query_video_search_by_contains(video_title=123)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_STR_EXPECTED)

        # Raise Error: ErrorCode.MONGODB_VIDEO_INVALID_SEARCH_PARAM
        with self.assertRaises(MongoError) as e:
            query_video_search_by_contains(video_test="lol")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_INVALID_SEARCH_PARAM)

    def test_j_query_video_search_by_pattern(self):
        search_video_title = self.data['const_video'][0]['video_title']
        search_video_channel = self.data['const_video'][0]['video_channel']
        search_video_description = self.data['const_video'][0][
            'video_description']

        # SEARCH BY TITLE PATTERN #
        # Search exact fail
        pattern_exact_fail = util_pattern_compile(search_video_title[1:2],
                                                  exact=True, ignore_case=True)
        self.assertEqual(len(
            query_video_search_by_pattern(pattern_title=pattern_exact_fail)),
            0)

        # Search exact successfully
        pattern_exact_success = util_pattern_compile(search_video_title,
                                                     exact=True,
                                                     ignore_case=True)
        self.assertEqual(
            query_video_search_by_pattern(pattern_title=pattern_exact_success)[
                0].video_title,
            search_video_title)

        # Search case fail
        pattern_case_fail = util_pattern_compile(
            search_video_title[1:2].upper(), exact=False, ignore_case=False)
        self.assertEqual(
            len(query_video_search_by_pattern(
                pattern_title=pattern_case_fail)),
            0)

        # Search case successfully
        pattern_case_success = util_pattern_compile(
            search_video_title[1:2].upper(), exact=False, ignore_case=True)
        self.assertEqual(
            query_video_search_by_pattern(pattern_title=pattern_case_success)[
                0].video_title,
            search_video_title)

        # SEARCH BY CHANNEL PATTERN #
        # Search exact fail
        pattern_exact_fail = util_pattern_compile(search_video_channel[1:2],
                                                  exact=True, ignore_case=True)
        self.assertEqual(len(
            query_video_search_by_pattern(pattern_channel=pattern_exact_fail)),
            0)

        # Search exact successfully
        pattern_exact_success = util_pattern_compile(search_video_channel,
                                                     exact=True,
                                                     ignore_case=True)
        res = query_video_search_by_pattern(
            pattern_channel=pattern_exact_success)[0]
        self.assertEqual(res.video_channel, search_video_channel)

        # Search case fail
        pattern_case_fail = util_pattern_compile(
            search_video_channel[1:2].upper(), exact=False, ignore_case=False)
        self.assertEqual(len(
            query_video_search_by_pattern(pattern_channel=pattern_case_fail)),
            0)

        # Search case successfully
        pattern_case_success = util_pattern_compile(
            search_video_channel[1:2].upper(), exact=False, ignore_case=True)
        self.assertEqual(
            query_video_search_by_pattern(
                pattern_channel=pattern_case_success)[
                0].video_channel,
            search_video_channel)

        # SEARCH BY DESCRIPTION PATTERN #
        # Search exact fail
        pattern_exact_fail = util_pattern_compile(
            search_video_description[1:2],
            exact=True, ignore_case=True)
        self.assertEqual(len(query_video_search_by_pattern(
            pattern_description=pattern_exact_fail)), 0)

        # Search exact successfully
        pattern_exact_success = util_pattern_compile(search_video_description,
                                                     exact=True,
                                                     ignore_case=True)
        res = query_video_search_by_pattern(
            pattern_description=pattern_exact_success)[0]
        self.assertEqual(res.video_description, search_video_description)

        # Search case fail
        pattern_case_fail = util_pattern_compile(
            search_video_description[1:2].upper(), exact=False,
            ignore_case=False)
        self.assertEqual(len(query_video_search_by_pattern(
            pattern_description=pattern_case_fail)), 0)

        # Search case successfully
        pattern_case_success = util_pattern_compile(
            search_video_description[1:2].upper(),
            exact=False, ignore_case=True)

        res = query_video_search_by_pattern(
            pattern_description=pattern_case_success)[0]
        self.assertEqual(res.video_description, search_video_description)

        # Raise Error: ErrorCode.MONGODB_EMPTY_PARAM
        with self.assertRaises(MongoError) as e:
            query_video_search_by_pattern()
        self.assertEqual(e.exception.error_code, ErrorCode.MONGODB_EMPTY_PARAM)

        # Raise Error: ErrorCode.MONGODB_RE_PATTERN_EXPECTED
        with self.assertRaises(MongoError) as e:
            query_video_search_by_pattern(video_title="1234")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_RE_PATTERN_EXPECTED)

        # Raise Error: ErrorCode.MONGODB_INVALID_SEARCH_PARAM
        with self.assertRaises(MongoError) as e:
            query_video_search_by_pattern(video_lmao=pattern_case_success)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_INVALID_SEARCH_PARAM)

    def test_k_query_video_search_by_aggregate(self):
        pipeline = [
            {"$unwind": "$video_tag"},
            {"$unwind": "$video_category"},
            {"$unwind": "$video_uri"},
            {
                "$match":
                    {
                        "video_tag": {"$in": ["politics"]},
                        "video_title": {"$regex": "Ha"},
                        "video_uri.video_uri_mid": ""
                    }
            }
        ]
        videos = query_video_search_by_aggregate(pipeline)
        self.assertEqual(videos[0]['video_title'],
                         self.data['const_video'][0]['video_title'])

        # Raise Error: ErrorCode.MONGODB_LIST_EXPECTED
        with self.assertRaises(MongoError) as e:
            query_video_search_by_aggregate("lol")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_LIST_EXPECTED)


class TestQueryVideoOp(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.data = util_tests_load_data()
        util_tests_clean_database()

    def test_a_query_video_op_create(self):
        vid = self.data['temp_video_op'][0]['video_id']
        op = query_video_op_create(
            user_id=self.data['temp_video_op'][0]['user_id'],
            video_id=vid)
        self.assertEqual(op.video_id, vid)

        # Raise Error: ErrorCode.MONGODB_USER_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_video_op_create(user_id="123456781234567812345678",
                                  video_id=self.data['temp_video_op'][0][
                                      'video_id'])
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_USER_NOT_FOUND)

        # Raise Error: ErrorCode.MONGODB_VIDEO_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_video_op_create(
                user_id=self.data['temp_video_op'][0]['user_id'],
                video_id="123456781234567812345678")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_VIDEO_NOT_FOUND)

        # Raise Error: ErrorCode.MONGODB_OP_EXISTS
        with self.assertRaises(MongoError) as e:
            query_video_op_create(
                user_id=self.data['temp_video_op'][0]['user_id'],
                video_id=self.data['temp_video_op'][0]['video_id'])
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_VIDEO_OP_EXISTS)

    def test_b_query_video_op_get_by_user_id(self):
        op = query_video_op_get_by_user_id(
            self.data['temp_video_op'][0]['user_id'])[0]
        self.assertEqual(op.video_id,
                         self.data['temp_video_op'][0]['video_id'])

    def test_c_query_video_op_get_by_video_id(self):
        op = query_video_op_get_by_video_id(
            self.data['temp_video_op'][0]['video_id'])[0]
        self.assertEqual(
            op.user_id, self.data['const_video_op'][0]['user_id'])

    def test_d_query_video_op_get_by_user_video(self):
        temp_video_op = query_video_op_get_by_user_video(
            user_id=self.data['temp_video_op'][0]['user_id'],
            video_id=self.data['temp_video_op'][0]['video_id'])[0].to_dict()
        self.assertEqual(temp_video_op['video_id'],
                         self.data['temp_video_op'][0]['video_id'])
        self.assertEqual(temp_video_op['user_id'],
                         self.data['temp_video_op'][0]['user_id'])

    def test_e_query_video_op_get_by_op_id(self):
        temp_video_op = query_video_op_get_by_user_video(
            user_id=self.data['temp_video_op'][0]['user_id'],
            video_id=self.data['temp_video_op'][0]['video_id'])[0].to_dict()
        temp_video_op_alter = query_video_op_get_by_op_id(
            temp_video_op['video_op_id'])
        self.assertEqual(temp_video_op_alter[0].to_dict()['video_op_id'],
                         temp_video_op['video_op_id'])

    def test_f_query_video_op_update_process(self):
        new_process = 777
        new_process_date = get_time_now_utc()
        temp_video_op = query_video_op_get_by_user_video(
            user_id=self.data['temp_video_op'][0]['user_id'],
            video_id=self.data['temp_video_op'][0]['video_id'])[0].to_dict()
        query_video_op_update_process(temp_video_op['video_op_id'],
                                      new_process,
                                      new_process_date)
        temp_video_op_new = \
            query_video_op_get_by_op_id(temp_video_op['video_op_id'])[0]
        self.assertEqual(temp_video_op_new.process, new_process)
        self.assertEqual(temp_video_op_new.process_date, new_process_date)

        # Raise Error: ErrorCode.MONGODB_VIDEO_OP_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_video_op_update_process("123456781234567812345678",
                                          new_process, new_process_date)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_VIDEO_OP_NOT_FOUND)

    def test_g_query_video_op_update_comment(self):
        new_comment = "this is just a new comment"
        new_comment_date = get_time_now_utc()
        temp_video_op = query_video_op_get_by_user_video(
            user_id=self.data['temp_video_op'][0]['user_id'],
            video_id=self.data['temp_video_op'][0]['video_id'])[0].to_dict()
        query_video_op_update_comment(temp_video_op['video_op_id'],
                                      new_comment,
                                      new_comment_date)
        temp_video_op_new = \
            query_video_op_get_by_op_id(temp_video_op['video_op_id'])[0]
        self.assertEqual(temp_video_op_new.comment, new_comment)
        self.assertEqual(temp_video_op_new.comment_date, new_comment_date)

        # Raise Error: ErrorCode.MONGODB_VIDEO_OP_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_video_op_update_comment("123456781234567812345678",
                                          new_comment, new_comment_date)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_VIDEO_OP_NOT_FOUND)

    def test_h_query_video_op_update_like(self):
        new_like_date = get_time_now_utc()
        temp_video_op = query_video_op_get_by_user_video(
            user_id=self.data['temp_video_op'][0]['user_id'],
            video_id=self.data['temp_video_op'][0]['video_id'])[0].to_dict()
        query_video_op_update_like(temp_video_op['video_op_id'], True,
                                   new_like_date)
        temp_video_op_new = \
            query_video_op_get_by_op_id(temp_video_op['video_op_id'])[0]
        self.assertEqual(temp_video_op_new.like, True)
        self.assertEqual(temp_video_op_new.like_date, new_like_date)

        new_like_date_2 = get_time_now_utc()
        query_video_op_update_like(temp_video_op['video_op_id'], False,
                                   new_like_date_2)
        temp_video_op_new_2 = \
            query_video_op_get_by_op_id(temp_video_op['video_op_id'])[0]
        self.assertEqual(temp_video_op_new_2.like, False)
        self.assertEqual(temp_video_op_new_2.like_date, new_like_date_2)

        # Raise Error: ErrorCode.MONGODB_VIDEO_OP_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_video_op_update_like("123456781234567812345678", True,
                                       new_like_date)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_VIDEO_OP_NOT_FOUND)

    def test_i_query_video_op_update_dislike(self):
        new_dislike_date = get_time_now_utc()
        temp_video_op = query_video_op_get_by_user_video(
            user_id=self.data['temp_video_op'][0]['user_id'],
            video_id=self.data['temp_video_op'][0]['video_id'])[0].to_dict()
        query_video_op_update_dislike(temp_video_op['video_op_id'], True,
                                      new_dislike_date)
        temp_video_op_new = \
            query_video_op_get_by_op_id(temp_video_op['video_op_id'])[0]
        self.assertEqual(temp_video_op_new.dislike, True)
        self.assertEqual(temp_video_op_new.dislike_date, new_dislike_date)

        new_dislike_date_2 = get_time_now_utc()
        query_video_op_update_dislike(temp_video_op['video_op_id'], False,
                                      new_dislike_date_2)
        temp_video_op_new_2 = \
            query_video_op_get_by_op_id(temp_video_op['video_op_id'])[0]
        self.assertEqual(temp_video_op_new_2.dislike, False)
        self.assertEqual(temp_video_op_new_2.dislike_date, new_dislike_date_2)

        # Raise Error: ErrorCode.MONGODB_VIDEO_OP_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_video_op_update_dislike("123456781234567812345678", True,
                                          new_dislike_date)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_VIDEO_OP_NOT_FOUND)

    def test_j_query_video_op_update_star(self):
        new_star_date = get_time_now_utc()
        temp_video_op = query_video_op_get_by_user_video(
            user_id=self.data['temp_video_op'][0]['user_id'],
            video_id=self.data['temp_video_op'][0]['video_id'])[0].to_dict()
        query_video_op_update_star(temp_video_op['video_op_id'], True,
                                   new_star_date)
        temp_video_op_new = \
            query_video_op_get_by_op_id(temp_video_op['video_op_id'])[0]
        self.assertEqual(temp_video_op_new.star, True)
        self.assertEqual(temp_video_op_new.star_date, new_star_date)

        new_star_date_2 = get_time_now_utc()
        query_video_op_update_star(temp_video_op['video_op_id'], False,
                                   new_star_date_2)
        temp_video_op_new_2 = \
            query_video_op_get_by_op_id(temp_video_op['video_op_id'])[0]
        self.assertEqual(temp_video_op_new_2.star, False)
        self.assertEqual(temp_video_op_new_2.star_date, new_star_date_2)

        # Raise Error: ErrorCode.MONGODB_VIDEO_OP_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_video_op_update_star("123456781234567812345678", False)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_VIDEO_OP_NOT_FOUND)

    def test_k_query_video_op_delete(self):
        temp_video_op = query_video_op_get_by_user_video(
            user_id=self.data['temp_video_op'][0]['user_id'],
            video_id=self.data['temp_video_op'][0]['video_id'])[0]
        self.assertEqual(
            query_video_op_delete(temp_video_op.to_dict()['video_op_id']), 1)

        # Raise Error: ErrorCode.MONGODB_VIDEO_OP_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_video_op_delete(temp_video_op.to_dict()['video_op_id'])
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_VIDEO_OP_NOT_FOUND)

    def test_l_query_video_op_search_comment_by_contains(self):
        video_op = query_video_op_search_comment_by_contains(
            self.data['const_video_op'][0]['comment'][1:10])[0].to_dict()
        self.assertEqual(video_op['user_id'],
                         self.data['const_video_op'][0]['user_id'])

    def test_m_query_video_op_search_comment_by_pattern(self):
        search_comment = self.data['const_video_op'][0]['comment']

        # Search exact fail
        pattern_exact_fail = util_pattern_compile(search_comment[1:10],
                                                  exact=True, ignore_case=True)
        self.assertEqual(
            len(query_video_op_search_comment_by_pattern(pattern_exact_fail)),
            0)

        # Search exact successfully
        pattern_exact_success = util_pattern_compile(search_comment,
                                                     exact=True,
                                                     ignore_case=True)
        self.assertEqual(
            query_video_op_search_comment_by_pattern(pattern_exact_success)[
                0].comment,
            search_comment)

        # Search case fail
        pattern_case_fail = util_pattern_compile(search_comment[1:10].upper(),
                                                 exact=False,
                                                 ignore_case=False)
        self.assertEqual(
            len(query_video_op_search_comment_by_pattern(pattern_case_fail)),
            0)

        # Search case successfully
        pattern_case_success = util_pattern_compile(
            search_comment[1:10].upper(), exact=False, ignore_case=True)
        self.assertEqual(
            query_video_op_search_comment_by_pattern(pattern_case_success)[
                0].comment,
            search_comment)

        # Raise Error: ErrorCode.MONGODB_VIDEO_OP_NOT_FOUND
        with self.assertRaises(MongoError) as e:
            query_video_op_search_comment_by_pattern("abc")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_RE_PATTERN_EXPECTED)

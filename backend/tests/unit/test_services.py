import unittest
from flask import Flask, g
from service.service_search import service_search_video, \
    service_search_user, service_search_user_by_contains, \
    service_search_video_by_pattern, service_search_user_by_aggregation, \
    service_search_user_by_pattern, service_search_video_by_aggregation, \
    service_search_video_by_contains
from service.service_user import service_user_reg, \
    service_user_get_star, service_user_get_process, service_user_get_like, \
    service_user_get_user, service_user_get_dislike, \
    service_user_get_comment, service_user_close, service_user_login, \
    service_user_update_info
from service.service_video import service_video_info, \
    service_video_delete, service_video_comments, service_video_dislikes, \
    service_video_likes, service_video_stars, service_video_update, \
    service_video_upload, service_video_get_by_user
from service.service_video_op import service_video_op_add_comment, \
    service_video_op_add_dislike, service_video_op_add_like, \
    service_video_op_add_process, service_video_op_add_star, \
    service_video_op_add_view, service_video_op_cancel_comment, \
    service_video_op_cancel_dislike, service_video_op_cancel_like, \
    service_video_op_cancel_process, service_video_op_cancel_star, \
    service_video_op_get_comment, service_video_op_get_process, \
    service_video_op_get_view, service_video_op_update_comment, \
    service_video_op_update_process, query_video_op_get_by_user_video, \
    query_video_op_create, service_video_op_get_by_user
from service.service_auth import service_auth_user_get, \
    service_auth_user_modify, service_auth_video_get, \
    service_auth_video_op_get, service_auth_hide_video, \
    service_auth_hide_user
from settings import config
from utils.util_tests import util_tests_python_version, \
    util_tests_load_data, util_tests_clean_database
from db.query_user import query_user_get_by_name, \
    query_user_get_by_id
from db.query_video import query_video_get_by_title, \
    query_video_get_by_video_id, query_video_create, \
    query_video_update
from db.query_video_op import query_video_op_get_by_video_id
from db.mongo import init_db
from models.model_errors import ErrorCode, ServiceError
from utils.util_time import get_time_now_utc
from utils.util_serializer import util_serializer_mongo_results_to_array


app = Flask(__name__)
app.config.from_object(config['test'])

with app.app_context():
    if 'db' not in g:
        g.db = init_db()


class TestServiceSearchUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        util_tests_clean_database() if util_tests_python_version() else exit()
        cls.data = util_tests_load_data()

    def test_search_user(self):
        # Search successfully with ignore_case
        self.assertEqual(
            service_search_user(name="ta", ignore_case=False)[0]['user_name'],
            self.data['const_user'][0]['user_name'])

        # Search successfully with exact (result = 0)
        self.assertEqual(
            len(service_search_user(name="milvu", exact=True)), 0)

        # Search successfully with ignore_case and exact
        self.assertEqual(
            service_search_user(name="milvUS", ignore_case=True,
                                exact=True)[0]['user_name'],
            self.data['const_user'][1]['user_name'])

        # Search successfully with custom pattern (pattern=True)
        self.assertEqual(
            service_search_user(name=".*ta.*", pattern=True)[0][
                'user_name'],
            self.data['const_user'][0]['user_name'])

        # Search successfully with aggregate
        pipeline = [
            {
                "$match":
                    {
                        "user_name": {"$regex": "yp"},
                        "user_status": "public"
                    }
            }
        ]
        result = service_search_user(aggregate=True,
                                     search_dict=pipeline)[0]['user_name']
        self.assertEqual(result, self.data['const_user'][0]['user_name'])

        # Raise Error: ErrorCode.SERVICE_PARAM_SLICE_NOT_SUPPORT
        with self.assertRaises(ServiceError) as e:
            service_search_user(slice=True)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_PARAM_SLICE_NOT_SUPPORT)

    def test_search_user_by_contains(self):
        user = self.data['const_user'][0]
        res = service_search_user_by_contains(user_id=user['_id']['$oid'])
        self.assertEqual(res[0]['user_name'], user['user_name'])
        res = service_search_user_by_contains(user_email=user['user_email'])
        self.assertEqual(res[0]['user_name'], user['user_name'])
        res = service_search_user_by_contains(
            user_first_name=user['user_detail']['user_first_name'])
        self.assertEqual(res[0]['user_name'], user['user_name'])
        res = service_search_user_by_contains(
            user_last_name=user['user_detail']['user_last_name'])
        self.assertEqual(res[0]['user_name'], user['user_name'])
        res = service_search_user_by_contains(
            user_phone=user['user_detail']['user_phone'])
        self.assertEqual(res[0]['user_name'], user['user_name'])
        res = service_search_user_by_contains(
            user_street1=user['user_detail']['user_street1'])
        self.assertEqual(res[0]['user_name'], user['user_name'])
        res = service_search_user_by_contains(
            user_street2=user['user_detail']['user_street2'])
        self.assertEqual(res[0]['user_name'], user['user_name'])
        res = service_search_user_by_contains(
            user_city=user['user_detail']['user_city'])
        self.assertEqual(res[0]['user_name'], user['user_name'])
        res = service_search_user_by_contains(
            user_state=user['user_detail']['user_state'])
        self.assertEqual(res[0]['user_name'], user['user_name'])
        res = service_search_user_by_contains(
            user_country=user['user_detail']['user_country'])
        self.assertEqual(res[0]['user_name'], user['user_name'])
        res = service_search_user_by_contains(
            user_zip=user['user_detail']['user_zip'])
        self.assertEqual(res[0]['user_name'], user['user_name'])
        res = service_search_user_by_contains(user_status=user['user_status'])
        self.assertEqual(res[0]['user_name'], user['user_name'])

        # Raise Error: ErrorCode.SERVICE_PARAM_SLICE_NOT_SUPPORT
        with self.assertRaises(ServiceError) as e:
            service_search_user_by_contains(user_lol="lol")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_SEARCH_PARAM)

    def test_search_user_by_pattern(self):
        user_email = self.data['const_user'][1]['user_email'][2:5]
        self.assertEqual(
            service_search_user(email=user_email,
                                ignore_case=False)[0]['user_name'],
            self.data['const_user'][1]['user_name'])

        user_detail = self.data['const_user'][1]['user_detail']
        user_first_name = user_detail['user_first_name'][1:3]
        user_last_name = user_detail['user_last_name'][1:3]

        self.assertEqual(
            service_search_user(first_name=user_first_name,
                                ignore_case=False)[0]['user_name'],
            self.data['const_user'][1]['user_name'])

        self.assertEqual(
            service_search_user(last_name=user_last_name,
                                ignore_case=False)[0]['user_name'],
            self.data['const_user'][1]['user_name'])

        user_phone = user_detail['user_phone'][2:5]
        self.assertEqual(
            service_search_user(phone=user_phone,
                                ignore_case=False)[0]['user_name'],
            self.data['const_user'][1]['user_name'])

        user_street1 = user_detail['user_street1']

        user2_detail = self.data['const_user'][0]['user_detail']
        user2_street2 = user2_detail['user_street2']
        self.assertEqual(service_search_user(
            street1=user_street1, exact=True)[0]['user_name'],
                         self.data['const_user'][1]['user_name'])

        self.assertEqual(service_search_user(
            street2=user2_street2, exact=True)[0]['user_name'],
                         self.data['const_user'][0]['user_name'])

        user_city = user_detail['user_city']
        user_state = user_detail['user_state']
        user_country = user_detail['user_country']
        user_zip = user_detail['user_zip']
        self.assertEqual(service_search_user(
            city=user_city, exact=True)[0]['user_name'],
                         self.data['const_user'][1]['user_name'])

        self.assertEqual(service_search_user(
            state=user_state, exact=True)[0]['user_name'],
                         self.data['const_user'][1]['user_name'])

        self.assertEqual(service_search_user(
            country=user_country, exact=True)[0]['user_name'],
                         self.data['const_user'][1]['user_name'])

        self.assertEqual(service_search_user(
            zip=user_zip, exact=True)[0]['user_name'],
                         self.data['const_user'][1]['user_name'])

        user2_status = self.data['const_user'][0]['user_status']
        self.assertEqual(service_search_user(
            status=user2_status, exact=True)[0]['user_name'],
                         self.data['const_user'][0]['user_name'])

        # Raise Error: ErrorCode.SERVICE_INVALID_SEARCH_PARAM
        with self.assertRaises(ServiceError) as e:
            service_search_user_by_pattern(pattern_lol="lol")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_PATTERN_SEARCH_NOT_SUPPORT)

    def test_search_user_by_aggregate(self):
        pipeline1 = [
            {
                "$match":
                    {
                        "user_name": {"$regex": "yp"},
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
            service_search_user_by_aggregation(pipeline1)[0]['user_name'],
            self.data['const_user'][0]['user_name'])
        self.assertEqual(
            service_search_user_by_aggregation(pipeline2)[0]['user_name'],
            self.data['const_user'][0]['user_name'])
        with self.assertRaises(ServiceError) as e:
            service_search_user_by_aggregation()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)


class TestServiceSearchVideo(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        util_tests_clean_database()
        cls.data = util_tests_load_data()

    def test_search_video(self):
        self.assertEqual(
            service_search_video(title="Xi")[0]['video_title'],
            self.data['const_video'][0]['video_title'],
            msg="Test Search Video: Title")

        self.assertEqual(len(service_search_video(
            title="xi", ignore_case=False)), 0,
            msg="Test Search Video: Title (not found)")

        self.assertEqual(
            len(service_search_video(title="Z")), 0,
            msg="Test Search Video: Title")

        self.assertEqual(
            service_search_video(video_category="A")[0][
                'video_title'],
            self.data['const_video'][0]['video_title'],
            msg="Test Search Video: Category")

        self.assertEqual(
            service_search_video(video_tag="O")[0]['video_title'],
            self.data['const_video'][0]['video_title'],
            msg="Test Search Video: Tag")

        self.assertEqual(
            service_search_video(title="a h", slice=True)[0][
                'video_title'],
            self.data['const_video'][0]['video_title'],
            msg="Test Search Video: Tag")

        self.assertEqual(
            service_search_video(title="i a", slice=True)[0][
                'video_title'],
            self.data['const_video'][0]['video_title'],
            msg="Test Search Video: Tag")

        self.assertEqual(
            service_search_video(title="i%20a", slice=True)[0][
                'video_title'],
            self.data['const_video'][0]['video_title'],
            msg="Test Search Video: Tag")

        # Search successfully with custom pattern (pattern=True)
        self.assertEqual(
            service_search_video(title=".*i.*", pattern=True)[0][
                'video_title'],
            self.data['const_video'][0]['video_title'])

        # Search successfully with aggregate
        pipeline = [
            {
                "$match":
                    {
                        "video_title": {"$regex": "Ha"},
                        "video_status": "public"
                    }
            }
        ]
        res = service_search_video(aggregate=True,
                                   search_dict=pipeline)
        self.assertEqual(res[0]['video_title'],
                         self.data['const_video'][0]['video_title'])

    def test_search_video_by_contains(self):
        video = self.data['const_video'][0]
        res = service_search_video_by_contains(video_id=video['_id']['$oid'])
        self.assertEqual(res[0]['video_title'], video['video_title'])
        res = service_search_video_by_contains(
            video_title=video['video_title'])
        self.assertEqual(res[0]['video_title'], video['video_title'])
        res = service_search_video_by_contains(
            video_channel=video['video_channel'][0:2])
        self.assertEqual(res[0]['video_title'], video['video_title'])
        res = service_search_video_by_contains(
            video_category=video['video_category'][0])
        self.assertEqual(res[0]['video_title'], video['video_title'])
        res = service_search_video_by_contains(video_tag=video['video_tag'][0])
        self.assertEqual(res[0]['video_title'], video['video_title'])
        res = service_search_video_by_contains(
            video_description=video['video_description'][1:4])
        self.assertEqual(res[0]['video_title'], video['video_title'])

        # Raise Error: ErrorCode.SERVICE_PARAM_SLICE_NOT_SUPPORT
        with self.assertRaises(ServiceError) as e:
            service_search_video_by_contains(video_lol="lol")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_SEARCH_PARAM)

    def test_search_video_by_pattern(self):
        video_channel = self.data['const_video'][0]['video_channel']

        self.assertEqual(
            service_search_video(channel=video_channel,
                                 exact=True)[0]['video_title'],
            self.data['const_video'][0]['video_title'])

        video = self.data['const_video'][0]
        video_description = video['video_description'][1:5]
        self.assertEqual(
            service_search_video(description=video_description,
                                 ignore_case=False)[0]['video_description'],
            self.data['const_video'][0]['video_description'])

        # Raise Error: ErrorCode.SERVICE_INVALID_SEARCH_PARAM
        with self.assertRaises(ServiceError) as e:
            service_search_video_by_pattern(pattern_lol="lol")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_PATTERN_SEARCH_NOT_SUPPORT)

    def test_search_video_by_aggregate(self):
        pipeline = [
            {
                "$match":
                    {
                        "video_title": {"$regex": "Xi"},
                        "video_status": "public"
                    }
            }
        ]
        self.assertEqual(
            service_search_video_by_aggregation(pipeline)[0]['video_title'],
            self.data['const_video'][0]['video_title'])
        with self.assertRaises(ServiceError) as e:
            service_search_video_by_aggregation()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)


class TestServiceUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        util_tests_clean_database()
        cls.data = util_tests_load_data()

    def test_a_service_user_reg(self):
        # Register successfully
        test_name = self.data['temp_user'][0]['user_name']
        test_password = self.data['temp_user'][0]['user_password']
        test_email = self.data['temp_user'][0]['user_email']

        self.assertEqual(service_user_reg(user_name=test_name,
                                          user_password=test_password,
                                          user_email=test_email)['user_name'],
                         self.data['temp_user'][0]['user_name'])

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_user_reg()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

    def test_b_service_user_login(self):
        # Check successfully with user name
        test_name = self.data['temp_user'][0]['user_name']
        test_password = self.data['temp_user'][0]['user_password']
        test_email = self.data['temp_user'][0]['user_email']

        # Check successfully with user email
        user = service_user_login(
            user_name=test_name, user_password=test_password)
        self.assertEqual(user['user_name'], test_name)

        user = service_user_login(
            user_email=test_email, user_password=test_password)
        self.assertEqual(user['user_name'], test_name)

        user = service_user_login(
            user=test_name, user_password=test_password)
        self.assertEqual(user['user_name'], test_name)

        user = service_user_login(
            user=test_email, user_password=test_password)
        self.assertEqual(user['user_name'], test_name)

        # Password Wrong
        with self.assertRaises(ServiceError) as e:
            service_user_login(user_name=test_name,
                               user_password="xxx")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_PASS_WRONG)

        with self.assertRaises(ServiceError) as e:
            service_user_login(user_email=test_email,
                               user_password="xxx")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_PASS_WRONG)

        with self.assertRaises(ServiceError) as e:
            service_user_login(user=test_name,
                               user_password="xxx")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_PASS_WRONG)

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_user_login()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.SERVICE_USER_NOT_FOUND
        test2_name = self.data['temp_user'][1]['user_name']
        test2_password = self.data['temp_user'][1]['user_password']
        test2_email = self.data['temp_user'][1]['user_email']
        with self.assertRaises(ServiceError) as e:
            service_user_login(user_name=test2_name,
                               user_password=test2_password)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_NOT_FOUND)

        with self.assertRaises(ServiceError) as e:
            service_user_login(user_email=test2_email,
                               user_password=test2_password)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_NOT_FOUND)

        with self.assertRaises(ServiceError) as e:
            service_user_login(user=test2_email,
                               user_password=test2_password)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_NOT_FOUND)

        # Raise Error: ErrorCode.SERVICE_USER_CLOSED
        test3_name = self.data['const_user'][3]['user_name']
        test3_email = self.data['const_user'][3]['user_email']
        with self.assertRaises(ServiceError) as e:
            service_user_login(user_name=test3_name,
                               user_password=test3_name)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_CLOSED)

        with self.assertRaises(ServiceError) as e:
            service_user_login(user_email=test3_email,
                               user_password=test3_name)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_CLOSED)

        with self.assertRaises(ServiceError) as e:
            service_user_login(user=test3_name,
                               user_password=test3_name)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_CLOSED)

    def test_c_service_user_get_user(self):
        # Get successfully
        res = service_user_get_user(
            self.data['const_user'][0]['_id']['$oid'])
        self.assertEqual(
            res['user_name'], self.data['const_user'][0]['user_name'])

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_user('some random user')
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Raise Error: ErrorCode.SERVICE_USER_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_user_get_user('123456781234567812345678')
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_NOT_FOUND)

    def test_d_service_user_get_like(self):
        # Get successfully
        res = service_user_get_like(self.data['const_user'][0]['_id']['$oid'])
        self.assertEqual(len(res), 1)

        # no video op
        res = service_user_get_like(self.data['const_user'][1]['_id']['$oid'])
        self.assertEqual(len(res), 0)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_like('some random user')
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Raise Error: ErrorCode.SERVICE_USER_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_user_get_like('123456781234567812345678')
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_NOT_FOUND)

    def test_e_service_user_get_dislike(self):
        # Get successfully
        oid = self.data['const_user'][0]['_id']['$oid']
        res = service_user_get_dislike(oid)
        self.assertEqual(res[0]['user_id'],
                         self.data['const_user'][0]['_id']['$oid'])

        # no video op
        temp_id = self.data['const_user'][1]['_id']['$oid']
        res = service_user_get_dislike(temp_id)
        self.assertEqual(len(res), 0)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_dislike('some random user')
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Raise Error: ErrorCode.SERVICE_USER_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_user_get_dislike('123456781234567812345678')
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_NOT_FOUND)

    def test_f_service_user_get_comment(self):
        # Get successfully
        oid = self.data['const_user'][0]['_id']['$oid']
        res = service_user_get_comment(oid)
        self.assertEqual(res[0]['user_id'],
                         self.data['const_user'][0]['_id']['$oid'])

        # no video op
        temp_id = self.data['const_user'][1]['_id']['$oid']
        res = service_user_get_comment(temp_id)
        self.assertEqual(len(res), 0)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_comment('some random user')
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Raise Error: ErrorCode.SERVICE_USER_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_user_get_comment('123456781234567812345678')
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_NOT_FOUND)

    def test_g_service_user_get_star(self):
        # Get successfully
        res = service_user_get_star(self.data['const_user'][0]['_id']['$oid'])
        self.assertEqual(len(res), 1)

        # no video op
        res = service_user_get_star(self.data['const_user'][1]['_id']['$oid'])
        self.assertEqual(len(res), 0)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_star('some random user')
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Raise Error: ErrorCode.SERVICE_USER_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_user_get_star('123456781234567812345678')
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_NOT_FOUND)

    def test_h_service_user_get_process(self):
        # Get successfully
        oid = self.data['const_user'][0]['_id']['$oid']
        res = service_user_get_process(oid)
        self.assertEqual(len(res), 1)

        # no video op
        temp_id = self.data['const_user'][1]['_id']['$oid']
        res = service_user_get_process(temp_id)
        self.assertEqual(len(res), 0)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_process('some random user')
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Raise Error: ErrorCode.SERVICE_USER_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_user_get_process('123456781234567812345678')
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_NOT_FOUND)

    def test_i_service_user_update_info(self):
        test_name = self.data['temp_user'][0]['user_name']
        test_password = self.data['temp_user'][0]['user_password']
        test_email = self.data['temp_user'][0]['user_email']

        with self.assertRaises(ServiceError) as e:
            service_user_update_info(
                user_name=test_name, user_password="xxx")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_USER_ID)

        user = query_user_get_by_name(test_name)[0].to_dict()
        service_user_update_info(
            user_id=user['user_id'],
            user_name="lolo",
            user_email="lolo@gmail.com",
            user_password="lolo",
            user_thumbnail="thumbnail"
        )
        user = query_user_get_by_id(user['user_id'])[0].to_dict()
        self.assertEqual(user['user_name'], "lolo")
        service_user_update_info(
            user_id=user['user_id'],
            user_name=test_name,
            user_email=test_email,
            user_password=test_password,
            user_thumbnail="thumbnail"
        )
        user = query_user_get_by_id(user['user_id'])[0].to_dict()
        self.assertEqual(user['user_name'], test_name)

    def test_z_service_user_close(self):
        users = query_user_get_by_name(
            user_name=self.data['temp_user'][0]['user_name'])
        user_id = users[0].to_dict()['user_id']
        self.assertEqual(service_user_close(user_id=user_id), 1)

        with self.assertRaises(ServiceError) as e:
            service_user_close()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_USER_ID)


class TestServiceVideo(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        util_tests_clean_database()
        cls.data = util_tests_load_data()

        cls.temp_video_title = "test video title"
        cls.temp_video_raw_content = \
            "https://s3.amazon.com/test_video_content.avi"

        cls.temp_video_title_updated = "test video title updated"
        cls.temp_video_status = "public"
        cls.temp_video_raw_size = 51.23
        cls.const_vid = cls.data['const_video'][0]['_id']['$oid']

    def test_a_service_video_upload(self):
        test_user_id = self.data['const_user'][1]['_id']['$oid']
        vid = service_video_upload(test_user_id)
        query_video_update(
            vid,
            video_title=self.temp_video_title,
            video_raw_content=self.temp_video_raw_content)
        self.assertEqual(type(vid), str)
        self.assertEqual(len(vid), 24)

        # Simply create a video op for testing
        query_video_op_create(
            user_id=self.data['const_user'][1]['_id']['$oid'],
            video_id=vid,
            init_time=get_time_now_utc())

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_video_upload("1234")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

    def test_b_service_video_info(self):
        temp_video_id = query_video_get_by_title(
            self.temp_video_title)[0].to_dict()['video_id']
        self.assertEqual(service_video_info(
            video_id=temp_video_id)['video_title'],
            self.temp_video_title)

        # Raise Error: ErrorCode.SERVICE_VIDEO_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_video_info()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

    def test_c_service_video_get_by_user(self):
        temp_user_id = query_video_get_by_title(
            self.temp_video_title)[0].to_dict()['user_id']
        self.assertEqual(
            service_video_get_by_user(user_id=temp_user_id)[0]['video_title'],
            self.temp_video_title)

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_get_by_user()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_video_get_by_user(user_id="123321")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

    def test_d_service_video_update(self):
        temp_video_id = query_video_get_by_title(
            self.temp_video_title)[0].to_dict()['video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_update()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.SERVICE_VIDEO_INVALID_STATUS
        with self.assertRaises(ServiceError) as e:
            service_video_update(video_id=temp_video_id,
                                 video_title=self.temp_video_title_updated,
                                 video_status="invalid",
                                 video_raw_size=self.temp_video_raw_size)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_VIDEO_INVALID_STATUS)

        # Raise Error: ErrorCode.SERVICE_VIDEO_INVALID_STATUS
        with self.assertRaises(ServiceError) as e:
            service_video_update(video_id=temp_video_id,
                                 video_raw_status="invalid")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_VIDEO_INVALID_STATUS)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_video_update(video_id="123321",
                                 video_title=self.temp_video_title_updated,
                                 video_status=self.temp_video_status,
                                 video_raw_size=self.temp_video_raw_size)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful case
        self.assertEqual(
            service_video_update(video_id=temp_video_id,
                                 video_title=self.temp_video_title_updated,
                                 video_status=self.temp_video_status,
                                 video_raw_size=self.temp_video_raw_size)[
                0].to_dict()['video_raw_size'],
            self.temp_video_raw_size)

        self.assertEqual(
            service_video_update(video_id=temp_video_id,
                                 video_title=self.temp_video_title)[
                0].to_dict()['video_title'],
            self.temp_video_title)

    def test_e_service_video_comments(self):
        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_comments()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_video_comments(video_id="123321")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful case
        self.assertEqual(
            len(service_video_comments(video_id=self.const_vid)), 1)

        self.assertEqual(len(service_video_comments(
            video_id="123456781234567812345678")), 0)

    def test_f_service_video_likes(self):
        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_likes()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_video_likes(video_id="123321")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful case
        self.assertEqual(len(service_video_likes(
            video_id=self.const_vid)), 1)

        self.assertEqual(len(service_video_likes(
            video_id="123456781234567812345678")), 0)

    def test_g_service_video_dislikes(self):
        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_dislikes()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_video_dislikes(video_id="123321")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful case
        self.assertEqual(len(service_video_dislikes(
            video_id=self.const_vid)), 1)

        self.assertEqual(len(service_video_dislikes(
            video_id="123456781234567812345678")), 0)

    def test_h_service_video_stars(self):
        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_stars()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_video_stars(video_id="123321")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful case
        self.assertEqual(len(service_video_stars(
            video_id=self.const_vid)), 1)

        self.assertEqual(len(service_video_stars(
            video_id="123456781234567812345678")), 0)

    def test_i_service_video_delete(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_delete()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_video_delete(video_id="123321")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful case
        self.assertEqual(
            service_video_delete(video_id=temp_video_id), 1)
        self.assertEqual(len(query_video_op_get_by_video_id(temp_video_id)), 0)


class TestServiceVideoOp(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        util_tests_clean_database()
        cls.data = util_tests_load_data()

        # create a temp video
        cls.temp_video_title = "video op test"
        cls.temp_video_raw_content = \
            "https://s3.amazon.com/test_video_content.avi"

        videos = query_video_get_by_title(cls.temp_video_title)
        if len(videos) == 0:
            vid = query_video_create(cls.data['const_user'][0]['_id']['$oid'])
            query_video_update(
                vid,
                video_title=cls.temp_video_title,
                video_raw_content=cls.temp_video_raw_content)

        temp_video_id = query_video_get_by_title(
            cls.temp_video_title)[0].to_dict()['video_id']

        # create a video op for the video
        ops = query_video_op_get_by_user_video(
            user_id=cls.data['const_user'][1]['_id']['$oid'],
            video_id=temp_video_id)

        if len(ops) == 0:
            query_video_op_create(
                user_id=cls.data['const_user'][1]['_id']['$oid'],
                video_id=temp_video_id,
                init_time=get_time_now_utc())

    def test_0_service_video_op_get_by_user(self):
        op_0 = service_video_op_get_by_user(
            user_id=self.data['const_user'][0]['_id']['$oid'])
        op_1 = service_video_op_get_by_user(
            user_id=self.data['const_user'][2]['_id']['$oid'])
        self.assertEqual(len(op_0), 1)
        self.assertEqual(len(op_1), 0)
        with self.assertRaises(ServiceError) as e:
            service_video_op_get_by_user()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

    def test_a_service_video_op_add_view(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_add_view()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_add_view(video_id="123123")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        original_view = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_view"]
        current_view = \
            service_video_op_add_view(video_id=temp_video_id)[
                "view_count"]
        self.assertEqual(original_view + 1, current_view)

    def test_b_service_video_op_get_view(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_get_view()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_get_view(video_id="123123")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Raise Error: ErrorCode.SERVICE_VIDEO_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_video_op_get_view(video_id="123456781234567812345678")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_VIDEO_NOT_FOUND)

        # Successful test
        original_view = query_video_get_by_video_id(
            temp_video_id)[0].to_dict()["video_view"]
        current_view = service_video_op_get_view(
            video_id=temp_video_id)["view_count"]
        self.assertEqual(original_view, current_view)

    def test_c_service_video_op_add_comment(self):
        temp_video_id = query_video_get_by_title(
            self.temp_video_title)[0].to_dict()['video_id']
        temp_comment = "test comment"

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_add_comment()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_add_comment(video_id="123123",
                                         user_id="aaa", comment="")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        original_comment = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_comment"]

        test_id = self.data['const_user'][1]['_id']['$oid']
        response = service_video_op_add_comment(video_id=temp_video_id,
                                                user_id=test_id,
                                                comment=temp_comment)
        current_comment = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_comment"]

        self.assertEqual(current_comment, original_comment + 1)
        self.assertEqual(temp_comment, response["comment"])

    def test_d_service_video_op_get_comment(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_video_op_get_comment(user_id="111", video_id="111")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_get_comment()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_cancel_comment(video_id="123123",
                                            user_id="aaa")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        original_comment = query_video_op_get_by_user_video(
            self.data['const_user'][1]['_id']['$oid'],
            temp_video_id)[0].to_dict()["comment"]

        test_id = self.data['const_user'][1]['_id']['$oid']
        response = service_video_op_get_comment(video_id=temp_video_id,
                                                user_id=test_id)

        self.assertEqual(original_comment, response["comment"])

    def test_e_service_video_op_update_comment(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']
        temp_comment = "test comment"

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_update_comment()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_update_comment(video_id="123123",
                                            user_id="aaa", comment="")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        test_id = self.data['const_user'][1]['_id']['$oid']
        response = service_video_op_update_comment(video_id=temp_video_id,
                                                   user_id=test_id,
                                                   comment=temp_comment)
        self.assertEqual(temp_comment, response["comment"])

    def test_f_service_video_op_cancel_comment(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_cancel_comment()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.SERVICE_VIDEO_OP_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_video_op_cancel_comment(
                user_id=self.data['const_user'][2]['_id']['$oid'],
                video_id=self.data['const_video'][1]['_id']['$oid']
            )
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_VIDEO_OP_NOT_FOUND)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_cancel_comment(video_id="123123",
                                            user_id="aaa")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        original_comment = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_comment"]

        test_id = self.data['const_user'][1]['_id']['$oid']
        response = service_video_op_cancel_comment(video_id=temp_video_id,
                                                   user_id=test_id)
        current_comment = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_comment"]

        self.assertEqual(current_comment, original_comment - 1)
        self.assertEqual(response["comment"], "")

    def test_g_service_video_op_add_process(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']
        temp_process = 30

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_add_process()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_add_process(video_id="123123",
                                         user_id="aaa", process=30)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        with self.assertRaises(ServiceError) as e:
            test_id = self.data['const_user'][1]['_id']['$oid']
            service_video_op_add_process(video_id=temp_video_id,
                                         user_id=test_id, process=-100)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_SEARCH_PARAM)

        # Successful test
        test_id = self.data['const_user'][1]['_id']['$oid']
        response = service_video_op_add_process(video_id=temp_video_id,
                                                user_id=test_id,
                                                process=temp_process)
        self.assertEqual(temp_process, response["process"])

    def test_h_service_video_op_get_process(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_get_process()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_get_process(video_id="123123",
                                         user_id="aaa")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        original_process = query_video_op_get_by_user_video(
            self.data['const_user'][1]['_id']['$oid'],
            temp_video_id)[0].to_dict()["process"]
        test_id = self.data['const_user'][1]['_id']['$oid']
        response = service_video_op_get_process(video_id=temp_video_id,
                                                user_id=test_id)
        self.assertEqual(original_process, response["process"])

    def test_i_service_video_op_update_process(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']
        temp_process = 60

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_update_process()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_update_process(video_id="123123",
                                            user_id="aaa", process=30)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        with self.assertRaises(ServiceError) as e:
            test_id = self.data['const_user'][1]['_id']['$oid']
            service_video_op_update_process(video_id=temp_video_id,
                                            user_id=test_id, process=-100)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_SEARCH_PARAM)

        # Successful test
        test_id = self.data['const_user'][1]['_id']['$oid']
        response = service_video_op_update_process(video_id=temp_video_id,
                                                   user_id=test_id,
                                                   process=temp_process)
        self.assertEqual(temp_process, response["process"])

    def test_j_service_video_op_cancel_process(self):
        temp_video_id = query_video_get_by_title(
            self.temp_video_title)[0].to_dict()['video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_cancel_process()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_cancel_process(video_id="123123",
                                            user_id="aaa")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        test_id = self.data['const_user'][1]['_id']['$oid']
        response = service_video_op_cancel_process(video_id=temp_video_id,
                                                   user_id=test_id)
        self.assertEqual(response["process"], 0)

    def test_k_service_video_op_add_like(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_add_like()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_add_like(video_id="123123",
                                      user_id="aaa")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        original_like = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_like"]
        test_id = self.data['const_user'][1]['_id']['$oid']
        response = service_video_op_add_like(video_id=temp_video_id,
                                             user_id=test_id)
        current_like = query_video_get_by_video_id(temp_video_id)[0].to_dict()[
            "video_like"]
        self.assertEqual(response["like"], True)
        self.assertEqual(response["dislike"], False)
        self.assertEqual(original_like + 1, current_like)

        # Raise Error: ErrorCode.SERVICE_VIDEO_LIKE_UPDATE_FAILURE
        with self.assertRaises(ServiceError) as e:
            test_id = self.data['const_user'][1]['_id']['$oid']
            service_video_op_add_like(video_id=temp_video_id,
                                      user_id=test_id)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_VIDEO_LIKE_UPDATE_FAILURE)

        # If already dislike, can switch to like
        original_like = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_like"]
        original_dislike = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_dislike"]
        test_id = self.data['const_user'][1]['_id']['$oid']
        service_video_op_add_dislike(video_id=temp_video_id,
                                     user_id=test_id)
        response = service_video_op_add_like(video_id=temp_video_id,
                                             user_id=test_id)
        current_like = query_video_get_by_video_id(temp_video_id)[0].to_dict()[
            "video_like"]
        current_dislike = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_dislike"]
        self.assertEqual(response["like"], True)
        self.assertEqual(response["dislike"], False)
        self.assertEqual(original_like, current_like)
        self.assertEqual(original_dislike, current_dislike)

    def test_l_service_video_op_cancel_like(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_cancel_like()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_cancel_like(video_id="123123",
                                         user_id="aaa")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        original_like = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_like"]

        test_id = self.data['const_user'][1]['_id']['$oid']
        response = service_video_op_cancel_like(video_id=temp_video_id,
                                                user_id=test_id)
        current_like = query_video_get_by_video_id(temp_video_id)[0].to_dict()[
            "video_like"]
        self.assertEqual(response["like"], False)
        self.assertEqual(response["dislike"], False)
        self.assertEqual(original_like - 1, current_like)

        # Raise Error: ErrorCode.SERVICE_VIDEO_LIKE_UPDATE_FAILURE
        with self.assertRaises(ServiceError) as e:
            test_id = self.data['const_user'][1]['_id']['$oid']
            service_video_op_cancel_like(video_id=temp_video_id,
                                         user_id=test_id)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_VIDEO_LIKE_UPDATE_FAILURE)

    def test_m_service_video_op_add_dislike(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_add_dislike()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_add_dislike(video_id="123123",
                                         user_id="aaa")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        original_dislike = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_dislike"]
        test_id = self.data['const_user'][1]['_id']['$oid']
        response = service_video_op_add_dislike(video_id=temp_video_id,
                                                user_id=test_id)
        current_dislike = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_dislike"]
        self.assertEqual(response["like"], False)
        self.assertEqual(response["dislike"], True)
        self.assertEqual(original_dislike + 1, current_dislike)

        # Raise Error: ErrorCode.SERVICE_VIDEO_DISLIKE_UPDATE_FAILURE
        with self.assertRaises(ServiceError) as e:
            test_id = self.data['const_user'][1]['_id']['$oid']
            service_video_op_add_dislike(video_id=temp_video_id,
                                         user_id=test_id)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_VIDEO_DISLIKE_UPDATE_FAILURE)

        # If already like, can switch to dislike
        original_like = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_like"]
        original_dislike = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_dislike"]
        test_id = self.data['const_user'][1]['_id']['$oid']
        service_video_op_add_like(video_id=temp_video_id,
                                  user_id=test_id)
        response = service_video_op_add_dislike(video_id=temp_video_id,
                                                user_id=test_id)
        current_like = query_video_get_by_video_id(temp_video_id)[0].to_dict()[
            "video_like"]
        current_dislike = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_dislike"]
        self.assertEqual(response["like"], False)
        self.assertEqual(response["dislike"], True)
        self.assertEqual(original_like, current_like)
        self.assertEqual(original_dislike, current_dislike)

    def test_n_service_video_op_cancel_dislike(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_cancel_dislike()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_cancel_dislike(video_id="123123",
                                            user_id="aaa")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        original_dislike = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_dislike"]
        test_id = self.data['const_user'][1]['_id']['$oid']
        response = service_video_op_cancel_dislike(video_id=temp_video_id,
                                                   user_id=test_id)
        current_dislike = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_dislike"]
        self.assertEqual(response["like"], False)
        self.assertEqual(response["dislike"], False)
        self.assertEqual(original_dislike - 1, current_dislike)

        # Raise Error: ErrorCode.SERVICE_VIDEO_DISLIKE_UPDATE_FAILURE
        with self.assertRaises(ServiceError) as e:
            test_id = self.data['const_user'][1]['_id']['$oid']
            service_video_op_cancel_dislike(video_id=temp_video_id,
                                            user_id=test_id)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_VIDEO_DISLIKE_UPDATE_FAILURE)

    def test_o_service_video_op_add_star(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_add_star()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_add_star(video_id="123123",
                                      user_id="aaa")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        original_star = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_star"]
        test_id = self.data['const_user'][1]['_id']['$oid']
        response = service_video_op_add_star(video_id=temp_video_id,
                                             user_id=test_id)
        current_star = query_video_get_by_video_id(temp_video_id)[0].to_dict()[
            "video_star"]
        self.assertEqual(response["star"], True)
        self.assertEqual(original_star + 1, current_star)

        # Raise Error: ErrorCode.SERVICE_VIDEO_DISLIKE_UPDATE_FAILURE
        with self.assertRaises(ServiceError) as e:
            test_id = self.data['const_user'][1]['_id']['$oid']
            service_video_op_add_star(video_id=temp_video_id,
                                      user_id=test_id)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_VIDEO_STAR_UPDATE_FAILURE)

    def test_p_service_video_op_cancel_star(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_cancel_star()
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_cancel_star(video_id="123123",
                                         user_id="aaa")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        original_star = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_star"]
        test_id = self.data['const_user'][1]['_id']['$oid']
        response = service_video_op_cancel_star(video_id=temp_video_id,
                                                user_id=test_id)
        current_star = query_video_get_by_video_id(temp_video_id)[0].to_dict()[
            "video_star"]
        self.assertEqual(response["star"], False)
        self.assertEqual(original_star - 1, current_star)

        # Raise Error: ErrorCode.SERVICE_VIDEO_DISLIKE_UPDATE_FAILURE
        with self.assertRaises(ServiceError) as e:
            test_id = self.data['const_user'][1]['_id']['$oid']
            service_video_op_cancel_star(video_id=temp_video_id,
                                         user_id=test_id)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_VIDEO_STAR_UPDATE_FAILURE)

    def test_z_delete_testing_data(self):
        temp_video_id = query_video_get_by_title(
            self.temp_video_title)[0].to_dict()['video_id']
        service_video_delete(video_id=temp_video_id)


class TestServiceAuth(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        util_tests_clean_database()
        cls.data = util_tests_load_data()

    def test_a_service_auth_user_get(self):
        uid = self.data['const_user'][2]['_id']['$oid']
        fake = '123456781234567812345678'
        self.assertEqual(service_auth_user_get(uid, uid), True)
        self.assertEqual(service_auth_user_get(fake, uid), False)
        with self.assertRaises(ServiceError) as e:
            service_auth_user_get(uid, fake)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_NOT_FOUND)

    def test_b_service_auth_user_modify(self):
        uid = self.data['const_user'][0]['_id']['$oid']
        self.assertEqual(service_auth_user_modify(uid, uid), True)

    def test_c_service_auth_video_get(self):
        uid = self.data['const_user'][0]['_id']['$oid']
        vid = self.data['const_video'][0]['_id']['$oid']
        self.assertEqual(service_auth_video_get(uid, vid), True)

        uid = self.data['const_user'][0]['_id']['$oid']
        vid = self.data['const_video'][3]['_id']['$oid']
        self.assertEqual(service_auth_video_get(uid, vid), False)

    def test_d_service_auth_video_modify(self):
        pass

    def test_e_service_auth_video_op_get(self):
        uid = self.data['const_user'][0]['_id']['$oid']
        vid = self.data['const_video'][0]['_id']['$oid'][1:]
        with self.assertRaises(ServiceError) as e:
            service_auth_video_op_get(uid, uid, '1' + vid)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_VIDEO_NOT_FOUND)

    def test_f_service_auth_video_op_post(self):
        uid = self.data['const_user'][0]['_id']['$oid']
        vid = self.data['const_video'][0]['_id']['$oid']
        with self.assertRaises(ServiceError) as e:
            service_auth_video_op_get(uid, uid, '1' + vid[1:])
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_VIDEO_NOT_FOUND)

        with self.assertRaises(ServiceError) as e:
            service_auth_video_op_get(uid, uid, vid[:-2] + '00')
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_VIDEO_NOT_FOUND)

    def test_g_service_auth_video_op_modify(self):
        pass

    def test_h_service_auth_hide_video(self):
        uid = self.data['const_user'][0]['_id']['$oid']
        vid = self.data['const_video'][3]['_id']['$oid']
        res = query_video_get_by_video_id(vid)
        res = util_serializer_mongo_results_to_array(res)
        vid = self.data['const_video'][3]['_id']['$oid']
        res2 = query_video_get_by_video_id(vid)
        res2 = util_serializer_mongo_results_to_array(res2)
        res.append(res2[0])
        res = service_auth_hide_video(uid, res)
        self.assertEqual(len(res), 0)

    def test_i_service_auth_hide_user(self):
        uid = self.data['const_user'][3]['_id']['$oid']
        res = query_user_get_by_id(uid)
        res = util_serializer_mongo_results_to_array(res)
        uid = self.data['const_user'][0]['_id']['$oid']
        res = service_auth_hide_user(uid, res)
        self.assertEqual(len(res), 0)

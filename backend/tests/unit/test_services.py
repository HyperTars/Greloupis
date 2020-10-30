import unittest
from service.service_search import service_search_video, \
    service_search_user, service_search_user_by_contains, \
    service_search_video_by_pattern, service_search_user_by_aggregation, \
    service_search_user_by_pattern, service_search_video_by_aggregation, \
    service_search_video_by_contains
from service.service_user import service_user_reg, \
    service_user_get_star, service_user_get_process, service_user_get_like, \
    service_user_get_info, service_user_get_dislike, \
    service_user_get_comment, service_user_check_password, service_user_cancel
from service.service_video import service_video_info, \
    service_video_delete, service_video_comments, service_video_dislikes, \
    service_video_likes, service_video_stars, service_video_update, \
    service_video_upload
from service.service_video_op import service_video_op_add_comment, \
    service_video_op_add_dislike, service_video_op_add_like, \
    service_video_op_add_process, service_video_op_add_star, \
    service_video_op_add_view, service_video_op_cancel_comment, \
    service_video_op_cancel_dislike, service_video_op_cancel_like, \
    service_video_op_cancel_process, service_video_op_cancel_star, \
    service_video_op_get_comment, service_video_op_get_process, \
    service_video_op_get_view, service_video_op_update_comment, \
    service_video_op_update_process, query_video_op_get_by_user_video, \
    query_video_op_create
from settings import config
from utils.util_tests import util_tests_python_version, \
    util_tests_load_data
from db.query_user import query_user_get_by_name
from db.query_video import query_video_get_by_title, \
    query_video_get_by_video_id
from db.query_video_op import query_video_op_get_by_video_id
from models.model_errors import ErrorCode, MongoError, ServiceError
from utils.util_time import get_time_now_utc


class TestServiceSearchUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if util_tests_python_version() is False:
            exit()
        cls.data = util_tests_load_data()
        cls.conf = config['test']

    def test_search_user(self):
        # Search successfully with ignore_case
        self.assertEqual(
            service_search_user(self.conf, name="t", ignore_case=False)[0][
                'user_name'],
            self.data['const_user'][0]['user_name'])

        # Search successfully with exact (result = 0)
        self.assertEqual(
            len(service_search_user(self.conf, name="milvu", exact=True)), 0)

        # Search successfully with ignore_case and exact
        self.assertEqual(
            service_search_user(self.conf, name="milvUS", ignore_case=True,
                                exact=True)[0]['user_name'],
            self.data['const_user'][1]['user_name'])

        # Search successfully with custom pattern (pattern=True)
        self.assertEqual(
            service_search_user(self.conf, name=".*t.*", pattern=True)[0][
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
        self.assertEqual(service_search_user(self.conf, aggregate=True,
                                             search_dict=pipeline)[0][
                             'user_name'],
                         self.data['const_user'][0]['user_name'])

        # Raise Error: ErrorCode.SERVICE_PARAM_SLICE_NOT_SUPPORT
        with self.assertRaises(ServiceError) as e:
            service_search_user(self.conf, slice=True)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_PARAM_SLICE_NOT_SUPPORT)

    def test_search_user_by_contains(self):
        user = self.data['const_user'][0]
        self.assertEqual(
            service_search_user_by_contains(user_id=user['_id']['$oid'])[0][
                'user_name'],
            user['user_name'])
        self.assertEqual(
            service_search_user_by_contains(user_email=user['user_email'])[0][
                'user_name'],
            user['user_name'])
        self.assertEqual(service_search_user_by_contains(
            user_first_name=user['user_detail']['user_first_name'])
                         [0]['user_name'], user['user_name'])
        self.assertEqual(service_search_user_by_contains(
            user_last_name=user['user_detail']['user_last_name'])
                         [0]['user_name'], user['user_name'])
        self.assertEqual(service_search_user_by_contains(
            user_phone=user['user_detail']['user_phone'])
                         [0]['user_name'], user['user_name'])
        self.assertEqual(service_search_user_by_contains(
            user_street1=user['user_detail']['user_street1'])
                         [0]['user_name'], user['user_name'])
        self.assertEqual(service_search_user_by_contains(
            user_street2=user['user_detail']['user_street2'])
                         [0]['user_name'], user['user_name'])
        self.assertEqual(service_search_user_by_contains(
            user_city=user['user_detail']['user_city'])
                         [0]['user_name'], user['user_name'])
        self.assertEqual(service_search_user_by_contains(
            user_state=user['user_detail']['user_state'])
                         [0]['user_name'], user['user_name'])
        self.assertEqual(service_search_user_by_contains(
            user_country=user['user_detail']['user_country'])
                         [0]['user_name'], user['user_name'])
        self.assertEqual(service_search_user_by_contains(
            user_zip=user['user_detail']['user_zip'])
                         [0]['user_name'], user['user_name'])
        self.assertEqual(
            service_search_user_by_contains(user_status=user['user_status'])
            [0]['user_name'], user['user_name'])

        # Raise Error: ErrorCode.SERVICE_PARAM_SLICE_NOT_SUPPORT
        with self.assertRaises(ServiceError) as e:
            service_search_user_by_contains(user_lol="lol")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_SEARCH_PARAM)

    def test_search_user_by_pattern(self):
        user_email = self.data['const_user'][1]['user_email'][2:5]
        self.assertEqual(
            service_search_user(self.conf,
                                email=user_email,
                                ignore_case=False)[0]['user_name'],
            self.data['const_user'][1]['user_name'])

        user_detail = self.data['const_user'][1]['user_detail']
        user_first_name = user_detail['user_first_name'][1:3]
        user_last_name = user_detail['user_last_name'][1:3]

        self.assertEqual(
            service_search_user(self.conf,
                                first_name=user_first_name,
                                ignore_case=False)[0]['user_name'],
            self.data['const_user'][1]['user_name'])

        self.assertEqual(
            service_search_user(self.conf,
                                last_name=user_last_name,
                                ignore_case=False)[0]['user_name'],
            self.data['const_user'][1]['user_name'])

        user_phone = user_detail['user_phone'][2:5]
        self.assertEqual(
            service_search_user(self.conf,
                                phone=user_phone,
                                ignore_case=False)[0]['user_name'],
            self.data['const_user'][1]['user_name'])

        user_street1 = user_detail['user_street1']

        user2_detail = self.data['const_user'][0]['user_detail']
        user2_street2 = user2_detail['user_street2']
        self.assertEqual(service_search_user(self.conf,
                                             street1=user_street1,
                                             exact=True)[0]['user_name'],
                         self.data['const_user'][1]['user_name'])

        self.assertEqual(service_search_user(self.conf,
                                             street2=user2_street2,
                                             exact=True)[0]['user_name'],
                         self.data['const_user'][0]['user_name'])

        user_city = user_detail['user_city']
        user_state = user_detail['user_state']
        user_country = user_detail['user_country']
        user_zip = user_detail['user_zip']
        self.assertEqual(service_search_user(self.conf,
                                             city=user_city,
                                             exact=True)[0]['user_name'],
                         self.data['const_user'][1]['user_name'])

        self.assertEqual(service_search_user(self.conf,
                                             state=user_state,
                                             exact=True)[0]['user_name'],
                         self.data['const_user'][1]['user_name'])

        self.assertEqual(service_search_user(self.conf,
                                             country=user_country,
                                             exact=True)[0]['user_name'],
                         self.data['const_user'][1]['user_name'])

        self.assertEqual(service_search_user(self.conf,
                                             zip=user_zip,
                                             exact=True)[0]['user_name'],
                         self.data['const_user'][1]['user_name'])

        user2_status = self.data['const_user'][0]['user_status']
        self.assertEqual(service_search_user(self.conf,
                                             status=user2_status,
                                             exact=True)[0]['user_name'],
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


class TestServiceSearchVideo(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if util_tests_python_version() is False:
            exit()
        cls.data = util_tests_load_data()
        cls.conf = config['test']

    def test_search_video(self):
        self.assertEqual(
            service_search_video(self.conf, title="Xi")[0]['video_title'],
            self.data['const_video'][0]['video_title'],
            msg="Test Search Video: Title")

        self.assertEqual(
            len(service_search_video(self.conf, title="xi",
                                     ignore_case=False)),
            0,
            msg="Test Search Video: Title (not found)")

        self.assertEqual(
            len(service_search_video(self.conf, title="E", format="json")), 0,
            msg="Test Search Video: Title, json")

        self.assertEqual(
            service_search_video(self.conf, video_category="A")[0][
                'video_title'],
            self.data['const_video'][0]['video_title'],
            msg="Test Search Video: Category")

        self.assertEqual(
            service_search_video(self.conf, video_tag="O")[0]['video_title'],
            self.data['const_video'][0]['video_title'],
            msg="Test Search Video: Tag")

        self.assertEqual(
            service_search_video(self.conf, title="a h", slice=True)[0][
                'video_title'],
            self.data['const_video'][0]['video_title'],
            msg="Test Search Video: Tag")

        self.assertEqual(
            service_search_video(self.conf, title="i a", slice=True)[0][
                'video_title'],
            self.data['const_video'][0]['video_title'],
            msg="Test Search Video: Tag")

        self.assertEqual(
            service_search_video(self.conf, title="i%20a", slice=True)[0][
                'video_title'],
            self.data['const_video'][0]['video_title'],
            msg="Test Search Video: Tag")

        # Search successfully with custom pattern (pattern=True)
        self.assertEqual(
            service_search_video(self.conf, title=".*i.*", pattern=True)[0][
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
        self.assertEqual(service_search_video(self.conf, aggregate=True,
                                              search_dict=pipeline)[0][
                             'video_title'],
                         self.data['const_video'][0]['video_title'])

    def test_search_video_by_contains(self):
        video = self.data['const_video'][0]
        self.assertEqual(
            service_search_video_by_contains(video_id=video['_id']['$oid'])[0]
            ['video_title'], video['video_title'])
        self.assertEqual(
            service_search_video_by_contains(video_title=video['video_title'])[
                0]
            ['video_title'], video['video_title'])
        self.assertEqual(service_search_video_by_contains(
            video_channel=video['video_channel'][0:2])[0]
                         ['video_title'], video['video_title'])
        self.assertEqual(service_search_video_by_contains(
            video_category=video['video_category'][0])[0]
                         ['video_title'], video['video_title'])
        self.assertEqual(
            service_search_video_by_contains(video_tag=video['video_tag'][0])[
                0]
            ['video_title'], video['video_title'])
        self.assertEqual(service_search_video_by_contains(
            video_description=video['video_description'][1:4])[0]
                         ['video_title'], video['video_title'])

        # Raise Error: ErrorCode.SERVICE_PARAM_SLICE_NOT_SUPPORT
        with self.assertRaises(ServiceError) as e:
            service_search_video_by_contains(video_lol="lol")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_SEARCH_PARAM)

    def test_search_video_by_pattern(self):
        video_channel = self.data['const_video'][0]['video_channel']

        self.assertEqual(
            service_search_video(self.conf,
                                 channel=video_channel,
                                 exact=True)[0]['video_title'],
            self.data['const_video'][0]['video_title'])

        video = self.data['const_video'][0]
        video_description = video['video_description'][1:5]
        self.assertEqual(
            service_search_video(self.conf,
                                 description=video_description,
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


class TestServiceUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if util_tests_python_version() is False:
            exit()
        cls.data = util_tests_load_data()
        cls.conf = config['test']

    def test_a_service_user_reg(self):
        # Register successfully
        test_name = self.data['temp_user'][0]['user_name']
        test_password = self.data['temp_user'][0]['user_password']
        test_email = self.data['temp_user'][0]['user_email']

        self.assertEqual(service_user_reg(self.conf,
                                          user_name=test_name,
                                          user_password=test_password,
                                          user_email=test_email)['user_name'],
                         self.data['temp_user'][0]['user_name'])

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_user_reg(self.conf)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

    def test_b_service_user_check_password(self):
        # Check successfully with user name
        test_name = self.data['temp_user'][0]['user_name']
        test_password = self.data['temp_user'][0]['user_password']
        test_email = self.data['temp_user'][0]['user_email']

        self.assertTrue(
            service_user_check_password(self.conf,
                                        user_name=test_name,
                                        user_password=test_password))

        # Check successfully with user email
        self.assertTrue(
            service_user_check_password(self.conf,
                                        user_email=test_email,
                                        user_password=test_password))

        # Password Wrong
        self.assertFalse(
            service_user_check_password(self.conf,
                                        user_name=test_name,
                                        user_password="xxx"))

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_user_check_password(self.conf)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        test2_name = self.data['temp_user'][1]['user_name']
        test2_password = self.data['temp_user'][1]['user_password']

        # Raise Error: ErrorCode.SERVICE_USER_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_user_check_password(self.conf,
                                        user_name=test2_name,
                                        user_password=test2_password)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_NOT_FOUND)

    def test_c_service_user_get_info(self):
        # Get successfully
        self.assertEqual(service_user_get_info(self.conf,
                                               self.data['const_user'][0][
                                                   '_id']['$oid'])['user'][0][
                             'user_name'],
                         self.data['const_user'][0]['user_name'])

        self.assertEqual(service_user_get_info(self.conf,
                                               self.data['const_user'][1][
                                                   '_id']['$oid'])['user'][0][
                             'user_name'],
                         self.data['const_user'][1]['user_name'])

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_info(self.conf, 'some random user')
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Raise Error: ErrorCode.SERVICE_USER_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_user_get_info(self.conf, '123456781234567812345678')
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_NOT_FOUND)

    def test_d_service_user_get_like(self):
        # Get successfully
        self.assertEqual(len(service_user_get_like(self.conf,
                                                   self.data['const_user'][0][
                                                       '_id']['$oid'])), 0)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_like(self.conf,
                                  self.data['const_user'][1]['_id']['$oid'])
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_NO_VIDEO_OP)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_like(self.conf, 'some random user')
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Raise Error: ErrorCode.SERVICE_USER_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_user_get_like(self.conf, '123456781234567812345678')
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_NOT_FOUND)

    def test_e_service_user_get_dislike(self):
        # Get successfully
        self.assertEqual(service_user_get_dislike(self.conf,
                                                  self.data['const_user'][0][
                                                      '_id']['$oid'])[0][
                             'user_id'],
                         self.data['const_user'][0]['_id']['$oid'])

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_dislike(self.conf,
                                     self.data['const_user'][1]['_id']['$oid'])
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_NO_VIDEO_OP)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_dislike(self.conf, 'some random user')
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Raise Error: ErrorCode.SERVICE_USER_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_user_get_dislike(self.conf, '123456781234567812345678')
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_NOT_FOUND)

    def test_f_service_user_get_comment(self):
        # Get successfully
        self.assertEqual(service_user_get_comment(self.conf,
                                                  self.data['const_user'][0][
                                                      '_id']['$oid'])[0][
                             'user_id'],
                         self.data['const_user'][0]['_id']['$oid'])

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_comment(self.conf,
                                     self.data['const_user'][1]['_id']['$oid'])
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_NO_VIDEO_OP)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_comment(self.conf, 'some random user')
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Raise Error: ErrorCode.SERVICE_USER_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_user_get_comment(self.conf, '123456781234567812345678')
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_NOT_FOUND)

    def test_g_service_user_get_star(self):
        # Get successfully
        self.assertEqual(len(service_user_get_star(self.conf,
                                                   self.data['const_user'][0][
                                                       '_id']['$oid'])), 1)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_star(self.conf,
                                  self.data['const_user'][1]['_id']['$oid'])
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_NO_VIDEO_OP)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_star(self.conf, 'some random user')
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Raise Error: ErrorCode.SERVICE_USER_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_user_get_star(self.conf, '123456781234567812345678')
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_NOT_FOUND)

    def test_h_service_user_get_process(self):
        # Get successfully
        self.assertEqual(len(service_user_get_process(self.conf,
                                                      self.data['const_user'][
                                                          0]['_id']['$oid'])),
                         0)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_process(self.conf,
                                     self.data['const_user'][1]['_id']['$oid'])
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_NO_VIDEO_OP)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_process(self.conf, 'some random user')
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Raise Error: ErrorCode.SERVICE_USER_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_user_get_process(self.conf, '123456781234567812345678')
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_USER_NOT_FOUND)

    def test_z_service_user_cancel(self):
        user_id = query_user_get_by_name(
            user_name=self.data['temp_user'][0]['user_name'])[0].to_dict()[
            'user_id']
        self.assertEqual(service_user_cancel(self.conf, user_id), 1)


class TestServiceVideo(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if util_tests_python_version() is False:
            exit()
        cls.data = util_tests_load_data()
        cls.conf = config['test']
        cls.temp_video_title = "test video title"
        cls.temp_video_raw_content = \
            "https://s3.amazon.com/test_video_content.avi"

        cls.temp_video_title_updated = "test video title updated"
        cls.temp_video_status = "public"
        cls.temp_video_raw_size = 51.23

        cls.temp_video_title_op = "XiXiHaHa"

    def test_a_service_video_upload(self):
        test_user_id = self.data['const_user'][1]['_id']['$oid']

        self.assertEqual(
            service_video_upload(self.conf,
                                 user_id=test_user_id,
                                 video_title=self.temp_video_title,
                                 video_raw_content=self.temp_video_raw_content)
            [0]['video_title'],
            self.temp_video_title)

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_upload(self.conf,
                                 user_id=self.data['const_user'][1]['_id'][
                                     '$oid'],
                                 video_raw_content=self.temp_video_raw_content)

        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Simply create a video op for testing
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']
        query_video_op_create(
            user_id=self.data['const_user'][1]['_id']['$oid'],
            video_id=temp_video_id,
            init_time=get_time_now_utc())

    def test_b_service_video_info(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']
        self.assertEqual(
            service_video_info(self.conf, video_id=temp_video_id)[0][
                'video_title'],
            self.temp_video_title)

        # Raise Error: ErrorCode.SERVICE_VIDEO_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_video_info(self.conf)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.SERVICE_VIDEO_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_video_info(self.conf, video_id="123456781234567812345678")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_VIDEO_NOT_FOUND)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_video_update(self.conf, video_id="123321")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

    def test_c_service_video_update(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_update(self.conf)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.SERVICE_VIDEO_INVALID_STATUS
        with self.assertRaises(ServiceError) as e:
            service_video_update(self.conf, video_id=temp_video_id,
                                 video_title=self.temp_video_title_updated,
                                 video_status="invalid",
                                 video_raw_size=self.temp_video_raw_size)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_VIDEO_INVALID_STATUS)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_video_update(self.conf, video_id="123321",
                                 video_title=self.temp_video_title_updated,
                                 video_status=self.temp_video_status,
                                 video_raw_size=self.temp_video_raw_size)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful case
        self.assertEqual(
            service_video_update(self.conf, video_id=temp_video_id,
                                 video_title=self.temp_video_title_updated,
                                 video_status=self.temp_video_status,
                                 video_raw_size=self.temp_video_raw_size)[
                0].to_dict()['video_raw_size'],
            self.temp_video_raw_size)

        self.assertEqual(
            service_video_update(self.conf, video_id=temp_video_id,
                                 video_title=self.temp_video_title)[
                0].to_dict()['video_title'],
            self.temp_video_title)

    def test_d_service_video_comments(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title_op)[0].to_dict()[
                'video_id']
        temp_comment = \
            query_video_op_get_by_video_id(temp_video_id)[0].to_dict()[
                'comment']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_comments(self.conf)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_video_comments(self.conf, video_id="123321")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful case
        self.assertEqual(
            len(service_video_comments(self.conf, video_id=temp_video_id)), 1)
        self.assertEqual(
            service_video_comments(self.conf, video_id=temp_video_id)[0][
                'comment'], temp_comment)

    def test_e_service_video_likes(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title_op)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_likes(self.conf)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_video_likes(self.conf, video_id="123321")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful case
        self.assertEqual(
            len(service_video_likes(self.conf, video_id=temp_video_id)), 0)

    def test_f_service_video_dislikes(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title_op)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_dislikes(self.conf)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_video_dislikes(self.conf, video_id="123321")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful case
        self.assertEqual(
            len(service_video_dislikes(self.conf, video_id=temp_video_id)), 1)

    def test_g_service_video_stars(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title_op)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_stars(self.conf)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_video_stars(self.conf, video_id="123321")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful case
        self.assertEqual(
            len(service_video_stars(self.conf, video_id=temp_video_id)), 1)

    def test_h_service_video_delete(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_delete(self.conf)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_video_delete(self.conf, video_id="123321")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful case
        self.assertEqual(
            service_video_delete(self.conf, video_id=temp_video_id), 1)
        self.assertEqual(len(query_video_op_get_by_video_id(temp_video_id)), 0)


class TestServiceVideoOp(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if util_tests_python_version() is False:
            exit()
        cls.data = util_tests_load_data()
        cls.conf = config['test']

        # create a temp video
        cls.temp_video_title = "video op test"
        cls.temp_video_raw_content = \
            "https://s3.amazon.com/test_video_content.avi"

        service_video_upload(conf=cls.conf,
                             user_id=cls.data['const_user'][0]['_id']['$oid'],
                             video_title=cls.temp_video_title,
                             video_raw_content=cls.temp_video_raw_content)

        temp_video_id = \
            query_video_get_by_title(cls.temp_video_title)[0].to_dict()[
                'video_id']

        # create a video op for the video
        query_video_op_create(user_id=cls.data['const_user'][0]['_id']['$oid'],
                              video_id=temp_video_id,
                              init_time=get_time_now_utc())

    def test_a_service_video_op_add_view(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_add_view(self.conf)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_add_view(self.conf, video_id="123123")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        original_view = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_view"]
        current_view = \
            service_video_op_add_view(self.conf, video_id=temp_video_id)[
                "view_count"]
        self.assertEqual(original_view + 1, current_view)

    def test_b_service_video_op_get_view(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_get_view(self.conf)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_get_view(self.conf, video_id="123123")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        original_view = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_view"]
        current_view = \
            service_video_op_get_view(self.conf, video_id=temp_video_id)[
                "view_count"]
        self.assertEqual(original_view, current_view)

    def test_c_service_video_op_add_comment(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']
        temp_comment = "test comment"

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_add_comment(self.conf)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_add_comment(self.conf, video_id="123123",
                                         user_id="aaa", comment="")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        original_comment = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_comment"]

        test_id = self.data['const_user'][0]['_id']['$oid']
        response = service_video_op_add_comment(self.conf,
                                                video_id=temp_video_id,
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

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_get_comment(self.conf)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_cancel_comment(self.conf, video_id="123123",
                                            user_id="aaa")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        original_comment = query_video_op_get_by_user_video(
            self.data['const_user'][0]['_id']['$oid'],
            temp_video_id)[0].to_dict()["comment"]

        test_id = self.data['const_user'][0]['_id']['$oid']
        response = service_video_op_get_comment(self.conf,
                                                video_id=temp_video_id,
                                                user_id=test_id)

        self.assertEqual(original_comment, response["comment"])

    def test_e_service_video_op_update_comment(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']
        temp_comment = "test comment"

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_update_comment(self.conf)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_update_comment(self.conf, video_id="123123",
                                            user_id="aaa", comment="")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        test_id = self.data['const_user'][0]['_id']['$oid']
        response = service_video_op_update_comment(self.conf,
                                                   video_id=temp_video_id,
                                                   user_id=test_id,
                                                   comment=temp_comment)
        self.assertEqual(temp_comment, response["comment"])

    def test_f_service_video_op_cancel_comment(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_cancel_comment(self.conf)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_cancel_comment(self.conf, video_id="123123",
                                            user_id="aaa")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        original_comment = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_comment"]

        test_id = self.data['const_user'][0]['_id']['$oid']
        response = service_video_op_cancel_comment(self.conf,
                                                   video_id=temp_video_id,
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
            service_video_op_add_process(self.conf)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_add_process(self.conf, video_id="123123",
                                         user_id="aaa", process=30)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        with self.assertRaises(ServiceError) as e:
            test_id = self.data['const_user'][0]['_id']['$oid']
            service_video_op_add_process(self.conf, video_id=temp_video_id,
                                         user_id=test_id, process=-100)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_SEARCH_PARAM)

        # Successful test
        test_id = self.data['const_user'][0]['_id']['$oid']
        response = service_video_op_add_process(self.conf,
                                                video_id=temp_video_id,
                                                user_id=test_id,
                                                process=temp_process)
        self.assertEqual(temp_process, response["process"])

    def test_h_service_video_op_get_process(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_get_process(self.conf)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_get_process(self.conf, video_id="123123",
                                         user_id="aaa")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        original_process = query_video_op_get_by_user_video(
            self.data['const_user'][0]['_id']['$oid'],
            temp_video_id)[0].to_dict()["process"]
        test_id = self.data['const_user'][0]['_id']['$oid']
        response = service_video_op_get_process(self.conf,
                                                video_id=temp_video_id,
                                                user_id=test_id)
        self.assertEqual(original_process, response["process"])

    def test_i_service_video_op_update_process(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']
        temp_process = 60

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_update_process(self.conf)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_update_process(self.conf, video_id="123123",
                                            user_id="aaa", process=30)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        with self.assertRaises(ServiceError) as e:
            test_id = self.data['const_user'][0]['_id']['$oid']
            service_video_op_update_process(self.conf, video_id=temp_video_id,
                                            user_id=test_id, process=-100)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_SEARCH_PARAM)

        # Successful test
        test_id = self.data['const_user'][0]['_id']['$oid']
        response = service_video_op_update_process(self.conf,
                                                   video_id=temp_video_id,
                                                   user_id=test_id,
                                                   process=temp_process)
        self.assertEqual(temp_process, response["process"])

    def test_j_service_video_op_cancel_process(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_cancel_process(self.conf)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_cancel_process(self.conf, video_id="123123",
                                            user_id="aaa")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        test_id = self.data['const_user'][0]['_id']['$oid']
        response = service_video_op_cancel_process(self.conf,
                                                   video_id=temp_video_id,
                                                   user_id=test_id)
        self.assertEqual(response["process"], 0)

    def test_k_service_video_op_add_like(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_add_like(self.conf)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_add_like(self.conf, video_id="123123",
                                      user_id="aaa")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        original_like = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_like"]
        test_id = self.data['const_user'][0]['_id']['$oid']
        response = service_video_op_add_like(self.conf, video_id=temp_video_id,
                                             user_id=test_id)
        current_like = query_video_get_by_video_id(temp_video_id)[0].to_dict()[
            "video_like"]
        self.assertEqual(response["like"], True)
        self.assertEqual(response["dislike"], False)
        self.assertEqual(original_like + 1, current_like)

        # Raise Error: ErrorCode.MONGODB_VIDEO_LIKE_UPDATE_FAILURE
        with self.assertRaises(MongoError) as e:
            test_id = self.data['const_user'][0]['_id']['$oid']
            service_video_op_add_like(self.conf, video_id=temp_video_id,
                                      user_id=test_id)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_VIDEO_LIKE_UPDATE_FAILURE)

        # If already dislike, can switch to like
        original_like = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_like"]
        original_dislike = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_dislike"]
        test_id = self.data['const_user'][0]['_id']['$oid']
        service_video_op_add_dislike(self.conf,
                                     video_id=temp_video_id,
                                     user_id=test_id)
        response = service_video_op_add_like(self.conf,
                                             video_id=temp_video_id,
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
            service_video_op_cancel_like(self.conf)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_cancel_like(self.conf, video_id="123123",
                                         user_id="aaa")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        original_like = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_like"]

        test_id = self.data['const_user'][0]['_id']['$oid']
        response = service_video_op_cancel_like(self.conf,
                                                video_id=temp_video_id,
                                                user_id=test_id)
        current_like = query_video_get_by_video_id(temp_video_id)[0].to_dict()[
            "video_like"]
        self.assertEqual(response["like"], False)
        self.assertEqual(response["dislike"], False)
        self.assertEqual(original_like - 1, current_like)

        # Raise Error: ErrorCode.MONGODB_VIDEO_LIKE_UPDATE_FAILURE
        with self.assertRaises(MongoError) as e:
            test_id = self.data['const_user'][0]['_id']['$oid']
            service_video_op_cancel_like(self.conf, video_id=temp_video_id,
                                         user_id=test_id)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_VIDEO_LIKE_UPDATE_FAILURE)

    def test_m_service_video_op_add_dislike(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_add_dislike(self.conf)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_add_dislike(self.conf, video_id="123123",
                                         user_id="aaa")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        original_dislike = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_dislike"]
        test_id = self.data['const_user'][0]['_id']['$oid']
        response = service_video_op_add_dislike(self.conf,
                                                video_id=temp_video_id,
                                                user_id=test_id)
        current_dislike = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_dislike"]
        self.assertEqual(response["like"], False)
        self.assertEqual(response["dislike"], True)
        self.assertEqual(original_dislike + 1, current_dislike)

        # Raise Error: ErrorCode.MONGODB_VIDEO_DISLIKE_UPDATE_FAILURE
        with self.assertRaises(MongoError) as e:
            test_id = self.data['const_user'][0]['_id']['$oid']
            service_video_op_add_dislike(self.conf, video_id=temp_video_id,
                                         user_id=test_id)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_VIDEO_DISLIKE_UPDATE_FAILURE)

        # If already like, can switch to dislike
        original_like = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_like"]
        original_dislike = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_dislike"]
        test_id = self.data['const_user'][0]['_id']['$oid']
        service_video_op_add_like(self.conf,
                                  video_id=temp_video_id,
                                  user_id=test_id)
        response = service_video_op_add_dislike(self.conf,
                                                video_id=temp_video_id,
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
            service_video_op_cancel_dislike(self.conf)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_cancel_dislike(self.conf, video_id="123123",
                                            user_id="aaa")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        original_dislike = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_dislike"]
        test_id = self.data['const_user'][0]['_id']['$oid']
        response = service_video_op_cancel_dislike(self.conf,
                                                   video_id=temp_video_id,
                                                   user_id=test_id)
        current_dislike = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_dislike"]
        self.assertEqual(response["like"], False)
        self.assertEqual(response["dislike"], False)
        self.assertEqual(original_dislike - 1, current_dislike)

        # Raise Error: ErrorCode.MONGODB_VIDEO_DISLIKE_UPDATE_FAILURE
        with self.assertRaises(MongoError) as e:
            test_id = self.data['const_user'][0]['_id']['$oid']
            service_video_op_cancel_dislike(self.conf, video_id=temp_video_id,
                                            user_id=test_id)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_VIDEO_DISLIKE_UPDATE_FAILURE)

    def test_o_service_video_op_add_star(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_add_star(self.conf)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_add_star(self.conf, video_id="123123",
                                      user_id="aaa")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        original_star = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_star"]
        test_id = self.data['const_user'][0]['_id']['$oid']
        response = service_video_op_add_star(self.conf, video_id=temp_video_id,
                                             user_id=test_id)
        current_star = query_video_get_by_video_id(temp_video_id)[0].to_dict()[
            "video_star"]
        self.assertEqual(response["star"], True)
        self.assertEqual(original_star + 1, current_star)

        # Raise Error: ErrorCode.MONGODB_VIDEO_DISLIKE_UPDATE_FAILURE
        with self.assertRaises(MongoError) as e:
            test_id = self.data['const_user'][0]['_id']['$oid']
            service_video_op_add_star(self.conf, video_id=temp_video_id,
                                      user_id=test_id)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_VIDEO_STAR_UPDATE_FAILURE)

    def test_p_service_video_op_cancel_star(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_cancel_star(self.conf)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        with self.assertRaises(ServiceError) as e:
            service_video_op_cancel_star(self.conf, video_id="123123",
                                         user_id="aaa")
        self.assertEqual(e.exception.error_code,
                         ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Successful test
        original_star = \
            query_video_get_by_video_id(temp_video_id)[0].to_dict()[
                "video_star"]
        test_id = self.data['const_user'][0]['_id']['$oid']
        response = service_video_op_cancel_star(self.conf,
                                                video_id=temp_video_id,
                                                user_id=test_id)
        current_star = query_video_get_by_video_id(temp_video_id)[0].to_dict()[
            "video_star"]
        self.assertEqual(response["star"], False)
        self.assertEqual(original_star - 1, current_star)

        # Raise Error: ErrorCode.MONGODB_VIDEO_DISLIKE_UPDATE_FAILURE
        with self.assertRaises(MongoError) as e:
            test_id = self.data['const_user'][0]['_id']['$oid']
            service_video_op_cancel_star(self.conf, video_id=temp_video_id,
                                         user_id=test_id)
        self.assertEqual(e.exception.error_code,
                         ErrorCode.MONGODB_VIDEO_STAR_UPDATE_FAILURE)

    def test_z_delete_testing_data(self):
        temp_video_id = \
            query_video_get_by_title(self.temp_video_title)[0].to_dict()[
                'video_id']
        service_video_delete(self.conf, video_id=temp_video_id)


"""
if __name__ == "__main__":
    unittest.main()
"""

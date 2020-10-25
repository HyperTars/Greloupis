import unittest
from source.models.model_errors import *
from source.service.service_search import *
from source.service.service_user import *
from source.service.service_video import *
from source.service.service_video_op import *
from source.settings import *
from source.tests.unit.test_load_data import util_load_test_data


class TestServiceSearchUser(unittest.TestCase):
    data = util_load_test_data()
    const_user_0 = data['const_user'][0]
    const_user_1 = data['const_user'][1]
    const_user_2 = data['const_user'][2]

    @classmethod
    def setUpClass(cls) -> None:
        cls.conf = config['test']

    def test_search_user(self):
        # Search successfully with ignore_case
        self.assertEqual(service_search_user(self.conf, name="t", ignore_case=False)[0]['user_name'],
                         self.const_user_0['user_name'])

        # Search successfully with exact (result = 0)
        self.assertEqual(len(service_search_user(self.conf, name="milvu", exact=True)), 0)

        # Search successfully with ignore_case and exact
        self.assertEqual(service_search_user(self.conf, name="milvUS", ignore_case=True, exact=True)[0]['user_name'],
                         self.const_user_1['user_name'])

        # Search successfully with custom pattern (pattern=True)
        self.assertEqual(service_search_user(self.conf, name=".*t.*", pattern=True)[0]['user_name'],
                         self.const_user_0['user_name'])

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
        self.assertEqual(service_search_user(self.conf, aggregate=True, search_dict=pipeline)[0]['user_name'],
                         self.const_user_0['user_name'])

        # Raise Error: ErrorCode.SERVICE_PARAM_SLICE_NOT_SUPPORT
        with self.assertRaises(ServiceError) as e:
            service_search_user(self.conf, slice=True)
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_PARAM_SLICE_NOT_SUPPORT)

    def test_search_user_by_contains(self):
        user = self.const_user_0
        self.assertEqual(service_search_user_by_contains(user_id=user['_id']['$oid'])[0]['user_name'],
                         user['user_name'])
        self.assertEqual(service_search_user_by_contains(user_email=user['user_email'])[0]['user_name'],
                         user['user_name'])
        self.assertEqual(service_search_user_by_contains(user_first_name=user['user_detail']['user_first_name'])
                         [0]['user_name'], user['user_name'])
        self.assertEqual(service_search_user_by_contains(user_last_name=user['user_detail']['user_last_name'])
                         [0]['user_name'], user['user_name'])
        self.assertEqual(service_search_user_by_contains(user_phone=user['user_detail']['user_phone'])
                         [0]['user_name'], user['user_name'])
        self.assertEqual(service_search_user_by_contains(user_street1=user['user_detail']['user_street1'])
                         [0]['user_name'], user['user_name'])
        self.assertEqual(service_search_user_by_contains(user_street2=user['user_detail']['user_street2'])
                         [0]['user_name'], user['user_name'])
        self.assertEqual(service_search_user_by_contains(user_city=user['user_detail']['user_city'])
                         [0]['user_name'], user['user_name'])
        self.assertEqual(service_search_user_by_contains(user_state=user['user_detail']['user_state'])
                         [0]['user_name'], user['user_name'])
        self.assertEqual(service_search_user_by_contains(user_country=user['user_detail']['user_country'])
                         [0]['user_name'], user['user_name'])
        self.assertEqual(service_search_user_by_contains(user_zip=user['user_detail']['user_zip'])
                         [0]['user_name'], user['user_name'])
        self.assertEqual(service_search_user_by_contains(user_status=user['user_status'])
                         [0]['user_name'], user['user_name'])

        # Raise Error: ErrorCode.SERVICE_PARAM_SLICE_NOT_SUPPORT
        with self.assertRaises(ServiceError) as e:
            service_search_user_by_contains(user_lol="lol")
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_INVALID_SEARCH_PARAM)

    def test_search_user_by_pattern(self):
        self.assertEqual(service_search_user(self.conf, email=self.const_user_1['user_email'][2:5],
                                             ignore_case=False)[0]['user_name'], self.const_user_1['user_name'])

        self.assertEqual(service_search_user(self.conf,
                                             first_name=self.const_user_1['user_detail']['user_first_name'][1:3],
                                             ignore_case=False)[0]['user_name'], self.const_user_1['user_name'])

        self.assertEqual(service_search_user(self.conf,
                                             last_name=self.const_user_1['user_detail']['user_last_name'][1:3],
                                             ignore_case=False)[0]['user_name'], self.const_user_1['user_name'])

        self.assertEqual(service_search_user(self.conf,
                                             phone=self.const_user_1['user_detail']['user_phone'][2:5],
                                             ignore_case=False)[0]['user_name'], self.const_user_1['user_name'])

        self.assertEqual(service_search_user(self.conf,
                                             street1=self.const_user_1['user_detail']['user_street1'],
                                             exact=True)[0]['user_name'], self.const_user_1['user_name'])

        self.assertEqual(service_search_user(self.conf,
                                             street2=self.const_user_0['user_detail']['user_street2'],
                                             exact=True)[0]['user_name'], self.const_user_0['user_name'])

        self.assertEqual(service_search_user(self.conf,
                                             city=self.const_user_1['user_detail']['user_city'],
                                             exact=True)[0]['user_name'], self.const_user_1['user_name'])

        self.assertEqual(service_search_user(self.conf,
                                             state=self.const_user_1['user_detail']['user_state'],
                                             exact=True)[0]['user_name'], self.const_user_1['user_name'])

        self.assertEqual(service_search_user(self.conf,
                                             country=self.const_user_1['user_detail']['user_country'],
                                             exact=True)[0]['user_name'], self.const_user_1['user_name'])

        self.assertEqual(service_search_user(self.conf,
                                             zip=self.const_user_1['user_detail']['user_zip'],
                                             exact=True)[0]['user_name'], self.const_user_1['user_name'])

        self.assertEqual(service_search_user(self.conf,
                                             status=self.const_user_0['user_status'],
                                             exact=True)[0]['user_name'], self.const_user_0['user_name'])

        # Raise Error: ErrorCode.SERVICE_INVALID_SEARCH_PARAM
        with self.assertRaises(ServiceError) as e:
            service_search_user_by_pattern(pattern_lol="lol")
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_PATTERN_SEARCH_NOT_SUPPORT)

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
        self.assertEqual(service_search_user_by_aggregation(pipeline1)[0]['user_name'],
                         self.const_user_0['user_name'])
        self.assertEqual(service_search_user_by_aggregation(pipeline2)[0]['user_name'],
                         self.const_user_0['user_name'])


class TestServiceSearchVideo(unittest.TestCase):
    data = util_load_test_data()
    const_video_0 = data['const_video'][0]

    @classmethod
    def setUpClass(cls) -> None:
        cls.conf = config['test']

    def test_search_video(self):
        self.assertEqual(service_search_video(self.conf, title="Xi")[0]['video_title'],
                         self.const_video_0['video_title'], msg="Test Search Video: Title")

        self.assertEqual(len(service_search_video(self.conf, title="xi", ignore_case=False)), 0,
                         msg="Test Search Video: Title (not found)")

        self.assertEqual(len(service_search_video(self.conf, title="E", format="json")), 0,
                         msg="Test Search Video: Title, json")

        self.assertEqual(service_search_video(self.conf, video_category="A")[0]['video_title'],
                         self.const_video_0['video_title'], msg="Test Search Video: Category")

        self.assertEqual(service_search_video(self.conf, video_tag="O")[0]['video_title'],
                         self.const_video_0['video_title'], msg="Test Search Video: Tag")

        self.assertEqual(service_search_video(self.conf, title="a h", slice=True)[0]['video_title'],
                         self.const_video_0['video_title'], msg="Test Search Video: Tag")

        self.assertEqual(service_search_video(self.conf, title="i a", slice=True)[0]['video_title'],
                         self.const_video_0['video_title'], msg="Test Search Video: Tag")

        self.assertEqual(service_search_video(self.conf, title="i%20a", slice=True)[0]['video_title'],
                         self.const_video_0['video_title'], msg="Test Search Video: Tag")

        # Search successfully with custom pattern (pattern=True)
        self.assertEqual(service_search_video(self.conf, title=".*i.*", pattern=True)[0]['video_title'],
                         self.const_video_0['video_title'])

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
        self.assertEqual(service_search_video(self.conf, aggregate=True, search_dict=pipeline)[0]['video_title'],
                         self.const_video_0['video_title'])

    def test_search_video_by_contains(self):
        video = self.const_video_0
        self.assertEqual(service_search_video_by_contains(video_id=video['_id']['$oid'])[0]
                         ['video_title'], video['video_title'])
        self.assertEqual(service_search_video_by_contains(video_title=video['video_title'])[0]
                         ['video_title'], video['video_title'])
        self.assertEqual(service_search_video_by_contains(video_channel=video['video_channel'][0:2])[0]
                         ['video_title'], video['video_title'])
        self.assertEqual(service_search_video_by_contains(video_category=video['video_category'][0])[0]
                         ['video_title'], video['video_title'])
        self.assertEqual(service_search_video_by_contains(video_tag=video['video_tag'][0])[0]
                         ['video_title'], video['video_title'])
        self.assertEqual(service_search_video_by_contains(video_description=video['video_description'][1:4])[0]
                         ['video_title'], video['video_title'])

        # Raise Error: ErrorCode.SERVICE_PARAM_SLICE_NOT_SUPPORT
        with self.assertRaises(ServiceError) as e:
            service_search_video_by_contains(video_lol="lol")
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_INVALID_SEARCH_PARAM)

    def test_search_video_by_pattern(self):
        self.assertEqual(service_search_video(self.conf, channel=self.const_video_0['video_channel'],
                                              exact=True)[0]['video_title'], self.const_video_0['video_title'])

        self.assertEqual(service_search_video(self.conf, description=self.const_video_0['video_description'][1:5],
                                              ignore_case=False)[0]['video_description'],
                         self.const_video_0['video_description'])

        # Raise Error: ErrorCode.SERVICE_INVALID_SEARCH_PARAM
        with self.assertRaises(ServiceError) as e:
            service_search_video_by_pattern(pattern_lol="lol")
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_PATTERN_SEARCH_NOT_SUPPORT)

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
        self.assertEqual(service_search_video_by_aggregation(pipeline)[0]['video_title'],
                         self.const_video_0['video_title'])


class TestServiceUser(unittest.TestCase):
    data = util_load_test_data()

    const_user_0 = data['const_user'][0]
    const_user_1 = data['const_user'][1]
    const_user_2 = data['const_user'][2]

    temp_user_0 = data['temp_user'][0]
    temp_user_1 = data['temp_user'][1]

    @classmethod
    def setUpClass(cls) -> None:
        cls.conf = config['test']

    def test_a_service_user_reg(self):
        # Register successfully
        self.assertEqual(service_user_reg(self.conf, user_name=self.temp_user_0['user_name'],
                                          user_password=self.temp_user_0['user_password'],
                                          user_email=self.temp_user_0['user_email'])['user_name'],
                         self.temp_user_0['user_name'])

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_user_reg(self.conf)
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_MISSING_PARAM)

    def test_b_service_user_check_password(self):
        # Check successfully with user name
        self.assertTrue(service_user_check_password(self.conf, user_name=self.temp_user_0['user_name'],
                                                    user_password=self.temp_user_0['user_password']))

        # Check successfully with user email
        self.assertTrue(service_user_check_password(self.conf, user_email=self.temp_user_0['user_email'],
                                                    user_password=self.temp_user_0['user_password']))

        # Password Wrong
        self.assertFalse(service_user_check_password(self.conf, user_name=self.temp_user_0['user_name'],
                                                     user_password="xxx"))

        # Raise Error: ErrorCode.SERVICE_MISSING_PARAM
        with self.assertRaises(ServiceError) as e:
            service_user_check_password(self.conf)
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.SERVICE_USER_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_user_check_password(self.conf, user_name=self.temp_user_1['user_name'],
                                        user_password=self.temp_user_1['user_password'])
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_USER_NOT_FOUND)

    def test_c_service_user_get_info(self):
        # Get successfully
        self.assertEqual(service_user_get_info(self.conf, self.const_user_0['_id']['$oid'])['user'][0]['user_name'],
                         self.const_user_0['user_name'])

        self.assertEqual(service_user_get_info(self.conf, self.const_user_1['_id']['$oid'])['user'][0]['user_name'],
                         self.const_user_1['user_name'])

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_info(self.conf, 'some random user')
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Raise Error: ErrorCode.SERVICE_USER_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_user_get_info(self.conf, '123456781234567812345678')
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_USER_NOT_FOUND)

    def test_d_service_user_get_like(self):
        # Get successfully
        self.assertEqual(len(service_user_get_like(self.conf, self.const_user_0['_id']['$oid'])), 0)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_like(self.conf, self.const_user_1['_id']['$oid'])
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_USER_NO_VIDEO_OP)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_like(self.conf, 'some random user')
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Raise Error: ErrorCode.SERVICE_USER_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_user_get_like(self.conf, '123456781234567812345678')
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_USER_NOT_FOUND)

    def test_e_service_user_get_dislike(self):
        # Get successfully
        self.assertEqual(service_user_get_dislike(self.conf, self.const_user_0['_id']['$oid'])[0]['user_id'],
                         self.const_user_0['_id']['$oid'])

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_dislike(self.conf, self.const_user_1['_id']['$oid'])
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_USER_NO_VIDEO_OP)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_dislike(self.conf, 'some random user')
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Raise Error: ErrorCode.SERVICE_USER_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_user_get_dislike(self.conf, '123456781234567812345678')
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_USER_NOT_FOUND)

    def test_f_service_user_get_comment(self):
        # Get successfully
        self.assertEqual(service_user_get_comment(self.conf, self.const_user_0['_id']['$oid'])[0]['user_id'],
                         self.const_user_0['_id']['$oid'])

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_comment(self.conf, self.const_user_1['_id']['$oid'])
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_USER_NO_VIDEO_OP)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_comment(self.conf, 'some random user')
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Raise Error: ErrorCode.SERVICE_USER_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_user_get_comment(self.conf, '123456781234567812345678')
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_USER_NOT_FOUND)

    def test_g_service_user_get_star(self):
        # Get successfully
        self.assertEqual(len(service_user_get_star(self.conf, self.const_user_0['_id']['$oid'])), 0)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_star(self.conf, self.const_user_1['_id']['$oid'])
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_USER_NO_VIDEO_OP)

        # Raise Error: ErrorCode.SERVICE_INVALID_ID_OBJ
        with self.assertRaises(ServiceError) as e:
            service_user_get_star(self.conf, 'some random user')
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_INVALID_ID_OBJ)

        # Raise Error: ErrorCode.SERVICE_USER_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_user_get_star(self.conf, '123456781234567812345678')
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_USER_NOT_FOUND)

    def test_z_service_user_cancel(self):
        user_id = query_user_get_by_name(user_name=self.temp_user_0['user_name'])[0].to_dict()['user_id']
        self.assertEqual(service_user_cancel(self.conf, user_id), 1)


class TestServiceVideo(unittest.TestCase):
    data = util_load_test_data()

    const_user_0 = data['const_user'][0]
    const_user_1 = data['const_user'][1]
    const_user_2 = data['const_user'][2]

    temp_user_0 = data['temp_user'][0]
    temp_user_1 = data['temp_user'][1]

    const_video_0 = data['const_video'][0]

    @classmethod
    def setUpClass(cls) -> None:
        cls.conf = config['test']
        cls.temp_video_title = "test video title"
        cls.temp_video_raw_content = "https://s3.amazon.com/test_video_content.avi"

    def test_a_service_video_upload(self):
        self.assertEqual(service_video_upload(self.conf, user_id=self.const_user_1['_id']['$oid'],
                                              video_title=self.temp_video_title,
                                              video_raw_content=self.temp_video_raw_content)['video_title'],
                         self.temp_video_title)

    def test_b_service_video_info(self):
        temp_video_id = query_video_get_by_title(self.temp_video_title)[0].to_dict()['video_id']
        self.assertEqual(service_video_info(self.conf, video_id=temp_video_id)['video_title'],
                         self.temp_video_title)

        # Raise Error: ErrorCode.SERVICE_VIDEO_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_video_info(self.conf)
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.SERVICE_VIDEO_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_video_info(self.conf, video_id="123456781234567812345678")
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_VIDEO_NOT_FOUND)

    def test_c_service_video_update(self):
        pass

    def test_d_service_video_comments(self):
        pass

    def test_e_service_video_likes(self):
        pass

    def test_f_service_video_dislikes(self):
        pass

    def test_g_service_video_stars(self):
        pass

    def test_h_service_video_delete(self):
        temp_video_id = query_video_get_by_title(self.temp_video_title)[0].to_dict()['video_id']
        self.assertEqual(service_video_delete(self.conf, video_id=temp_video_id), 1)

        # Raise Error: ErrorCode.SERVICE_VIDEO_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_video_info(self.conf)
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_MISSING_PARAM)

        # Raise Error: ErrorCode.SERVICE_VIDEO_NOT_FOUND
        with self.assertRaises(ServiceError) as e:
            service_video_info(self.conf, video_id="123456781234567812345678")
        self.assertEqual(e.exception.error_code, ErrorCode.SERVICE_VIDEO_NOT_FOUND)


if __name__ == "__main__":
    unittest.main()

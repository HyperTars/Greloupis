import unittest
from source.settings import *
from source.db.mongo import get_db
from source.tests.unit.test_load_data import *
from source.db.query_user import *
from source.db.query_video import *
from source.db.query_video_op import *
from source.models.model_errors import *
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
    data = util_load_test_data()

    const_video_0 = data['const_video'][0]

    temp_video_0 = data['temp_video'][0]

    def setUp(self):
        pass

    def test_a_query_video_create(self):
        self.assertEqual(query_video_create(user_id=self.temp_video_0['user_id'],
                                            video_title=self.temp_video_0['video_title'],
                                            video_raw_content=self.temp_video_0['video_raw_content']).video_title,
                         self.temp_video_0['video_title'])

    def test_b_query_video_get_by_video_id(self):
        self.assertEqual(query_video_get_by_video_id(str(self.const_video_0['_id']['$oid']))[0].video_title,
                         self.const_video_0['video_title'])

    def test_c_query_video_get_by_user_id(self):
        self.assertEqual(len(query_video_get_by_user_id(self.temp_video_0['user_id'])), 2)

    def test_d_query_video_get_by_title(self):
        self.assertEqual(query_video_get_by_title(self.temp_video_0['video_title'])[0].user_id,
                         self.temp_video_0['user_id'])

    def test_e_query_video_cnt_incr_by_one(self):
        temp_model = query_video_get_by_title(self.temp_video_0['video_title'])[0].to_dict()
        temp_video_id = temp_model['video_id']
        temp_video_view = temp_model['video_view']
        temp_video_comment = temp_model['video_comment']
        temp_video_like = temp_model['video_like']
        temp_video_dislike = temp_model['video_dislike']
        temp_video_star = temp_model['video_star']
        temp_video_share = temp_model['video_share']

        query_video_cnt_incr_by_one(temp_video_id, "video_view")
        self.assertEqual(query_video_get_by_video_id(temp_video_id)[0].video_view, temp_video_view + 1)
        query_video_cnt_incr_by_one(temp_video_id, "video_comment")
        self.assertEqual(query_video_get_by_video_id(temp_video_id)[0].video_view, temp_video_comment + 1)
        query_video_cnt_incr_by_one(temp_video_id, "video_like")
        self.assertEqual(query_video_get_by_video_id(temp_video_id)[0].video_view, temp_video_like + 1)
        query_video_cnt_incr_by_one(temp_video_id, "video_dislike")
        self.assertEqual(query_video_get_by_video_id(temp_video_id)[0].video_view, temp_video_dislike + 1)
        query_video_cnt_incr_by_one(temp_video_id, "video_star")
        self.assertEqual(query_video_get_by_video_id(temp_video_id)[0].video_view, temp_video_star + 1)
        query_video_cnt_incr_by_one(temp_video_id, "video_share")
        self.assertEqual(query_video_get_by_video_id(temp_video_id)[0].video_view, temp_video_share + 1)

    def test_f_query_video_cnt_decr_by_one(self):
        temp_model = query_video_get_by_title(self.temp_video_0['video_title'])[0].to_dict()
        temp_video_id = temp_model['video_id']
        temp_video_view = temp_model['video_view']
        temp_video_comment = temp_model['video_comment']
        temp_video_like = temp_model['video_like']
        temp_video_dislike = temp_model['video_dislike']
        temp_video_star = temp_model['video_star']
        temp_video_share = temp_model['video_share']

        query_video_cnt_decr_by_one(temp_video_id, "video_view")
        self.assertEqual(query_video_get_by_video_id(temp_video_id)[0].video_view, temp_video_view - 1)
        query_video_cnt_decr_by_one(temp_video_id, "video_comment")
        self.assertEqual(query_video_get_by_video_id(temp_video_id)[0].video_view, temp_video_comment - 1)
        query_video_cnt_decr_by_one(temp_video_id, "video_like")
        self.assertEqual(query_video_get_by_video_id(temp_video_id)[0].video_view, temp_video_like - 1)
        query_video_cnt_decr_by_one(temp_video_id, "video_dislike")
        self.assertEqual(query_video_get_by_video_id(temp_video_id)[0].video_view, temp_video_dislike - 1)
        query_video_cnt_decr_by_one(temp_video_id, "video_star")
        self.assertEqual(query_video_get_by_video_id(temp_video_id)[0].video_view, temp_video_star - 1)
        query_video_cnt_decr_by_one(temp_video_id, "video_share")
        self.assertEqual(query_video_get_by_video_id(temp_video_id)[0].video_view, temp_video_share - 1)

    def test_g_query_video_update(self):
        temp_video_id = query_video_get_by_title(self.temp_video_0['video_title'])[0].to_dict()['video_id']

        old_title = self.temp_video_0['video_title']
        new_title = "new_title"
        new_raw_content = "some new content uri"
        new_raw_status = "finished"
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

        query_video_update(temp_video_id, video_title=new_title, video_raw_content=new_raw_content,
                           video_raw_status=new_raw_status, video_raw_size=new_raw_size, video_duration=new_duration,
                           video_channel=new_channel, video_tag=new_tag, video_category=new_category,
                           video_description=new_description, video_language=new_language, video_status=new_status,
                           video_thumbnail=new_thumbnail, video_uri_low=new_uri_low, video_uri_mid=new_uri_mid,
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
        self.assertEqual(query_video_get_by_video_id(temp_video_id)[0].video_title, old_title)

    def test_h_query_video_delete(self):
        temp_video_id_0 = query_video_get_by_title(self.temp_video_0['video_title'])[0].to_dict()['video_id']
        self.assertEqual(query_video_delete(temp_video_id_0), 1)

    def test_i_query_video_search_by_contains(self):
        video = query_video_search_by_contains(video_id=self.const_video_0['_id']['$oid'])[0]  # exact video_id
        self.assertEqual(video.video_title, self.const_video_0['video_title'])

        video = query_video_search_by_contains(user_id=self.const_video_0['user_id'])[0]  # exact user_id
        self.assertEqual(video.video_title, self.const_video_0['video_title'])

        video = query_video_search_by_contains(video_title=self.const_video_0['video_title'][1:2])[0]
        self.assertEqual(video.video_title, self.const_video_0['video_title'])

        video = query_video_search_by_contains(video_channel=self.const_video_0['video_channel'])[0]
        self.assertEqual(video.video_title, self.const_video_0['video_title'])

        video = query_video_search_by_contains(video_category=self.const_video_0['video_category'][0])[0]
        self.assertEqual(video.video_title, self.const_video_0['video_title'])

        video = query_video_search_by_contains(video_tag=self.const_video_0['video_tag'][0])[0]
        self.assertEqual(video.video_title, self.const_video_0['video_title'])

        video = query_video_search_by_contains(video_description=self.const_video_0['video_description'][2:3])[0]
        self.assertEqual(video.video_title, self.const_video_0['video_title'])

    def test_j_query_video_search_by_pattern(self):
        search_video_title = self.const_video_0['video_title']
        search_video_channel = self.const_video_0['video_channel']
        search_video_description = self.const_video_0['video_description']

        # SEARCH BY TITLE PATTERN #
        # Search exact fail
        pattern_exact_fail = util_pattern_compile(search_video_title[1:2], exact=True, ignore_case=True)
        self.assertEqual(len(query_video_search_by_pattern(pattern_title=pattern_exact_fail)), 0)

        # Search exact successfully
        pattern_exact_success = util_pattern_compile(search_video_title, exact=True, ignore_case=True)
        self.assertEqual(query_video_search_by_pattern(pattern_title=pattern_exact_success)[0].video_title,
                         search_video_title)

        # Search case fail
        pattern_case_fail = util_pattern_compile(search_video_title[1:2].upper(), exact=False, ignore_case=False)
        self.assertEqual(len(query_video_search_by_pattern(pattern_title=pattern_case_fail)), 0)

        # Search case successfully
        pattern_case_success = util_pattern_compile(search_video_title[1:2].upper(), exact=False, ignore_case=True)
        self.assertEqual(query_video_search_by_pattern(pattern_title=pattern_case_success)[0].video_title,
                         search_video_title)

        # SEARCH BY CHANNEL PATTERN #
        # Search exact fail
        pattern_exact_fail = util_pattern_compile(search_video_channel[1:2], exact=True, ignore_case=True)
        self.assertEqual(len(query_video_search_by_pattern(pattern_channel=pattern_exact_fail)), 0)

        # Search exact successfully
        pattern_exact_success = util_pattern_compile(search_video_channel, exact=True, ignore_case=True)
        self.assertEqual(query_video_search_by_pattern(pattern_channel=pattern_exact_success)[0].video_channel,
                         search_video_channel)

        # Search case fail
        pattern_case_fail = util_pattern_compile(search_video_channel[1:2].upper(), exact=False, ignore_case=False)
        self.assertEqual(len(query_video_search_by_pattern(pattern_channel=pattern_case_fail)), 0)

        # Search case successfully
        pattern_case_success = util_pattern_compile(search_video_channel[1:2].upper(), exact=False, ignore_case=True)
        self.assertEqual(query_video_search_by_pattern(pattern_channel=pattern_case_success)[0].video_channel,
                         search_video_channel)

        # SEARCH BY DESCRIPTION PATTERN #
        # Search exact fail
        pattern_exact_fail = util_pattern_compile(search_video_description[1:2], exact=True, ignore_case=True)
        self.assertEqual(len(query_video_search_by_pattern(pattern_description=pattern_exact_fail)), 0)

        # Search exact successfully
        pattern_exact_success = util_pattern_compile(search_video_description, exact=True, ignore_case=True)
        self.assertEqual(query_video_search_by_pattern(pattern_description=pattern_exact_success)[0].video_description,
                         search_video_description)

        # Search case fail
        pattern_case_fail = util_pattern_compile(search_video_description[1:2].upper(), exact=False, ignore_case=False)
        self.assertEqual(len(query_video_search_by_pattern(pattern_description=pattern_case_fail)), 0)

        # Search case successfully
        pattern_case_success = util_pattern_compile(search_video_description[1:2].upper(),
                                                    exact=False, ignore_case=True)
        self.assertEqual(query_video_search_by_pattern(pattern_description=pattern_case_success)[0].video_description,
                         search_video_description)

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
        self.assertEqual(videos[0]['video_title'], self.const_video_0['video_title'])


"""
class TestQueryVideoOp(unittest.TestCase):
    data = util_load_test_data()

    const_video_op_0 = data['const_video_op'][0]

    temp_video_op_0 = data['temp_video_op'][0]

    def setUp(self):
        pass

    def test_a_query_video_op_create(self):
        query_video_op_create()

    def test_b_query_video_op_get_by_user_id(self):
        query_video_op_get_by_user_id()

        query_video_op_get_by_video_id()

        query_video_op_get_by_user_video()

        query_video_op_get_by_op_id()

        query_video_op_update_process()

        query_video_op_update_comment()

        query_video_op_update_like()

        query_video_op_update_dislike()

        query_video_op_update_star()

        query_video_op_delete()

        query_video_op_search_comment_by_contains()

        query_video_op_search_comment_by_pattern()
"""

if __name__ == "__main__":
    db = get_db(TestConfig)
    unittest.main()

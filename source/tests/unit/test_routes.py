import unittest
from flask import Flask, request
from source.routes.route_search import *
from source.routes.route_user import *
from source.routes.route_video import *
from source.settings import config
from source.utils.util_serializer import *
from source.tests.unit.test_load_data import *

app = Flask(__name__)


class TestRouteSearch(unittest.TestCase):
    data = util_load_test_data()
    const_user_0 = data['const_user'][0]
    const_user_1 = data['const_user'][1]
    const_user_2 = data['const_user'][2]
    const_video_0 = data['const_video'][0]

    @classmethod
    def setUpClass(cls) -> None:
        cls.conf = config['test']

    def test_route_search_user(self):
        # Test search user by keyword
        with app.test_request_context('/search/user?keyword=' + self.const_user_0['user_name'], data={}):
            keyword = request.args.get('keyword')

            response_json = RouteSearchUser().get(self.conf).get_json()
            self.assertIsNotNone(response_json["body"], msg="Response json should contains body")

            # route calls service layer function, so two layers should retrieve same result
            self.assertEqual(response_json["body"][0]["user_id"], self.const_user_0['_id']['$oid'],
                             msg="First matched user id")
            self.assertEqual(response_json["body"][0]["user_email"], self.const_user_0['user_email'],
                             msg="First matched user email")
            self.assertEqual(response_json["body"][0]["user_name"], self.const_user_0['user_name'],
                             msg="First matched user name")

    def test_route_search_video(self):
        # Test search video by keyword
        with app.test_request_context(
                '/search/video?keyword=xixihaha', data={}):
            keyword = request.args.get('keyword')

            response_json = RouteSearchVideo().get(self.conf).get_json()
            self.assertIsNotNone(response_json["body"], msg="Response json should contains body")
            self.assertEqual(response_json["body"][0]["video_id"], "5f88c0307a6eb86b0eccc8d2",
                             msg="First matched video id")
            self.assertEqual(response_json["body"][0]["video_title"], "XiXiHaHa", msg="First matched video title")
            self.assertEqual(response_json["body"][0]["video_raw_content"],
                             "https://s3.amazon.com/54asd56a4d5asdasd.mp4", msg="First matched video content")


class TestRouteUser(unittest.TestCase):
    data = util_load_test_data()
    const_user_0 = data['const_user'][0]
    const_user_1 = data['const_user'][1]
    const_user_2 = data['const_user'][2]

    @classmethod
    def setUpClass(cls) -> None:
        cls.conf = config['test']

    def test_a_route_user_post(self):
        pass

    def test_b_route_user_get(self):
        pass

    def test_c_route_user_put(self):
        pass

    def test_d_route_user_delete(self):
        pass

    def test_e_route_user_login(self):
        pass

    def test_f_route_user_logout(self):
        pass

    def test_g_route_user_like(self):
        pass

    def test_h_route_user_dislike(self):
        pass

    def test_i_route_user_star(self):
        pass

    def test_j_route_user_comment(self):
        pass

    def test_k_route_user_process(self):
        pass


if __name__ == '__main__':
    unittest.main()

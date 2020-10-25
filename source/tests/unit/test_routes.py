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
            # service_search_json = util_serializer_api_response(service_search_video(conf=conf, name=keyword,
            #                                                                         ignore_case=True, format="json",
            #                                                                         slice=True), 200).get_json()

            # self.assertEqual(response_json["body"][0]["user_id"], service_search_json["body"][0]["user_id"],
            #                  msg="First matched user id")
            # self.assertEqual(response_json["body"][0]["user_email"], service_search_json["body"][0]["user_email"],
            #                  msg="First matched user email")
            # self.assertEqual(response_json["body"][0]["user_name"], service_search_json["body"][0]["user_name"],
            #                  msg="First matched user name")

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


if __name__ == '__main__':
    unittest.main()

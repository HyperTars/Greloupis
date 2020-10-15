import unittest
from flask import Flask, request
from source.routes.route_search import *
from source.routes.route_user import *
from source.routes.route_video import *
from source.settings import config
from source.utils.util_serializer import *

app = Flask(__name__)


class TestRoutes(unittest.TestCase):

    def test_route(self):
        '''
            Test search user by keyword
        '''
        with app.test_request_context(
                '/search/user?keyword=hypertars', data={}):
            keyword = request.args.get('keyword')
            conf = config["test"]

            response_json = RouteSearchUser().get(conf).get_json()
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

            self.assertEqual(response_json["body"][0]["user_id"], "5f887100ddbec35968356a98",
                             msg="First matched user id")
            self.assertEqual(response_json["body"][0]["user_email"], "hypertars@gmail.com",
                             msg="First matched user email")
            self.assertEqual(response_json["body"][0]["user_name"], "hypertars",
                             msg="First matched user name")


        '''
            Test search video by keyword
        '''
        with app.test_request_context(
                '/search/video?keyword=xixihaha', data={}):
            keyword = request.args.get('keyword')

            response_json = RouteSearchVideo().get(conf).get_json()
            self.assertIsNotNone(response_json["body"], msg="Response json should contains body")
            self.assertEqual(response_json["body"][0]["video_id"], "5f8871e4ddbec35968356a99",
                             msg="First matched video id")
            self.assertEqual(response_json["body"][0]["video_title"], "XiXiHaHa", msg="First matched video title")
            self.assertEqual(response_json["body"][0]["video_raw_content"],
                             "https://s3.amazon.com/54asd56a4d5asdasd.mp4", msg="First matched video content")

    def test_user(self):
        pass

    def test_video(self):
        pass


if __name__ == '__main__':
    unittest.main()

import unittest
from flask import Flask, request
from source.routes.route_search import *
from source.routes.route_user import *
from source.routes.route_video import *

app = Flask(__name__)

class TestRoutes(unittest.TestCase):

    def test_route(self):
        '''
            Test search user by keyword
        '''
        with app.test_request_context(
            '/search/user?keyword=hypertars', data={}):
            keyword = request.args.get('keyword')

            response_json = RouteSearchUser().get().get_json()
            self.assertIsNotNone(response_json["body"], msg="Response json should contains body")
            self.assertEqual(response_json["body"][0]["user_id"], "5f886cfc9da357118cf8623b", msg="First matched user id")
            self.assertEqual(response_json["body"][0]["user_email"], "hypertars@gmail.com", msg="First matched user email")
            self.assertEqual(response_json["body"][0]["user_name"], "hypertars", msg="First matched user name")


        '''
            Test search video by keyword
        '''
        with app.test_request_context(
            '/search/video?keyword=xixihaha', data={}):
            keyword = request.args.get('keyword')

            response_json = RouteSearchVideo().get().get_json()
            self.assertIsNotNone(response_json["body"], msg="Response json should contains body")
            self.assertEqual(response_json["body"][0]["video_id"], "5f886eb79da357118cf8623c", msg="First matched video id")
            self.assertEqual(response_json["body"][0]["video_title"], "XiXiHaHa", msg="First matched video title")
            self.assertEqual(response_json["body"][0]["video_raw_content"], "https://s3.amazon.com/54asd56a4d5asdasd.mp4", msg="First matched video content")


    def test_user(self):
        pass
    
    def test_video(self):
        pass

if __name__ == '__main__':
    unittest.main()
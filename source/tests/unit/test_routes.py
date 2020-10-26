import unittest
from flask import Flask, request
from mongoengine.connection import disconnect
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
            self.assertEqual(response_json["body"][0]["video_id"], "5f88c0307a6eb86b0eccc8d2",
                             msg="First matched video id")
            self.assertEqual(response_json["body"][0]["video_title"], "XiXiHaHa", msg="First matched video title")
            self.assertEqual(response_json["body"][0]["video_raw_content"],
                             "https://s3.amazon.com/54asd56a4d5asdasd.mp4", msg="First matched video content")


class TestRouteUser(unittest.TestCase):
    data = util_load_test_data()
    const_user_0 = data['const_user'][0]
    const_video_0 = data['const_video'][0]
    const_video_op_0 = data['const_video_op'][0]

    @classmethod
    def setUpClass(cls) -> None:
        cls.conf = config['test']

    def test_a_route_user_post(self):
        pass

    def test_b_route_user_get(self):
        temp_user_id = self.const_user_0['_id']['$oid']

        disconnect(alias='default')
        with app.test_request_context(
                '/user/' + temp_user_id, data={}):
            response_json = UserUserId().get(user_id=temp_user_id, conf=self.conf).get_json()

        disconnect(alias='default')
        service_result = service_user_get_info(self.conf, temp_user_id)

        # same result length
        self.assertEqual(len(service_result["user"]), len(response_json["body"]["user"]))
        self.assertEqual(len(service_result["video"]), len(response_json["body"]["video"]))
        self.assertEqual(len(service_result["video_op"]), len(response_json["body"]["video_op"]))

        disconnect(alias='default')
        wrong_id = '12345678123456781234567'
        with app.test_request_context(
                '/user/' + wrong_id + '/process', data={}):
            self.assertEqual(UserUserIdProcess().get(user_id=wrong_id, conf=self.conf).status_code,
                             util_error_handler(ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)).status_code)

    def test_c_route_user_put(self):
        pass

    def test_d_route_user_delete(self):
        pass

    def test_e_route_user_login(self):
        pass

    def test_f_route_user_logout(self):
        pass

    def test_g_route_user_like(self):
        temp_user_id = self.const_user_0['_id']['$oid']

        disconnect(alias='default')
        with app.test_request_context(
                '/user/' + temp_user_id + '/like', data={}):
            response_json = UserUserIdLike().get(user_id=temp_user_id, conf=self.conf).get_json()

        disconnect(alias='default')
        service_result = service_user_get_like(self.conf, temp_user_id)

        # same result length
        self.assertEqual(len(service_result), len(response_json["body"]))

        # same result value
        for i in range(len(service_result)):
            self.assertEqual(service_result[i]["user_id"], response_json["body"][i]["user_id"])
            self.assertEqual(service_result[i]["video_id"], response_json["body"][i]["video_id"])

        disconnect(alias='default')
        wrong_id = '12345678123456781234567'
        with app.test_request_context(
                '/user/' + wrong_id + '/process', data={}):
            self.assertEqual(UserUserIdProcess().get(user_id=wrong_id, conf=self.conf).status_code,
                             util_error_handler(ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)).status_code)

    def test_h_route_user_dislike(self):
        temp_user_id = self.const_user_0['_id']['$oid']

        disconnect(alias='default')
        with app.test_request_context(
                '/user/' + temp_user_id + '/dislike', data={}):
            response_json = UserUserIdDislike().get(user_id=temp_user_id, conf=self.conf).get_json()

        disconnect(alias='default')
        service_result = service_user_get_dislike(self.conf, temp_user_id)

        # same result length
        self.assertEqual(len(service_result), len(response_json["body"]))

        # same result value
        for i in range(len(service_result)):
            self.assertEqual(service_result[i]["user_id"], response_json["body"][i]["user_id"])
            self.assertEqual(service_result[i]["video_id"], response_json["body"][i]["video_id"])

        disconnect(alias='default')
        wrong_id = '12345678123456781234567'
        with app.test_request_context(
                '/user/' + wrong_id + '/process', data={}):
            self.assertEqual(UserUserIdProcess().get(user_id=wrong_id, conf=self.conf).status_code,
                             util_error_handler(ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)).status_code)

    def test_i_route_user_star(self):
        temp_user_id = self.const_user_0['_id']['$oid']

        disconnect(alias='default')
        with app.test_request_context(
                '/user/' + temp_user_id + '/star', data={}):
            response_json = UserUserIdStar().get(user_id=temp_user_id, conf=self.conf).get_json()

        disconnect(alias='default')
        service_result = service_user_get_star(self.conf, temp_user_id)

        # same result length
        self.assertEqual(len(service_result), len(response_json["body"]))

        # same result value
        for i in range(len(service_result)):
            self.assertEqual(service_result[i]["user_id"], response_json["body"][i]["user_id"])
            self.assertEqual(service_result[i]["video_id"], response_json["body"][i]["video_id"])

        disconnect(alias='default')
        wrong_id = '12345678123456781234567'
        with app.test_request_context(
                '/user/' + wrong_id + '/process', data={}):
            self.assertEqual(UserUserIdProcess().get(user_id=wrong_id, conf=self.conf).status_code,
                             util_error_handler(ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)).status_code)

    def test_j_route_user_comment(self):
        temp_user_id = self.const_user_0['_id']['$oid']

        disconnect(alias='default')
        with app.test_request_context(
                '/user/' + temp_user_id + '/comment', data={}):
            response_json = UserUserIdComment().get(user_id=temp_user_id, conf=self.conf).get_json()

        disconnect(alias='default')
        service_result = service_user_get_comment(self.conf, temp_user_id)

        # same result length
        self.assertEqual(len(service_result), len(response_json["body"]))

        # same result value
        for i in range(len(service_result)):
            self.assertEqual(service_result[i]["user_id"], response_json["body"][i]["user_id"])
            self.assertEqual(service_result[i]["video_id"], response_json["body"][i]["video_id"])
            self.assertEqual(service_result[i]["comment"], response_json["body"][i]["comment"])

        disconnect(alias='default')
        wrong_id = '12345678123456781234567'
        with app.test_request_context(
                '/user/' + wrong_id + '/process', data={}):
            self.assertEqual(UserUserIdProcess().get(user_id=wrong_id, conf=self.conf).status_code,
                             util_error_handler(ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)).status_code)

    def test_k_route_user_process(self):
        temp_user_id = self.const_user_0['_id']['$oid']

        disconnect(alias='default')
        with app.test_request_context(
                '/user/' + temp_user_id + '/process', data={}):
            response_json = UserUserIdProcess().get(user_id=temp_user_id, conf=self.conf).get_json()

        disconnect(alias='default')
        service_result = service_user_get_process(self.conf, temp_user_id)

        # same result length
        self.assertEqual(len(service_result), len(response_json["body"]))

        # same result value
        for i in range(len(service_result)):
            self.assertEqual(service_result[i]["user_id"], response_json["body"][i]["user_id"])
            self.assertEqual(service_result[i]["video_id"], response_json["body"][i]["video_id"])
            self.assertEqual(service_result[i]["process"], response_json["body"][i]["process"])

        disconnect(alias='default')
        wrong_id = '12345678123456781234567'
        with app.test_request_context(
                '/user/' + wrong_id + '/process', data={}):
            self.assertEqual(UserUserIdProcess().get(user_id=wrong_id, conf=self.conf).status_code,
                             util_error_handler(ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)).status_code)


if __name__ == '__main__':
    unittest.main()

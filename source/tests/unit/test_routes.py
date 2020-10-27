import unittest
from flask import Flask, request
from mongoengine.connection import disconnect
from source.routes.route_search import *
from source.routes.route_user import *
from source.routes.route_video import *
from source.settings import config
from source.utils.util_serializer import *
from source.tests.unit.test_load_data import *
import platform as pf
import copy

app = Flask(__name__)


class TestRouteSearch(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.data = util_load_test_data()
        if pf.python_version()[:3] != '3.7' and pf.python_version()[:3] != '3.8':
            print("Your python ver." + pf.python_version() + " is not supported. Please use python 3.7 or 3.8")
            exit()
        get_db(config['test'])
        cls.conf = config['test']

    def test_route_search_user(self):
        # Test search user by keyword
        with app.test_request_context('/search/user?keyword=' + self.data['const_user'][0]['user_name'], data={}):
            keyword = request.args.get('keyword')

            response_json = RouteSearchUser().get(self.conf).get_json()
            self.assertEqual(response_json["body"][0]["user_id"], self.data['const_user'][0]['_id']['$oid'],
                             msg="First matched user id")
            self.assertEqual(response_json["body"][0]["user_email"], self.data['const_user'][0]['user_email'],
                             msg="First matched user email")
            self.assertEqual(response_json["body"][0]["user_name"], self.data['const_user'][0]['user_name'],
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

    @classmethod
    def setUpClass(cls) -> None:
        cls.data = util_load_test_data()
        if pf.python_version()[:3] != '3.7' and pf.python_version()[:3] != '3.8':
            print("Your python ver." + pf.python_version() + " is not supported. Please use python 3.7 or 3.8")
            exit()
        get_db(config['test'])
        cls.conf = config['test']

    def test_a_route_user_post(self):
        pass

    def test_b_route_user_get(self):
        temp_user_id = self.data['const_user'][0]['_id']['$oid']

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
            self.assertEqual(UserUserId().get(user_id=wrong_id, conf=self.conf).status_code,
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
        temp_user_id = self.data['const_user'][0]['_id']['$oid']

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
            self.assertEqual(UserUserIdLike().get(user_id=wrong_id, conf=self.conf).status_code,
                             util_error_handler(ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)).status_code)

    def test_h_route_user_dislike(self):
        temp_user_id = self.data['const_user'][0]['_id']['$oid']

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
            self.assertEqual(UserUserIdDislike().get(user_id=wrong_id, conf=self.conf).status_code,
                             util_error_handler(ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)).status_code)

    def test_i_route_user_star(self):
        temp_user_id = self.data['const_user'][0]['_id']['$oid']

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
            self.assertEqual(UserUserIdStar().get(user_id=wrong_id, conf=self.conf).status_code,
                             util_error_handler(ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)).status_code)

    def test_j_route_user_comment(self):
        temp_user_id = self.data['const_user'][0]['_id']['$oid']

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
            self.assertEqual(UserUserIdComment().get(user_id=wrong_id, conf=self.conf).status_code,
                             util_error_handler(ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)).status_code)

    def test_k_route_user_process(self):
        temp_user_id = self.data['const_user'][0]['_id']['$oid']

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


class TestRouteVideo(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.data = util_load_test_data()
        if pf.python_version()[:3] != '3.7' and pf.python_version()[:3] != '3.8':
            print("Your python ver." + pf.python_version() + " is not supported. Please use python 3.7 or 3.8")
            exit()
        get_db(config['test'])
        cls.conf = config['test']
        cls.final_video_name = "full info hh"

    def test_a_video_post(self):
        post_data = self.data['temp_video'][0]

        # post video
        with app.test_request_context('/video', data=post_data):
            response_json = Video().post(self.conf).get_json()
            self.assertEqual(response_json["body"][0]["user_id"], post_data["user_id"])
            self.assertEqual(response_json["body"][0]["video_title"], post_data["video_title"])

        # SERVICE_MISSING_PARAM
        with app.test_request_context('/video', data={}):
            error_json = Video().post(self.conf).get_json()
            self.assertEqual(error_json["code"], 400)

    def test_b_video_get(self):
        temp_video_title = self.data['temp_video'][0]["video_title"]
        temp_video = util_serializer_mongo_results_to_array(query_video_get_by_title(temp_video_title))[0]
        temp_video_id = temp_video["video_id"]
        wrong_id_1 = "123123123"
        wrong_id_2 = "5f88f883e6ac4f89900ac984"

        # successful case
        with app.test_request_context('/video/' + temp_video_id, data={}):
            response_json = VideoVideoId().get(temp_video_id, self.conf).get_json()
            self.assertEqual(response_json["body"][0]["user_id"], temp_video["user_id"])
            self.assertEqual(response_json["body"][0]["video_title"], temp_video["video_title"])

        # invalid Param
        with app.test_request_context('/video/' + wrong_id_1, data={}):
            error_json = VideoVideoId().get(temp_video_id, self.conf).get_json()
            self.assertEqual(error_json["code"], 400)
            self.assertEqual(error_json["message"], ErrorCode.SERVICE_INVALID_ID_OBJ.get_msg())

        # video not found
        with app.test_request_context('/video/' + wrong_id_2, data={}):
            error_json = VideoVideoId().get(temp_video_id, self.conf).get_json()
            self.assertEqual(error_json["code"], 404)
            self.assertEqual(error_json["message"], ErrorCode.SERVICE_VIDEO_NOT_FOUND.get_msg())

    def test_c_video_update(self):
        temp_video_title = self.data['temp_video'][0]["video_title"]
        temp_video = util_serializer_mongo_results_to_array(query_video_get_by_title(temp_video_title))[0]
        temp_video_id = temp_video["video_id"]

        wrong_id_1 = "123123123"
        wrong_id_2 = "5f88f883e6ac4f89900ac984"

        update_video = self.data['temp_video'][1]
        update_video["video_title"] = self.final_video_name

        wrong_status_data = copy.deepcopy(self.data['temp_video'][1])
        wrong_status_data["video_status"] = "122345"

        # successful case
        with app.test_request_context('/video/' + temp_video_id, data=update_video):
            response_json = VideoVideoId().put(temp_video_id, self.conf).get_json()
            self.assertEqual(response_json["body"][0]["user_id"], update_video["user_id"])
            self.assertEqual(response_json["body"][0]["video_title"], update_video["video_title"])
            self.assertEqual(response_json["body"][0]["video_raw_size"], update_video["video_raw_size"])
            self.assertEqual(response_json["body"][0]["video_status"], update_video["video_status"])

        # invalid video_status
        with app.test_request_context('/video/' + temp_video_id, data=wrong_status_data):
            error_json = VideoVideoId().put(temp_video_id, self.conf).get_json()
            self.assertEqual(error_json["code"], 400)
            self.assertEqual(error_json["message"], ErrorCode.SERVICE_VIDEO_INVALID_STATUS.get_msg())

        # invalid Param
        with app.test_request_context('/video/' + wrong_id_1, data={}):
            error_json = VideoVideoId().get(temp_video_id, self.conf).get_json()
            self.assertEqual(error_json["code"], 400)
            self.assertEqual(error_json["message"], ErrorCode.SERVICE_INVALID_ID_OBJ.get_msg())

        # video not found
        with app.test_request_context('/video/' + wrong_id_2, data=update_video):
            error_json = VideoVideoId().get(temp_video_id, self.conf).get_json()
            self.assertEqual(error_json["code"], 404)
            self.assertEqual(error_json["message"], ErrorCode.SERVICE_VIDEO_NOT_FOUND.get_msg())

    def test_z_video_delete(self):
        temp_video = util_serializer_mongo_results_to_array(query_video_get_by_title(self.final_video_name))[0]
        temp_video_id = temp_video["video_id"]

        # successful case
        with app.test_request_context('/video/' + temp_video_id, data={}):
            response_json = VideoVideoId().delete(temp_video_id, self.conf).get_json()
            delete_search = query_video_get_by_video_id(temp_video_id)
            self.assertEqual(len(delete_search), 0)


if __name__ == '__main__':
    unittest.main()

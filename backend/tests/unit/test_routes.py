import datetime
import json
import unittest

from flask_jwt_extended import JWTManager, create_access_token
from flask_restx import Api
from mongoengine.connection import disconnect
from werkzeug.datastructures import Headers

from routes.route_search import RouteSearchUser, RouteSearchVideo
from routes.route_user import UserUserId, UserUserIdStar, \
    UserUserIdComment, UserUserIdDislike, UserUserIdLike, \
    UserUserIdProcess, user
from routes.route_video import Video, VideoVideoId, \
    VideoVideoIdComment, VideoVideoIdCommentUserId, VideoVideoIdDislike, \
    VideoVideoIdDislikeUserId, VideoVideoIdLike, VideoVideoIdLikeUserId, \
    VideoVideoIdProcessUserId, VideoVideoIdStar, VideoVideoIdStarUserId, \
    VideoVideoIdView
from settings import config
from utils.util_jwt import blacklist, util_get_formated_response
from utils.util_serializer import util_serializer_mongo_results_to_array
from utils.util_tests import util_tests_load_data, \
    util_tests_python_version
from service.service_user import service_user_get_comment, \
    service_user_get_dislike, service_user_get_info, service_user_get_like, \
    service_user_get_process, service_user_get_star
from utils.util_error_handler import util_error_handler
from db.query_video import query_video_get_by_video_id, \
    query_video_get_by_title
from models.model_errors import ErrorCode, ServiceError
from flask import Flask, Blueprint
import copy

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/')
api = Api(blueprint)
api.add_namespace(user)
app.register_blueprint(blueprint)
jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@jwt.expired_token_loader
def expired_token_callback():
    return util_get_formated_response(code=-10000,
                                      msg='The token has expired')


@jwt.revoked_token_loader
def revoked_token_callback():
    return util_get_formated_response(code=-10000,
                                      msg='The token has been revoked')


class TestUserRoute(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.config['TESTING'] = True
        app.config.from_object(config['test'])
        self.client = app.test_client()

    def test_route_login(self):
        response = self.client.post('/user/login', data={
            'user_name': 'fatbin',
            'user_password': 'fatbin_pass'
        })

        json_data = response.data
        json_dict = json.loads(json_data)
        print("test", json_dict['user_name'])
        # self.assertEqual('fatbin', json_dict['user_name'],
        #                  "login succeed, user name matched")

    def test_route_logout(self):
        with self.app.app_context():
            expires = datetime.timedelta(hours=20)
            token = create_access_token(identity='fatbin',
                                        expires_delta=expires, fresh=True)
            headers = Headers({'Authorization': 'Bearer ' + token})
            response = self.client.post('/user/logout', data={
                'user_name': 'fatbin',
                'user_password': 'fatbin_pass'
            }, headers=headers)
            json_data = response.data
            json_dict = json.loads(json_data)
            # print("test", json_dict)
            self.assertEqual(200, json_dict['code'], json_dict['message'])


class TestRouteSearch(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if util_tests_python_version() is False:
            exit()
        cls.data = util_tests_load_data()
        cls.conf = config['test']

    def test_route_search_user(self):
        # Test search user by keyword
        with app.test_request_context(
                '/search/user?keyword=' + self.data['const_user'][0][
                    'user_name'], data={}):
            response_json = RouteSearchUser().get(self.conf).get_json()
            self.assertEqual(response_json["body"][0]["user_id"],
                             self.data['const_user'][0]['_id']['$oid'],
                             msg="First matched user id")
            self.assertEqual(response_json["body"][0]["user_email"],
                             self.data['const_user'][0]['user_email'],
                             msg="First matched user email")
            self.assertEqual(response_json["body"][0]["user_name"],
                             self.data['const_user'][0]['user_name'],
                             msg="First matched user name")

    def test_route_search_video(self):
        # Test search video by keyword
        with app.test_request_context(
                '/search/video?keyword=xixihaha', data={}):
            response_json = RouteSearchVideo().get(self.conf).get_json()
            self.assertEqual(response_json["body"][0]["video_id"],
                             "5f88c0307a6eb86b0eccc8d2",
                             msg="First matched video id")
            self.assertEqual(response_json["body"][0]["video_title"],
                             "XiXiHaHa", msg="First matched video title")
            self.assertEqual(response_json["body"][0]["video_raw_content"],
                             "https://s3.amazon.com/54asd56a4d5asdasd.mp4",
                             msg="First matched video content")


class TestRouteUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if util_tests_python_version() is False:
            exit()
        cls.data = util_tests_load_data()
        cls.conf = config['test']

    def test_a_route_user_post(self):
        pass

    def test_b_route_user_get(self):
        temp_user_id = self.data['const_user'][0]['_id']['$oid']

        disconnect(alias='default')
        with app.test_request_context(
                '/user/' + temp_user_id, data={}):
            response_json = UserUserId().get(user_id=temp_user_id,
                                             conf=self.conf).get_json()

        disconnect(alias='default')
        service_result = service_user_get_info(self.conf, temp_user_id)

        # same result length
        self.assertEqual(len(service_result["user"]),
                         len(response_json["body"]["user"]))
        self.assertEqual(len(service_result["video"]),
                         len(response_json["body"]["video"]))
        self.assertEqual(len(service_result["video_op"]),
                         len(response_json["body"]["video_op"]))

        disconnect(alias='default')
        wrong_id = '12345678123456781234567'
        with app.test_request_context(
                '/user/' + wrong_id + '/process', data={}):
            self.assertEqual(
                UserUserId().get(user_id=wrong_id, conf=self.conf).status_code,
                util_error_handler(
                    ServiceError(
                        ErrorCode.SERVICE_INVALID_ID_OBJ)).status_code)

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
            response_json = UserUserIdLike().get(user_id=temp_user_id,
                                                 conf=self.conf).get_json()

        disconnect(alias='default')
        service_result = service_user_get_like(self.conf, temp_user_id)

        # same result length
        self.assertEqual(len(service_result), len(response_json["body"]))

        # same result value
        for i in range(len(service_result)):
            self.assertEqual(service_result[i]["user_id"],
                             response_json["body"][i]["user_id"])
            self.assertEqual(service_result[i]["video_id"],
                             response_json["body"][i]["video_id"])

        disconnect(alias='default')
        wrong_id = '12345678123456781234567'
        with app.test_request_context(
                '/user/' + wrong_id + '/process', data={}):
            code1 = UserUserIdLike().get(user_id=wrong_id,
                                         conf=self.conf).status_code
            code2 = util_error_handler(ServiceError(
                ErrorCode.SERVICE_INVALID_ID_OBJ)).status_code

            self.assertEqual(code1, code2)

    def test_h_route_user_dislike(self):
        temp_user_id = self.data['const_user'][0]['_id']['$oid']

        disconnect(alias='default')
        with app.test_request_context(
                '/user/' + temp_user_id + '/dislike', data={}):
            response_json = UserUserIdDislike().get(user_id=temp_user_id,
                                                    conf=self.conf).get_json()

        disconnect(alias='default')
        service_result = service_user_get_dislike(self.conf, temp_user_id)

        # same result length
        self.assertEqual(len(service_result), len(response_json["body"]))

        # same result value
        for i in range(len(service_result)):
            self.assertEqual(service_result[i]["user_id"],
                             response_json["body"][i]["user_id"])
            self.assertEqual(service_result[i]["video_id"],
                             response_json["body"][i]["video_id"])

        disconnect(alias='default')
        wrong_id = '12345678123456781234567'
        with app.test_request_context(
                '/user/' + wrong_id + '/process', data={}):
            code1 = UserUserIdDislike().get(user_id=wrong_id,
                                            conf=self.conf).status_code
            code2 = util_error_handler(ServiceError(
                ErrorCode.SERVICE_INVALID_ID_OBJ)).status_code
            self.assertEqual(code1, code2)

    def test_i_route_user_star(self):
        temp_user_id = self.data['const_user'][0]['_id']['$oid']

        disconnect(alias='default')
        with app.test_request_context(
                '/user/' + temp_user_id + '/star', data={}):
            response_json = UserUserIdStar().get(user_id=temp_user_id,
                                                 conf=self.conf).get_json()

        disconnect(alias='default')
        service_result = service_user_get_star(self.conf, temp_user_id)

        # same result length
        self.assertEqual(len(service_result), len(response_json["body"]))

        # same result value
        for i in range(len(service_result)):
            self.assertEqual(service_result[i]["user_id"],
                             response_json["body"][i]["user_id"])
            self.assertEqual(service_result[i]["video_id"],
                             response_json["body"][i]["video_id"])

        disconnect(alias='default')
        wrong_id = '12345678123456781234567'
        with app.test_request_context(
                '/user/' + wrong_id + '/process', data={}):
            code1 = UserUserIdStar().get(user_id=wrong_id,
                                         conf=self.conf).status_code
            code2 = util_error_handler(ServiceError(
                ErrorCode.SERVICE_INVALID_ID_OBJ)).status_code
            self.assertEqual(code1, code2)

    def test_j_route_user_comment(self):
        temp_user_id = self.data['const_user'][0]['_id']['$oid']

        disconnect(alias='default')
        with app.test_request_context(
                '/user/' + temp_user_id + '/comment', data={}):
            response_json = UserUserIdComment().get(user_id=temp_user_id,
                                                    conf=self.conf).get_json()

        disconnect(alias='default')
        service_result = service_user_get_comment(self.conf, temp_user_id)

        # same result length
        self.assertEqual(len(service_result), len(response_json["body"]))

        # same result value
        for i in range(len(service_result)):
            self.assertEqual(service_result[i]["user_id"],
                             response_json["body"][i]["user_id"])
            self.assertEqual(service_result[i]["video_id"],
                             response_json["body"][i]["video_id"])
            self.assertEqual(service_result[i]["comment"],
                             response_json["body"][i]["comment"])

        disconnect(alias='default')
        wrong_id = '12345678123456781234567'
        with app.test_request_context(
                '/user/' + wrong_id + '/process', data={}):
            code1 = UserUserIdComment().get(user_id=wrong_id,
                                            conf=self.conf).status_code
            code2 = util_error_handler(ServiceError(
                ErrorCode.SERVICE_INVALID_ID_OBJ)).status_code
            self.assertEqual(code1, code2)

    def test_k_route_user_process(self):
        temp_user_id = self.data['const_user'][0]['_id']['$oid']

        disconnect(alias='default')
        with app.test_request_context(
                '/user/' + temp_user_id + '/process', data={}):
            response_json = UserUserIdProcess().get(user_id=temp_user_id,
                                                    conf=self.conf).get_json()

        disconnect(alias='default')
        service_result = service_user_get_process(self.conf, temp_user_id)

        # same result length
        self.assertEqual(len(service_result), len(response_json["body"]))

        # same result value
        for i in range(len(service_result)):
            self.assertEqual(service_result[i]["user_id"],
                             response_json["body"][i]["user_id"])
            self.assertEqual(service_result[i]["video_id"],
                             response_json["body"][i]["video_id"])
            self.assertEqual(service_result[i]["process"],
                             response_json["body"][i]["process"])

        disconnect(alias='default')
        wrong_id = '12345678123456781234567'
        with app.test_request_context(
                '/user/' + wrong_id + '/process', data={}):
            code1 = UserUserIdProcess().get(user_id=wrong_id,
                                            conf=self.conf).status_code
            code2 = util_error_handler(ServiceError(
                ErrorCode.SERVICE_INVALID_ID_OBJ)).status_code
            self.assertEqual(code1, code2)


class TestRouteVideo(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if util_tests_python_version() is False:
            exit()
        cls.data = util_tests_load_data()
        cls.conf = config['test']
        cls.final_video_name = "full info hh"

    def test_a_video_post(self):
        post_data = self.data['temp_video'][0]

        # post video
        with app.test_request_context('/video', data=post_data):
            response_json = Video().post(self.conf).get_json()
            self.assertEqual(response_json["body"][0]["user_id"],
                             post_data["user_id"])
            self.assertEqual(response_json["body"][0]["video_title"],
                             post_data["video_title"])

        # SERVICE_MISSING_PARAM
        with app.test_request_context('/video', data={"user_id": "123"}):
            error_json = Video().post(self.conf).get_json()
            self.assertEqual(error_json["code"], 400)

    def test_b_video_get(self):
        temp_video_title = self.data['temp_video'][0]["video_title"]
        temp_video = util_serializer_mongo_results_to_array(
            query_video_get_by_title(temp_video_title))[0]
        temp_video_id = temp_video["video_id"]
        wrong_id_1 = "123123123"
        wrong_id_2 = "5f88f883e6ac4f89900ac984"

        # successful case
        with app.test_request_context('/video/' + temp_video_id, data={}):
            response_json = VideoVideoId().get(temp_video_id,
                                               self.conf).get_json()
            self.assertEqual(response_json["body"][0]["user_id"],
                             temp_video["user_id"])
            self.assertEqual(response_json["body"][0]["video_title"],
                             temp_video["video_title"])

        # invalid Param
        with app.test_request_context('/video/' + wrong_id_1, data={}):
            error_json = VideoVideoId().get(temp_video_id,
                                            self.conf).get_json()
            self.assertEqual(error_json["code"], 400)
            self.assertEqual(error_json["message"],
                             ErrorCode.SERVICE_INVALID_ID_OBJ.get_msg())

        # video not found
        with app.test_request_context('/video/' + wrong_id_2, data={}):
            error_json = VideoVideoId().get(temp_video_id,
                                            self.conf).get_json()
            self.assertEqual(error_json["code"], 404)
            self.assertEqual(error_json["message"],
                             ErrorCode.SERVICE_VIDEO_NOT_FOUND.get_msg())

    def test_c_video_update(self):
        temp_video_title = self.data['temp_video'][0]["video_title"]
        temp_video = util_serializer_mongo_results_to_array(
            query_video_get_by_title(temp_video_title))[0]
        temp_video_id = temp_video["video_id"]

        wrong_id_1 = "123123123"
        wrong_id_2 = "5f88f883e6ac4f89900ac984"

        update_video = self.data['temp_video'][1]
        update_video["video_title"] = self.final_video_name

        wrong_status_data = copy.deepcopy(self.data['temp_video'][1])
        wrong_status_data["video_status"] = "122345"

        # successful case
        with app.test_request_context('/video/' + temp_video_id,
                                      data=update_video):
            response_json = VideoVideoId().put(temp_video_id,
                                               self.conf).get_json()
            self.assertEqual(response_json["body"][0]["user_id"],
                             update_video["user_id"])
            self.assertEqual(response_json["body"][0]["video_title"],
                             update_video["video_title"])
            self.assertEqual(response_json["body"][0]["video_raw_size"],
                             update_video["video_raw_size"])
            self.assertEqual(response_json["body"][0]["video_status"],
                             update_video["video_status"])

        # invalid video_status
        with app.test_request_context('/video/' + temp_video_id,
                                      data=wrong_status_data):
            error_json = VideoVideoId().put(temp_video_id,
                                            self.conf).get_json()
            self.assertEqual(error_json["code"], 400)
            self.assertEqual(error_json["message"],
                             ErrorCode.SERVICE_VIDEO_INVALID_STATUS.get_msg())

        # invalid Param
        with app.test_request_context('/video/' + wrong_id_1, data={}):
            error_json = VideoVideoId().get(temp_video_id,
                                            self.conf).get_json()
            self.assertEqual(error_json["code"], 400)
            self.assertEqual(error_json["message"],
                             ErrorCode.SERVICE_INVALID_ID_OBJ.get_msg())

        # video not found
        with app.test_request_context('/video/' + wrong_id_2,
                                      data=update_video):
            error_json = VideoVideoId().get(temp_video_id,
                                            self.conf).get_json()
            self.assertEqual(error_json["code"], 404)
            self.assertEqual(error_json["message"],
                             ErrorCode.SERVICE_VIDEO_NOT_FOUND.get_msg())

    def test_d_video_view(self):
        temp_video = util_serializer_mongo_results_to_array(
            query_video_get_by_title(self.final_video_name))[0]
        temp_video_id = temp_video["video_id"]

        wrong_id = "5f88f883e6ac4f89900ac984"

        # get view successful case
        with app.test_request_context('/video/' + temp_video_id + '/view',
                                      data={}):
            response_json = VideoVideoIdView().get(temp_video_id,
                                                   self.conf).get_json()
            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["view_count"], 0)

        # get view error case
        with app.test_request_context('/video/' + wrong_id + '/view', data={}):
            error_json = VideoVideoIdView().get(wrong_id, self.conf).get_json()
            self.assertEqual(error_json["code"], 404)
            self.assertEqual(error_json["message"],
                             ErrorCode.MONGODB_VIDEO_OP_NOT_FOUND.get_msg())

        # add view successful case
        with app.test_request_context('/video/' + temp_video_id + '/view',
                                      data={}):
            response_json = VideoVideoIdView().put(temp_video_id,
                                                   self.conf).get_json()
            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["view_count"], 1)

        # add view error case
        with app.test_request_context('/video/' + wrong_id + '/view', data={}):
            VideoVideoIdView().put(temp_video_id, self.conf).get_json()
            self.assertEqual(error_json["code"], 404)
            self.assertEqual(error_json["message"],
                             ErrorCode.MONGODB_VIDEO_OP_NOT_FOUND.get_msg())

    def test_e_video_comment(self):
        temp_video = util_serializer_mongo_results_to_array(
            query_video_get_by_title(self.final_video_name))[0]
        temp_video_id = temp_video["video_id"]
        temp_user_id = temp_video["user_id"]
        temp_comment = "nice video"
        temp_comment_updated = "really nice video"

        wrong_id = "5f88f883e6ac4f89900ac984"

        # post comment successful case
        with app.test_request_context(
                '/video/' + temp_video_id + '/comment/' + temp_user_id,
                data={"comment": temp_comment}):
            response = VideoVideoIdCommentUserId().post(temp_video_id,
                                                        temp_user_id,
                                                        self.conf)
            response_json = response.get_json()
            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["comment"], temp_comment)

        # post comment error case
        with app.test_request_context(
                '/video/' + temp_video_id + '/comment/' + wrong_id,
                data={"comment": temp_comment}):
            error_json = VideoVideoIdCommentUserId().post(temp_video_id,
                                                          wrong_id,
                                                          self.conf).get_json()
            self.assertEqual(error_json["code"], 404)

        # get comment successful case
        with app.test_request_context(
                '/video/' + temp_video_id + '/comment/' + temp_user_id,
                data={}):
            response = VideoVideoIdCommentUserId().get(temp_video_id,
                                                       temp_user_id,
                                                       self.conf)
            response_json = response.get_json()
            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["comment"], temp_comment)

        # get comment error case
        with app.test_request_context(
                '/video/' + temp_video_id + '/comment/' + wrong_id,
                data={}):
            error_json = VideoVideoIdCommentUserId().get(temp_video_id,
                                                         wrong_id,
                                                         self.conf).get_json()
            self.assertEqual(error_json["code"], 404)

        # update comment successful case
        with app.test_request_context(
                '/video/' + temp_video_id + '/comment/' + temp_user_id,
                data={"comment": temp_comment_updated}):
            response = VideoVideoIdCommentUserId().put(temp_video_id,
                                                       temp_user_id,
                                                       self.conf)
            response_json = response.get_json()
            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["comment"],
                             temp_comment_updated)

        # update comment error case
        with app.test_request_context(
                '/video/' + temp_video_id + '/comment/' + wrong_id,
                data={"comment": temp_comment_updated}):
            error_json = VideoVideoIdCommentUserId().put(temp_video_id,
                                                         wrong_id,
                                                         self.conf).get_json()
            self.assertEqual(error_json["code"], 404)

        # get all comments of the video successful case
        with app.test_request_context('/video/' + temp_video_id + '/comment',
                                      data={}):
            response_json = VideoVideoIdComment().get(temp_video_id,
                                                      self.conf).get_json()
            self.assertEqual(response_json["body"][0]["video_id"],
                             temp_video_id)
            self.assertEqual(response_json["body"][0]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"][0]["comment"],
                             temp_comment_updated)

        # get all comments of the video error case
        with app.test_request_context('/video/' + wrong_id + '/comment/',
                                      data={}):
            error_json = VideoVideoIdComment().get(wrong_id,
                                                   self.conf).get_json()
            self.assertEqual(error_json["code"], 400)

        # delete comment successful case
        with app.test_request_context(
                '/video/' + temp_video_id + '/comment/' + temp_user_id,
                data={}):
            response = VideoVideoIdCommentUserId().delete(temp_video_id,
                                                          temp_user_id,
                                                          self.conf)
            response_json = response.get_json()
            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["comment"], "")

        # delete comment error case
        with app.test_request_context(
                '/video/' + temp_video_id + '/comment/' + wrong_id,
                data={}):
            error = VideoVideoIdCommentUserId().delete(temp_video_id,
                                                       wrong_id,
                                                       self.conf)
            error_json = error.get_json()
            self.assertEqual(error_json["code"], 404)

    def test_f_video_process(self):
        temp_video = util_serializer_mongo_results_to_array(
            query_video_get_by_title(self.final_video_name))[0]
        temp_video_id = temp_video["video_id"]
        temp_user_id = temp_video["user_id"]
        temp_process = 30
        temp_process_updated = 60

        wrong_id = "5f88f883e6ac4f89900ac984"

        # post process successful case
        with app.test_request_context(
                '/video/' + temp_video_id + '/process/' + temp_user_id,
                data={"process": temp_process}):
            response = VideoVideoIdProcessUserId().post(temp_video_id,
                                                        temp_user_id,
                                                        self.conf)
            response_json = response.get_json()
            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["process"], temp_process)

        # post process error case
        with app.test_request_context(
                '/video/' + temp_video_id + '/process/' + wrong_id,
                data={"process": temp_process}):
            error_json = VideoVideoIdCommentUserId().post(temp_video_id,
                                                          wrong_id,
                                                          self.conf).get_json()
            self.assertEqual(error_json["code"], 400)

        # post process error case
        with app.test_request_context(
                '/video/' + temp_video_id + '/process/' + temp_user_id,
                data={"process": -1}):
            error_json = VideoVideoIdProcessUserId().post(temp_video_id,
                                                          wrong_id,
                                                          self.conf).get_json()
            self.assertEqual(error_json["code"], 500)

        # get process successful case
        with app.test_request_context(
                '/video/' + temp_video_id + '/process/' + temp_user_id,
                data={}):
            response = VideoVideoIdProcessUserId().get(temp_video_id,
                                                       temp_user_id,
                                                       self.conf)
            response_json = response.get_json()
            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["process"], temp_process)

        # get process error case
        with app.test_request_context(
                '/video/' + temp_video_id + '/process/' + wrong_id,
                data={}):
            error_json = VideoVideoIdProcessUserId().get(temp_video_id,
                                                         wrong_id,
                                                         self.conf).get_json()
            self.assertEqual(error_json["code"], 404)

        # update process successful case
        with app.test_request_context(
                '/video/' + temp_video_id + '/process/' + temp_user_id,
                data={"process": temp_process_updated}):
            response = VideoVideoIdProcessUserId().put(temp_video_id,
                                                       temp_user_id,
                                                       self.conf)
            response_json = response.get_json()
            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["process"],
                             temp_process_updated)

        # update process error case
        with app.test_request_context(
                '/video/' + temp_video_id + '/process/' + wrong_id,
                data={"process": temp_process_updated}):
            error_json = VideoVideoIdProcessUserId().put(temp_video_id,
                                                         wrong_id,
                                                         self.conf).get_json()
            self.assertEqual(error_json["code"], 404)

        # update process error case
        with app.test_request_context(
                '/video/' + temp_video_id + '/process/' + temp_user_id,
                data={"process": -100}):
            error_json = VideoVideoIdProcessUserId().put(temp_video_id,
                                                         temp_user_id,
                                                         self.conf).get_json()
            self.assertEqual(error_json["code"], 400)

        # delete process successful case
        with app.test_request_context(
                '/video/' + temp_video_id + '/process/' + temp_user_id,
                data={}):
            response = VideoVideoIdProcessUserId().delete(temp_video_id,
                                                          temp_user_id,
                                                          self.conf)
            response_json = response.get_json()
            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["process"], 0)

        # delete process error case
        with app.test_request_context(
                '/video/' + temp_video_id + '/process/' + wrong_id,
                data={}):
            error = VideoVideoIdProcessUserId().delete(temp_video_id,
                                                       wrong_id,
                                                       self.conf)
            error_json = error.get_json()
            self.assertEqual(error_json["code"], 404)

    def test_g_video_like(self):
        temp_video = util_serializer_mongo_results_to_array(
            query_video_get_by_title(self.final_video_name))[0]
        temp_video_id = temp_video["video_id"]
        temp_user_id = temp_video["user_id"]
        wrong_id = "5f88f883e6ac4f89900ac984"

        # post like successful case
        with app.test_request_context(
                '/video/' + temp_video_id + '/like/' + temp_user_id,
                data={}):
            response_json = VideoVideoIdLikeUserId().post(temp_video_id,
                                                          temp_user_id,
                                                          self.conf).get_json()
            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["like"], True)

        # post like error case
        with app.test_request_context(
                '/video/' + temp_video_id + '/like/' + wrong_id,
                data={}):
            error_json = VideoVideoIdLikeUserId().post(temp_video_id, wrong_id,
                                                       self.conf).get_json()
            self.assertEqual(error_json["code"], 404)

        # get all likes of the video successful case
        with app.test_request_context('/video/' + temp_video_id + '/like',
                                      data={}):
            response_json = VideoVideoIdLike().get(temp_video_id,
                                                   self.conf).get_json()
            self.assertEqual(response_json["body"][0]["video_id"],
                             temp_video_id)
            self.assertEqual(response_json["body"][0]["user_id"], temp_user_id)

        # get all likes of the video error case
        with app.test_request_context('/video/' + wrong_id + '/like/',
                                      data={}):
            error_json = VideoVideoIdLike().get(wrong_id, self.conf).get_json()
            self.assertEqual(error_json["code"], 400)

        # cancel like successful case
        with app.test_request_context(
                '/video/' + temp_video_id + '/like/' + temp_user_id,
                data={}):
            response = VideoVideoIdLikeUserId().delete(temp_video_id,
                                                       temp_user_id,
                                                       self.conf)
            response_json = response.get_json()
            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["like"], False)

        # cancel like error case
        with app.test_request_context(
                '/video/' + temp_video_id + '/like/' + wrong_id,
                data={}):
            error_json = VideoVideoIdLikeUserId().delete(temp_video_id,
                                                         wrong_id,
                                                         self.conf).get_json()
            self.assertEqual(error_json["code"], 404)

    def test_h_video_dislike(self):
        temp_video = util_serializer_mongo_results_to_array(
            query_video_get_by_title(self.final_video_name))[0]
        temp_video_id = temp_video["video_id"]
        temp_user_id = temp_video["user_id"]
        wrong_id = "5f88f883e6ac4f89900ac984"

        # post dislike successful case
        with app.test_request_context(
                '/video/' + temp_video_id + '/dislike/' + temp_user_id,
                data={}):
            response = VideoVideoIdDislikeUserId().post(temp_video_id,
                                                        temp_user_id,
                                                        self.conf)
            response_json = response.get_json()
            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["dislike"], True)

        # post dislike error case
        with app.test_request_context(
                '/video/' + temp_video_id + '/dislike/' + wrong_id,
                data={}):
            error_json = VideoVideoIdDislikeUserId().post(temp_video_id,
                                                          wrong_id,
                                                          self.conf).get_json()
            self.assertEqual(error_json["code"], 404)

        # get all dislikes of the video successful case
        with app.test_request_context('/video/' + temp_video_id + '/dislike',
                                      data={}):
            response_json = VideoVideoIdDislike().get(temp_video_id,
                                                      self.conf).get_json()
            self.assertEqual(response_json["body"][0]["video_id"],
                             temp_video_id)
            self.assertEqual(response_json["body"][0]["user_id"], temp_user_id)

        # get all dislikes of the video error case
        with app.test_request_context('/video/' + wrong_id + '/dislike/',
                                      data={}):
            error_json = VideoVideoIdDislike().get(wrong_id,
                                                   self.conf).get_json()
            self.assertEqual(error_json["code"], 400)

        # cancel dislike successful case
        with app.test_request_context(
                '/video/' + temp_video_id + '/dislike/' + temp_user_id,
                data={}):
            response = VideoVideoIdDislikeUserId().delete(temp_video_id,
                                                          temp_user_id,
                                                          self.conf)
            response_json = response.get_json()
            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["dislike"], False)

        # cancel dislike error case
        with app.test_request_context(
                '/video/' + temp_video_id + '/dislike/' + wrong_id,
                data={}):
            error = VideoVideoIdDislikeUserId().delete(temp_video_id,
                                                       wrong_id,
                                                       self.conf)
            error_json = error.get_json()
            self.assertEqual(error_json["code"], 404)

    def test_i_video_star(self):
        temp_video = util_serializer_mongo_results_to_array(
            query_video_get_by_title(self.final_video_name))[0]
        temp_video_id = temp_video["video_id"]
        temp_user_id = temp_video["user_id"]
        wrong_id = "5f88f883e6ac4f89900ac984"

        # post star successful case
        with app.test_request_context(
                '/video/' + temp_video_id + '/star/' + temp_user_id,
                data={}):
            response_json = VideoVideoIdStarUserId().post(temp_video_id,
                                                          temp_user_id,
                                                          self.conf).get_json()
            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["star"], True)

        # post star error case
        with app.test_request_context(
                '/video/' + temp_video_id + '/star/' + wrong_id,
                data={}):
            error_json = VideoVideoIdStarUserId().post(temp_video_id, wrong_id,
                                                       self.conf).get_json()
            self.assertEqual(error_json["code"], 404)

        # get all stars of the video successful case
        with app.test_request_context('/video/' + temp_video_id + '/star',
                                      data={}):
            response_json = VideoVideoIdStar().get(temp_video_id,
                                                   self.conf).get_json()
            self.assertEqual(response_json["body"][0]["video_id"],
                             temp_video_id)
            self.assertEqual(response_json["body"][0]["user_id"], temp_user_id)

        # get all stars of the video error case
        with app.test_request_context('/video/' + wrong_id + '/like/',
                                      data={}):
            error_json = VideoVideoIdStar().get(wrong_id, self.conf).get_json()
            self.assertEqual(error_json["code"], 400)

        # cancel star successful case
        with app.test_request_context(
                '/video/' + temp_video_id + '/star/' + temp_user_id,
                data={}):
            response = VideoVideoIdStarUserId().delete(temp_video_id,
                                                       temp_user_id,
                                                       self.conf)
            response_json = response.get_json()
            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["star"], False)

        # cancel star error case
        with app.test_request_context(
                '/video/' + temp_video_id + '/star/' + wrong_id,
                data={}):
            error_json = VideoVideoIdStarUserId().delete(temp_video_id,
                                                         wrong_id,
                                                         self.conf).get_json()
            self.assertEqual(error_json["code"], 404)

    def test_z_video_delete(self):
        temp_video = util_serializer_mongo_results_to_array(
            query_video_get_by_title(self.final_video_name))[0]
        temp_video_id = temp_video["video_id"]

        # successful case
        with app.test_request_context('/video/' + temp_video_id, data={}):
            VideoVideoId().delete(temp_video_id, self.conf).get_json()
            delete_search = query_video_get_by_video_id(temp_video_id)
            self.assertEqual(len(delete_search), 0)

        # video not found
        with app.test_request_context('/video/' + temp_video_id, data={}):
            error_json = VideoVideoId().delete(temp_video_id,
                                               self.conf).get_json()
            self.assertEqual(error_json["code"], 404)
            self.assertEqual(error_json["message"],
                             ErrorCode.MONGODB_VIDEO_NOT_FOUND.get_msg())


"""
if __name__ == '__main__':
    unittest.main()
"""

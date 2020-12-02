import datetime
import json
import unittest
import copy
from flask import Flask, Blueprint, g
from flask_jwt_extended import JWTManager, create_access_token
from flask_restx import Api
from db.mongo import init_db
from werkzeug.datastructures import Headers

from settings import config
from utils.util_error_handler import util_error_handler
from utils.util_jwt import blacklist
from utils.util_tests import util_tests_load_data, \
    util_tests_python_version, util_tests_clean_database
from models.model_errors import ErrorCode, ServiceError
from db.query_video import query_video_get_by_video_id, \
    query_video_get_by_title, query_video_delete, \
    query_video_update
from routes.route_search import RouteSearchUser, \
    RouteSearchVideo, RouteSearchTopVideos
from routes.route_video import VideoVideoId
from routes.route_user import UserUserId, user
from routes.route_video import video
from service.service_user import service_user_get_user
from service.service_video import service_video_get_by_user
from service.service_video_op import service_video_op_get_by_user

app = Flask(__name__)
app.testing = True
blueprint = Blueprint('api', __name__, url_prefix='/')
app.config.from_object(config['test'])
api = Api(blueprint)
api.add_namespace(user)
api.add_namespace(video)
app.register_blueprint(blueprint)
jwt = JWTManager(app)
with app.app_context():
    if 'db' not in g:
        g.db = init_db()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


class TestRouteSearch(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        util_tests_clean_database() if util_tests_python_version() else exit()
        cls.data = util_tests_load_data()
        util_tests_clean_database()

    def test_route_search_user(self):
        # Test search user by keyword
        url = '/search/user?keyword='
        request = url + self.data['const_user'][0]['user_name']
        with app.test_request_context(request, data={}):
            response_json = RouteSearchUser().get().get_json()
            self.assertEqual(response_json["body"][0]["user_id"],
                             self.data['const_user'][0]['_id']['$oid'],
                             msg="First matched user id")
            self.assertEqual(response_json["body"][0]["user_email"],
                             self.data['const_user'][0]['user_email'],
                             msg="First matched user email")
            self.assertEqual(response_json["body"][0]["user_name"],
                             self.data['const_user'][0]['user_name'],
                             msg="First matched user name")

        # With Param
        request = request + '&param=name'
        with app.test_request_context(request, data={}):
            response_json = RouteSearchUser().get().get_json()
            self.assertEqual(response_json["body"][0]["user_id"],
                             self.data['const_user'][0]['_id']['$oid'])

        request = url + \
            self.data['const_user'][0]['user_email'] + \
            '&param=email'
        with app.test_request_context(request, data={}):
            response_json = RouteSearchUser().get().get_json()
            self.assertEqual(response_json["body"][0]["user_id"],
                             self.data['const_user'][0]['_id']['$oid'])

        request = url + \
            self.data['const_user'][0]['user_detail']['user_first_name'] + \
            '&param=first_name'
        with app.test_request_context(request, data={}):
            response_json = RouteSearchUser().get().get_json()
            self.assertEqual(response_json["body"][0]["user_id"],
                             self.data['const_user'][0]['_id']['$oid'])

        request = url + \
            self.data['const_user'][0]['user_detail']['user_last_name'] + \
            '&param=last_name'
        with app.test_request_context(request, data={}):
            response_json = RouteSearchUser().get().get_json()
            self.assertEqual(response_json["body"][0]["user_id"],
                             self.data['const_user'][0]['_id']['$oid'])

        request = url + \
            self.data['const_user'][0]['user_detail']['user_street1'] + \
            '&param=street1'
        with app.test_request_context(request, data={}):
            response_json = RouteSearchUser().get().get_json()
            self.assertEqual(response_json["body"][0]["user_id"],
                             self.data['const_user'][0]['_id']['$oid'])

        request = url + \
            self.data['const_user'][0]['user_detail']['user_street2'] + \
            '&param=street2'
        with app.test_request_context(request, data={}):
            response_json = RouteSearchUser().get().get_json()
            self.assertEqual(response_json["body"][0]["user_id"],
                             self.data['const_user'][0]['_id']['$oid'])

        request = url + \
            self.data['const_user'][0]['user_detail']['user_city'] + \
            '&param=city'
        with app.test_request_context(request, data={}):
            response_json = RouteSearchUser().get().get_json()
            self.assertEqual(response_json["body"][0]["user_id"],
                             self.data['const_user'][0]['_id']['$oid'])

        request = url + \
            self.data['const_user'][0]['user_detail']['user_state'] + \
            '&param=state'
        with app.test_request_context(request, data={}):
            response_json = RouteSearchUser().get().get_json()
            self.assertEqual(response_json["body"][0]["user_id"],
                             self.data['const_user'][0]['_id']['$oid'])

        request = url + \
            self.data['const_user'][0]['user_detail']['user_country'] + \
            '&param=country'
        with app.test_request_context(request, data={}):
            response_json = RouteSearchUser().get().get_json()
            self.assertEqual(response_json["body"][0]["user_id"],
                             self.data['const_user'][0]['_id']['$oid'])

        request = url + \
            self.data['const_user'][0]['user_detail']['user_zip'] + \
            '&param=zip'
        with app.test_request_context(request, data={}):
            response_json = RouteSearchUser().get().get_json()
            self.assertEqual(response_json["body"][0]["user_id"],
                             self.data['const_user'][0]['_id']['$oid'])

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        error_code = str(ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_code())
        with app.test_request_context('/search/user', data={}):
            response_json = RouteSearchUser().get().get_json()
        self.assertEqual(response_json["error_code"], error_code)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        error_code = str(ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_code())
        request = '/search/user?keyword=fake&param=fake'
        with app.test_request_context(request, data={}):
            response_json = RouteSearchUser().get().get_json()
        self.assertEqual(response_json["error_code"], error_code)

    def test_route_search_video(self):
        # Test search video by keyword
        url = '/search/video?keyword='
        request = url + self.data['const_video'][0]['video_title']
        with app.test_request_context(request, data={}):
            response_json = RouteSearchVideo().get().get_json()
            self.assertEqual(response_json["body"][0]["video_id"],
                             self.data['const_video'][0]['_id']['$oid'],
                             msg="First matched video id")
            self.assertEqual(response_json["body"][0]["video_title"],
                             self.data['const_video'][0]['video_title'],
                             msg="First matched video title")
            self.assertEqual(response_json["body"][0]["video_raw_content"],
                             self.data['const_video'][0]['video_raw_content'],
                             msg="First matched video content")

        # With Param
        request = request + '&param=title'
        with app.test_request_context(request, data={}):
            response_json = RouteSearchVideo().get().get_json()
            self.assertEqual(response_json["body"][0]["video_id"],
                             self.data['const_video'][0]['_id']['$oid'])

        request = url + \
            self.data['const_video'][0]['video_channel'] + \
            '&param=channel'
        with app.test_request_context(request, data={}):
            response_json = RouteSearchVideo().get().get_json()
            self.assertEqual(response_json["body"][0]["video_id"],
                             self.data['const_video'][0]['_id']['$oid'])

        request = url + \
            self.data['const_video'][0]['video_description'] + \
            '&param=description'
        with app.test_request_context(request, data={}):
            response_json = RouteSearchVideo().get().get_json()
            self.assertEqual(response_json["body"][0]["video_id"],
                             self.data['const_video'][0]['_id']['$oid'])

        request = url + \
            self.data['const_video'][0]['video_category'][0] + \
            '&param=category'
        with app.test_request_context(request, data={}):
            response_json = RouteSearchVideo().get().get_json()
            self.assertEqual(response_json["body"][0]["video_id"],
                             self.data['const_video'][0]['_id']['$oid'])

        request = url + \
            self.data['const_video'][0]['video_tag'][0] + \
            '&param=tag'
        with app.test_request_context(request, data={}):
            response_json = RouteSearchVideo().get().get_json()
            self.assertEqual(response_json["body"][0]["video_id"],
                             self.data['const_video'][0]['_id']['$oid'])

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        error_code = str(ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_code())
        with app.test_request_context('/search/video', data={}):
            response_json = RouteSearchVideo().get().get_json()
        self.assertEqual(response_json["error_code"], error_code)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        error_code = str(ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_code())
        request = '/search/video?keyword=fake&param=fake'
        with app.test_request_context(request, data={}):
            response_json = RouteSearchVideo().get().get_json()
        self.assertEqual(response_json["error_code"], error_code)

    def test_route_search_top_videos(self):
        # Test search video by keyword
        url = '/search/video/top?keyword='
        request = url + 'video_upload_time'
        with app.test_request_context(request, data={}):
            response_json = RouteSearchTopVideos().get().get_json()
            self.assertEqual(response_json["body"][0]["video_id"],
                             self.data['const_video'][0]['_id']['$oid'])

        request = url + 'video_like'
        with app.test_request_context(request, data={}):
            response_json = RouteSearchTopVideos().get().get_json()
            self.assertEqual(response_json["body"][0]["video_id"],
                             self.data['const_video'][0]['_id']['$oid'])

        request = url + 'video_share'
        with app.test_request_context(request, data={}):
            response_json = RouteSearchTopVideos().get().get_json()
            self.assertEqual(response_json["body"][0]["video_id"],
                             self.data['const_video'][0]['_id']['$oid'])

        request = url + 'video_star'
        with app.test_request_context(request, data={}):
            response_json = RouteSearchTopVideos().get().get_json()
            self.assertEqual(response_json["body"][0]["video_id"],
                             self.data['const_video'][0]['_id']['$oid'])

        request = url + 'video_view'
        with app.test_request_context(request, data={}):
            response_json = RouteSearchTopVideos().get().get_json()
            self.assertEqual(response_json["body"][0]["video_id"],
                             self.data['const_video'][0]['_id']['$oid'])

        request = url + 'video_duration'
        with app.test_request_context(request, data={}):
            response_json = RouteSearchTopVideos().get().get_json()
            self.assertEqual(response_json["body"][0]["video_id"],
                             self.data['const_video'][0]['_id']['$oid'])

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        error_code = str(ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_code())
        with app.test_request_context('/search/video/top', data={}):
            response_json = RouteSearchTopVideos().get().get_json()
        self.assertEqual(response_json["error_code"], error_code)

        # Raise Error: ErrorCode.ROUTE_INVALID_REQUEST_PARAM
        error_code = str(ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_code())
        request = '/search/video/top?keyword=fake'
        with app.test_request_context(request, data={}):
            response_json = RouteSearchTopVideos().get().get_json()
        self.assertEqual(response_json["error_code"], error_code)


class TestRouteUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.data = util_tests_load_data()
        util_tests_clean_database()

    def test_a_route_user_login(self):
        url = '/user/login'
        data = {'user_name': self.data['const_user'][0]['user_name'],
                'user_password': self.data['const_user'][0]['user_name']}
        with app.test_client() as client:
            response = client.post(url, data=data)
            json_data = response.data
            json_dict = json.loads(json_data)
            self.assertEquals(
                json_dict['user_name'],
                self.data['const_user'][0]['user_name'])

        headers = Headers({'X-Forward-For': '127.0.0.0'})
        data = {'user_name': self.data['const_user'][1]['user_name'],
                'user_password': self.data['const_user'][1]['user_name']}
        with app.test_client() as client:
            response = client.post(url, data=data, headers=headers)
            json_data = response.data
            json_dict = json.loads(json_data)
            self.assertEquals(
                json_dict['user_name'],
                self.data['const_user'][1]['user_name'])

    def test_b_route_user_logout(self):
        url = '/user/login'
        data = {'user_name': self.data['const_user'][0]['user_name'],
                'user_password': self.data['const_user'][0]['user_name']}
        headers = {'X-Forward-For': '127.0.0.0'}
        with app.test_client() as client:
            response = client.post(url, data=data, headers=headers)
            json_data = response.data
            json_dict = json.loads(json_data)
            token = json_dict['user_token']
            headers = Headers({'Authorization': 'Bearer ' + token})
            response = client.post('/user/logout', headers=headers)
            json_data = response.data
            json_dict = json.loads(json_data)
            self.assertEqual(200, json_dict['code'], json_dict['message'])

    def test_b_route_user_get(self):
        uid = self.data['const_user'][0]['_id']['$oid']
        url = '/user/' + uid
        with app.test_request_context(url, data={}):
            response = UserUserId().get(user_id=uid)
        body = response.get_json()['body']
        service_user = service_user_get_user(user_id=uid)
        service_video = service_video_get_by_user(user_id=uid)
        service_op = service_video_op_get_by_user(user_id=uid)

        self.assertEqual(service_user['user_id'], body['user']['user_id'])
        self.assertEqual(len(service_video), len(body['video']))
        self.assertEqual(len(service_op), len(body['video_op']))

        wrong_id = '12345678123456781234567'
        with app.test_request_context(
                '/user/' + wrong_id + '/process', data={}):
            self.assertEqual(
                UserUserId().get(user_id=wrong_id).status_code,
                util_error_handler(
                    ServiceError(
                        ErrorCode.SERVICE_INVALID_ID_OBJ)).status_code)

    def test_c_route_user_token_workflow(self):
        # post (register)
        url = '/user'
        data = {'user_name': self.data['temp_user'][0]['user_name'],
                'user_email': self.data['temp_user'][0]['user_email'],
                'user_password': self.data['temp_user'][0]['user_name']}
        with app.test_client() as client:
            response = client.post(url, data=data)
            json_data = response.data
            json_dict = json.loads(json_data)
            self.assertEquals(
                json_dict['user_name'],
                self.data['temp_user'][0]['user_name'])

        user_id = json_dict['user_id']
        token = json_dict['user_token']
        headers = Headers({'Authorization': 'Bearer ' + token})
        url = '/user/' + user_id

        # update (put, private user)
        data = {'user_status': 'private'}
        with app.test_client() as client:
            response = client.put(url, data=data, headers=headers)
            json_data = response.data
            json_dict = json.loads(json_data)
            self.assertEquals(json_dict['body']['user_status'], 'private')

        # get (private user)
        with app.test_client() as client:
            response = client.get(url)
            json_data = response.data
            json_dict = json.loads(json_data)
            self.assertEquals(json_dict['body']['user']['user_status'],
                              'private')

        # delete (deleted user)
        with app.test_client() as client:
            response = client.delete(url, headers=headers)
            json_data = response.data
            json_dict = json.loads(json_data)
            self.assertEqual(200, json_dict['code'], json_dict['message'])

        # get (delete user)
        with app.test_client() as client:
            response = client.get(url)
            json_data = response.data
            json_dict = json.loads(json_data)
            self.assertTrue('error_code' in json_dict)


'''
    def test_g_route_user_like(self):
        temp_user_id = self.data['const_user'][0]['_id']['$oid']

        with app.test_request_context(
                '/user/' + temp_user_id + '/like', data={}):
            response_json = UserUserIdLike().get(
                user_id=temp_user_id).get_json()

        service_result = service_user_get_like(temp_user_id)

        # same result length
        self.assertEqual(len(service_result), len(response_json["body"]))

        # same result value
        for i in range(len(service_result)):
            self.assertEqual(service_result[i]["user_id"],
                             response_json["body"][i]["user_id"])
            self.assertEqual(service_result[i]["video_id"],
                             response_json["body"][i]["video_id"])

        wrong_id = '12345678123456781234567'
        with app.test_request_context(
                '/user/' + wrong_id + '/process', data={}):
            code1 = UserUserIdLike().get(user_id=wrong_id).status_code
            code2 = util_error_handler(ServiceError(
                ErrorCode.SERVICE_INVALID_ID_OBJ)).status_code

            self.assertEqual(code1, code2)

    def test_h_route_user_dislike(self):
        temp_user_id = self.data['const_user'][0]['_id']['$oid']

        with app.test_request_context(
                '/user/' + temp_user_id + '/dislike', data={}):
            response_json = UserUserIdDislike().get(
                user_id=temp_user_id).get_json()

        service_result = service_user_get_dislike(temp_user_id)

        # same result length
        self.assertEqual(len(service_result), len(response_json["body"]))

        # same result value
        for i in range(len(service_result)):
            self.assertEqual(service_result[i]["user_id"],
                             response_json["body"][i]["user_id"])
            self.assertEqual(service_result[i]["video_id"],
                             response_json["body"][i]["video_id"])

        wrong_id = '12345678123456781234567'
        with app.test_request_context(
                '/user/' + wrong_id + '/process', data={}):
            code1 = UserUserIdDislike().get(user_id=wrong_id).status_code
            code2 = util_error_handler(ServiceError(
                ErrorCode.SERVICE_INVALID_ID_OBJ)).status_code
            self.assertEqual(code1, code2)

    def test_i_route_user_star(self):
        temp_user_id = self.data['const_user'][0]['_id']['$oid']

        with app.test_request_context(
                '/user/' + temp_user_id + '/star', data={}):
            response_json = UserUserIdStar().get(
                user_id=temp_user_id).get_json()

        service_result = service_user_get_star(temp_user_id)

        # same result length
        self.assertEqual(len(service_result), len(response_json["body"]))

        # same result value
        for i in range(len(service_result)):
            self.assertEqual(service_result[i]["user_id"],
                             response_json["body"][i]["user_id"])
            self.assertEqual(service_result[i]["video_id"],
                             response_json["body"][i]["video_id"])

        wrong_id = '12345678123456781234567'
        with app.test_request_context(
                '/user/' + wrong_id + '/process', data={}):
            code1 = UserUserIdStar().get(user_id=wrong_id).status_code
            code2 = util_error_handler(ServiceError(
                ErrorCode.SERVICE_INVALID_ID_OBJ)).status_code
            self.assertEqual(code1, code2)

    def test_j_route_user_comment(self):
        temp_user_id = self.data['const_user'][0]['_id']['$oid']

        with app.test_request_context(
                '/user/' + temp_user_id + '/comment', data={}):
            response_json = UserUserIdComment().get(
                user_id=temp_user_id).get_json()

        service_result = service_user_get_comment(temp_user_id)

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

        wrong_id = '12345678123456781234567'
        with app.test_request_context(
                '/user/' + wrong_id + '/process', data={}):
            code1 = UserUserIdComment().get(user_id=wrong_id).status_code
            code2 = util_error_handler(ServiceError(
                ErrorCode.SERVICE_INVALID_ID_OBJ)).status_code
            self.assertEqual(code1, code2)

    def test_k_route_user_process(self):
        temp_user_id = self.data['const_user'][0]['_id']['$oid']

        with app.test_request_context(
                '/user/' + temp_user_id + '/process', data={}):
            response_json = UserUserIdProcess().get(
                user_id=temp_user_id).get_json()

        service_result = service_user_get_process(temp_user_id)

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

        wrong_id = '12345678123456781234567'
        with app.test_request_context(
                '/user/' + wrong_id + '/process', data={}):
            code1 = UserUserIdProcess().get(user_id=wrong_id).status_code
            code2 = util_error_handler(ServiceError(
                ErrorCode.SERVICE_INVALID_ID_OBJ)).status_code
            self.assertEqual(code1, code2)
'''


class TestRouteVideo(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.data = util_tests_load_data()
        util_tests_clean_database()
        cls.test_user_id = cls.data['temp_video'][0]["user_id"]

        with app.app_context():
            expires = datetime.timedelta(hours=20)
            cls.client = app.test_client()
            cls.token = create_access_token(
                identity=cls.test_user_id, expires_delta=expires, fresh=True)
            cls.headers = Headers({'Authorization': 'Bearer ' + cls.token})

    def test_a_video_post(self):
        data = self.data['temp_video'][0]

        # post video
        with app.app_context():
            response = self.client.post('/video', headers=self.headers)
            response_vid = json.loads(response.data)["body"]["video_id"]

            self.assertEqual(len(response_vid), 24)

        query_video_update(
            response_vid,
            video_title=data['video_title'],
            video_raw_content=data['video_raw_content'])

    def test_b_video_get(self):
        temp_video_id = self.data['const_video'][0]["_id"]["$oid"]
        wrong_id_1 = "123123123"
        wrong_id_2 = "5f88f883e6ac4f89900ac984"

        # successful case
        with app.test_request_context('/video/' + temp_video_id, data={}):
            response_json = VideoVideoId().get(
                temp_video_id).get_json()
            self.assertEqual(response_json["body"]["user_id"],
                             self.data['const_video'][0]["user_id"])
            self.assertEqual(response_json["body"]["video_title"],
                             self.data['const_video'][0]["video_title"])

        # invalid Param
        with app.test_request_context('/video/' + wrong_id_1, data={}):
            error_json = VideoVideoId().get(temp_video_id).get_json()
            self.assertEqual(error_json["code"], 400)
            self.assertEqual(error_json["message"],
                             ErrorCode.SERVICE_INVALID_ID_OBJ.get_msg())

        # video not found
        with app.test_request_context('/video/' + wrong_id_2, data={}):
            error_json = VideoVideoId().get(temp_video_id).get_json()
            self.assertEqual(error_json["code"], 404)
            self.assertEqual(error_json["message"],
                             ErrorCode.SERVICE_VIDEO_NOT_FOUND.get_msg())

    def test_c_video_update(self):
        temp_video_title = self.data['temp_video'][0]['video_title']
        temp_video = query_video_get_by_title(temp_video_title)[0].to_dict()
        temp_video_id = temp_video["video_id"]

        wrong_id_1 = "123123123"
        wrong_id_2 = "5f88f883e6ac4f89900ac984"

        update_video = temp_video
        update_video["video_title"] = temp_video_title + " hh"

        wrong_status_data = copy.deepcopy(temp_video)
        wrong_status_data["video_status"] = "122345"

        # successful case
        with app.app_context():
            response = self.client.put('/video/' + temp_video_id,
                                       data=update_video,
                                       headers=self.headers)
            response_json = json.loads(response.data)

            self.assertEqual(response_json["body"][0]["user_id"],
                             update_video["user_id"])
            self.assertEqual(response_json["body"][0]["video_title"],
                             update_video["video_title"])

        # update back
        update_video["video_title"] = temp_video_title
        self.client.put('/video/' + temp_video_id,
                        data=update_video,
                        headers=self.headers)

        # invalid video_status
        with app.app_context():
            response = self.client.put('/video/' + temp_video_id,
                                       data=wrong_status_data,
                                       headers=self.headers)
            error_json = json.loads(response.data)

            self.assertEqual(error_json["code"], 400)
            self.assertEqual(error_json["message"],
                             ErrorCode.SERVICE_VIDEO_INVALID_STATUS.get_msg())

        # invalid Param
        with app.app_context():
            response = self.client.put('/video/' + wrong_id_1,
                                       data={},
                                       headers=self.headers)
            error_json = json.loads(response.data)

            self.assertEqual(error_json["code"], 503)

        # video not found
        with app.app_context():
            response = self.client.put('/video/' + wrong_id_2,
                                       data=update_video,
                                       headers=self.headers)
            error_json = json.loads(response.data)
            self.assertEqual(error_json["code"], 404)
            self.assertEqual(error_json["message"],
                             ErrorCode.SERVICE_VIDEO_NOT_FOUND.get_msg())

    def test_d_video_view(self):
        temp_video_title = self.data['temp_video'][0]['video_title']
        temp_video = query_video_get_by_title(temp_video_title)[0].to_dict()
        temp_video_id = temp_video["video_id"]

        wrong_id = "5f88f883e6ac4f89900ac984"

        # get view successful case
        with app.app_context():
            response = self.client.get('/video/' + temp_video_id + '/view',
                                       data={},
                                       headers=self.headers)
            response_json = json.loads(response.data)
            # self.assertEqual(response_json["message"], "")
            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["view_count"], 0)

        # get view error case
        with app.app_context():
            response = self.client.get('/video/' + wrong_id + '/view',
                                       data={},
                                       headers=self.headers)
            error_json = json.loads(response.data)
            self.assertEqual(error_json["code"], 404)

        # add view successful case
        with app.app_context():
            response = self.client.put('/video/' + temp_video_id + '/view',
                                       data={},
                                       headers=self.headers)
            response_json = json.loads(response.data)
            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["view_count"], 1)

        # add view error case
        with app.app_context():
            response = self.client.put('/video/' + wrong_id + '/view',
                                       data={},
                                       headers=self.headers)
            error_json = json.loads(response.data)
            self.assertEqual(error_json["code"], 404)

    def test_e_video_comment(self):
        temp_video_title = self.data['temp_video'][0]['video_title']
        temp_video = query_video_get_by_title(temp_video_title)[0].to_dict()
        temp_video_id = temp_video["video_id"]
        temp_user_id = temp_video["user_id"]
        temp_comment = "nice video"
        temp_comment_updated = "really nice video"

        wrong_id = "5f88f883e6ac4f89900ac984"

        # post comment successful case
        with app.app_context():
            response = self.client.post(
                '/video/' + temp_video_id + '/comment/' + temp_user_id,
                data={"comment": temp_comment},
                headers=self.headers)
            response_json = json.loads(response.data)
            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["comment"], temp_comment)

        # post comment error case
        with app.app_context():
            response = self.client.post(
                '/video/' + temp_video_id + '/comment/' + wrong_id,
                data={"comment": temp_comment},
                headers=self.headers)
            error_json = json.loads(response.data)
            self.assertEqual(error_json["code"], 404)

        # get comment successful case
        with app.app_context():
            response = self.client.get(
                '/video/' + temp_video_id + '/comment/' + temp_user_id,
                data={},
                headers=self.headers)
            response_json = json.loads(response.data)
            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["comment"], temp_comment)

        # get comment error case
        with app.app_context():
            response = self.client.get(
                '/video/' + temp_video_id + '/comment/' + wrong_id,
                data={},
                headers=self.headers)
            error_json = json.loads(response.data)
            self.assertEqual(error_json["code"], 404)

        # update comment successful case
        with app.app_context():
            response = self.client.put(
                '/video/' + temp_video_id + '/comment/' + temp_user_id,
                data={"comment": temp_comment_updated},
                headers=self.headers)
            response_json = json.loads(response.data)

            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["comment"],
                             temp_comment_updated)

        # update comment error case
        with app.app_context():
            response = self.client.put(
                '/video/' + temp_video_id + '/comment/' + wrong_id,
                data={"comment": temp_comment_updated},
                headers=self.headers)
            error_json = json.loads(response.data)
            self.assertEqual(error_json["code"], 404)

        # get all comments of the video successful case
        with app.app_context():
            response = self.client.get(
                '/video/' + temp_video_id + '/comment',
                data={},
                headers=self.headers)
            response_json = json.loads(response.data)

            self.assertEqual(response_json["body"][0]["video_id"],
                             temp_video_id)
            self.assertEqual(response_json["body"][0]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"][0]["comment"],
                             temp_comment_updated)

        # get all comments of the video error case
        with app.app_context():
            response = self.client.get(
                '/video/' + wrong_id + '/comment',
                data={},
                headers=self.headers)
            error_json = json.loads(response.data)

            self.assertEqual(error_json["code"], 404)

        # delete comment successful case
        with app.app_context():
            response = self.client.delete(
                '/video/' + temp_video_id + '/comment/' + temp_user_id,
                data={},
                headers=self.headers)
            response_json = json.loads(response.data)
            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["comment"], "")

        # delete comment error case
        with app.app_context():
            response = self.client.delete(
                '/video/' + temp_video_id + '/comment/' + wrong_id,
                data={},
                headers=self.headers)
            error_json = json.loads(response.data)
            self.assertEqual(error_json["code"], 404)

    def test_f_video_process(self):
        temp_video_title = self.data['temp_video'][0]['video_title']
        temp_video = query_video_get_by_title(temp_video_title)[0].to_dict()
        temp_video_id = temp_video["video_id"]
        temp_user_id = temp_video["user_id"]
        temp_process = 30
        temp_process_updated = 60

        wrong_id = "5f88f883e6ac4f89900ac984"

        # post process successful case
        with app.app_context():
            response = self.client.post(
                '/video/' + temp_video_id + '/process/' + temp_user_id,
                data={"process": temp_process},
                headers=self.headers)
            response_json = json.loads(response.data)

            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["process"], temp_process)

        # post process error case
        with app.app_context():
            response = self.client.post(
                '/video/' + temp_video_id + '/process/' + wrong_id,
                data={"process": temp_process},
                headers=self.headers)
            error_json = json.loads(response.data)

            self.assertEqual(error_json["code"], 404)

        # post process error case
        with app.app_context():
            response = self.client.post(
                '/video/' + temp_video_id + '/process/' + temp_user_id,
                data={"process": -1},
                headers=self.headers)
            error_json = json.loads(response.data)
            self.assertEqual(error_json["code"], 500)

        # get process successful case
        with app.app_context():
            response = self.client.get(
                '/video/' + temp_video_id + '/process/' + temp_user_id,
                data={},
                headers=self.headers)
            response_json = json.loads(response.data)

            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["process"], temp_process)

        # get process error case
        with app.app_context():
            response = self.client.get(
                '/video/' + temp_video_id + '/process/' + wrong_id,
                data={},
                headers=self.headers)
            error_json = json.loads(response.data)
            self.assertEqual(error_json["code"], 404)

        # update process successful case
        with app.app_context():
            response = self.client.put(
                '/video/' + temp_video_id + '/process/' + temp_user_id,
                data={"process": temp_process_updated},
                headers=self.headers)
            response_json = json.loads(response.data)

            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["process"],
                             temp_process_updated)

        # update process error case
        with app.app_context():
            response = self.client.put(
                '/video/' + temp_video_id + '/process/' + wrong_id,
                data={"process": temp_process_updated},
                headers=self.headers)
            error_json = json.loads(response.data)
            self.assertEqual(error_json["code"], 404)

        # update process error case
        with app.app_context():
            response = self.client.put(
                '/video/' + temp_video_id + '/process/' + temp_user_id,
                data={"process": -100},
                headers=self.headers)
            error_json = json.loads(response.data)
            self.assertEqual(error_json["code"], 400)

        # delete process successful case
        with app.app_context():
            response = self.client.delete(
                '/video/' + temp_video_id + '/process/' + temp_user_id,
                data={},
                headers=self.headers)
            response_json = json.loads(response.data)
            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["process"], 0)

        # delete process error case
        with app.app_context():
            response = self.client.delete(
                '/video/' + temp_video_id + '/process/' + temp_user_id,
                data={},
                headers=self.headers)
            error_json = json.loads(response.data)
            self.assertEqual(error_json["code"], 500)

    def test_g_video_like(self):
        temp_video_title = self.data['temp_video'][0]['video_title']
        temp_video = query_video_get_by_title(temp_video_title)[0].to_dict()
        temp_video_id = temp_video["video_id"]
        temp_user_id = temp_video["user_id"]
        wrong_id = "5f88f883e6ac4f89900ac984"

        # post like successful case
        with app.app_context():
            response = self.client.post(
                '/video/' + temp_video_id + '/like/' + temp_user_id,
                data={},
                headers=self.headers)
            response_json = json.loads(response.data)
            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["like"], True)

        # post like error case
        with app.app_context():
            response = self.client.post(
                '/video/' + temp_video_id + '/like/' + temp_user_id,
                data={},
                headers=self.headers)
            error_json = json.loads(response.data)

            self.assertEqual(error_json["code"], 500)

        # get all likes of the video successful case
        with app.app_context():
            response = self.client.get(
                '/video/' + temp_video_id + '/like',
                data={},
                headers=self.headers)
            response_json = json.loads(response.data)
            self.assertEqual(response_json["body"][0]["video_id"],
                             temp_video_id)
            self.assertEqual(response_json["body"][0]["user_id"], temp_user_id)

        # get all likes of the video error case
        with app.app_context():
            response = self.client.get(
                '/video/' + wrong_id + '/like',
                data={},
                headers=self.headers)
            error_json = json.loads(response.data)
            self.assertEqual(error_json["code"], 404)

        # cancel like successful case
        with app.app_context():
            response = self.client.delete(
                '/video/' + temp_video_id + '/like/' + temp_user_id,
                data={},
                headers=self.headers)
            response_json = json.loads(response.data)

            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["like"], False)

        # cancel like error case
        with app.app_context():
            response = self.client.delete(
                '/video/' + temp_video_id + '/like/' + temp_user_id,
                data={},
                headers=self.headers)
            error_json = json.loads(response.data)

            self.assertEqual(error_json["code"], 500)

    def test_h_video_dislike(self):
        temp_video_title = self.data['temp_video'][0]['video_title']
        temp_video = query_video_get_by_title(temp_video_title)[0].to_dict()
        temp_video_id = temp_video["video_id"]
        temp_user_id = temp_video["user_id"]
        wrong_id = "5f88f883e6ac4f89900ac984"

        # post dislike successful case
        with app.app_context():
            response = self.client.post(
                '/video/' + temp_video_id + '/dislike/' + temp_user_id,
                data={},
                headers=self.headers)
            response_json = json.loads(response.data)

            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["dislike"], True)

        # post dislike error case
        with app.app_context():
            response = self.client.post(
                '/video/' + temp_video_id + '/dislike/' + wrong_id,
                data={},
                headers=self.headers)
            error_json = json.loads(response.data)

            self.assertEqual(error_json["code"], 404)

        # get all dislikes of the video successful case
        with app.app_context():
            response = self.client.get(
                '/video/' + temp_video_id + '/dislike',
                data={},
                headers=self.headers)
            response_json = json.loads(response.data)

            self.assertEqual(response_json["body"][0]["video_id"],
                             temp_video_id)
            self.assertEqual(response_json["body"][0]["user_id"], temp_user_id)

        # get all dislikes of the video error case
        with app.app_context():
            response = self.client.get(
                '/video/' + wrong_id + '/dislike',
                data={},
                headers=self.headers)
            error_json = json.loads(response.data)

            self.assertEqual(error_json["code"], 404)

        # cancel dislike successful case
        with app.app_context():
            response = self.client.delete(
                '/video/' + temp_video_id + '/dislike/' + temp_user_id,
                data={},
                headers=self.headers)
            response_json = json.loads(response.data)

            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["dislike"], False)

        # cancel dislike error case
        with app.app_context():
            response = self.client.delete(
                '/video/' + temp_video_id + '/dislike/' + wrong_id,
                data={},
                headers=self.headers)
            error_json = json.loads(response.data)

            self.assertEqual(error_json["code"], 404)

    def test_i_video_star(self):
        temp_video_title = self.data['temp_video'][0]['video_title']
        temp_video = query_video_get_by_title(temp_video_title)[0].to_dict()
        temp_video_id = temp_video["video_id"]
        temp_user_id = temp_video["user_id"]
        wrong_id = "5f88f883e6ac4f89900ac984"

        # post star successful case
        with app.app_context():
            response = self.client.post(
                '/video/' + temp_video_id + '/star/' + temp_user_id,
                data={},
                headers=self.headers)
            response_json = json.loads(response.data)

            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["star"], True)

        # post star error case
        with app.app_context():
            response = self.client.post(
                '/video/' + temp_video_id + '/star/' + wrong_id,
                data={},
                headers=self.headers)
            error_json = json.loads(response.data)
            self.assertEqual(error_json["code"], 404)

        # get all stars of the video successful case
        with app.app_context():
            response = self.client.get(
                '/video/' + temp_video_id + '/star',
                data={},
                headers=self.headers)
            response_json = json.loads(response.data)

            self.assertEqual(response_json["body"][0]["video_id"],
                             temp_video_id)
            self.assertEqual(response_json["body"][0]["user_id"], temp_user_id)

        # get all stars of the video error case
        with app.app_context():
            response = self.client.get(
                '/video/' + wrong_id + '/star',
                data={},
                headers=self.headers)
            error_json = json.loads(response.data)
            self.assertEqual(error_json["code"], 404)

        # cancel star successful case
        with app.app_context():
            response = self.client.delete(
                '/video/' + temp_video_id + '/star/' + temp_user_id,
                data={},
                headers=self.headers)
            response_json = json.loads(response.data)
            self.assertEqual(response_json["body"]["video_id"], temp_video_id)
            self.assertEqual(response_json["body"]["user_id"], temp_user_id)
            self.assertEqual(response_json["body"]["star"], False)

        # cancel star error case
        with app.app_context():
            response = self.client.delete(
                '/video/' + temp_video_id + '/star/' + wrong_id,
                data={},
                headers=self.headers)
            error_json = json.loads(response.data)

            self.assertEqual(error_json["code"], 404)

    def test_z_video_delete(self):
        temp_video_title = self.data['temp_video'][0]['video_title']
        temp_video = query_video_get_by_title(temp_video_title)[0].to_dict()
        temp_video_id = temp_video["video_id"]

        # successful case
        with app.app_context():
            self.client.delete('/video/' + temp_video_id,
                               data={},
                               headers=self.headers)
            delete_search = query_video_get_by_video_id(temp_video_id)
            self.assertEqual(len(delete_search), 1)

        query_video_delete(temp_video_id, silent=True)

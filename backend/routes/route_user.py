# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import ast
import datetime

from flask import request, jsonify

from flask_jwt_extended import create_access_token, \
    jwt_required, get_raw_jwt, get_jwt_identity, jwt_optional
from flask_restx import Resource, fields, Namespace

from service.service_user import service_user_get_comment, \
    service_user_get_dislike, service_user_get_info, service_user_get_like, \
    service_user_get_process, service_user_get_star, service_user_check_password, service_user_reg
from service.service_video import service_video_upload
from utils.util_jwt import blacklist, util_get_formated_response
from utils.util_error_handler import util_error_handler
from settings import config
from utils.util_serializer import util_serializer_api_response, util_serializer_mongo_results_to_array
from models.model_errors import MongoError, RouteError, ServiceError

# from source.utils.util_validator import *
# from flask import Flask, g, Blueprint
# from flask_restx import Api, marshal_with, reqparse
# import json

user = Namespace('user', description='User APIs')

address_detail = user.model(name='AddressDetail', model={
    'street1': fields.String,
    'street2': fields.String,
    'city': fields.String,
    'state': fields.String,
    'country': fields.String,
    'zip': fields.String
})

user_detail = user.model(name='UserDetail', model={
    'first_name': fields.String,
    'last_name': fields.String,
    'phone': fields.String,
    'address': fields.Nested(address_detail)
})

thumbnail = user.model(name='Thumbnail', model={
    'thumbnail_uri': fields.String,
    'thumbnail_type': fields.String
})

user_info = user.model(name='User', model={
    'user_id': fields.String,
    'user_name': fields.String,
    'user_email': fields.String,
    'user_password': fields.String,
    'user_detail': fields.Nested(user_detail),
    'user_status': fields.String,
    'user_thumbnail': fields.Nested(thumbnail),
    'user_follower': fields.Integer,
    'user_reg_date': fields.DateTime,
    'user_recent_login': fields.List(fields.String)
})

like = user.model(name='Like', model={
    'like_id': fields.String,
    'user_id': fields.String,
    'video_id': fields.String,
    'like_date': fields.String
})

dislike = user.model(name='Dislike', model={
    'dislike_id': fields.String,
    'user_id': fields.String,
    'video_id': fields.String,
    'dislike_date': fields.String
})

comment = user.model(name='Comment', model={
    'comment_id': fields.String,
    'user_id': fields.String,
    'video_id': fields.String,
    'comment_date': fields.String,
    'comment': fields.String
})

star = user.model(name='Star', model={
    'star_id': fields.String,
    'user_id': fields.String,
    'video_id': fields.String,
    'star_date': fields.String
})

process = user.model(name='Process', model={
    'process_id': fields.String,
    'user_id': fields.String,
    'video_id': fields.String,
    'process_date': fields.String,
    'process': fields.String,
})

general_response = user.model(name='ApiResponse', model={
    'code': fields.String,
    'body': fields.String
})

user_response = user.model(name='ApiResponseWithUser', model={
    'code': fields.String,
    'body': fields.Nested(user_info)
})

general_response_list = user.model(name='ApiResponseWithList', model={
    'code': fields.String,
    'body': fields.List(fields.String)
})

like_response_list = user.model(name='ApiResponseWithLikeList', model={
    'code': fields.String,
    'body': fields.List(fields.Nested(like))
})

dislike_response_list = user.model(name='ApiResponseWithDislikeList', model={
    'code': fields.String,
    'body': fields.List(fields.Nested(dislike))
})

star_response_list = user.model(name='ApiResponseWithStarList', model={
    'code': fields.String,
    'body': fields.List(fields.Nested(star))
})

comment_response_list = user.model(name='ApiResponseWithCommentList', model={
    'code': fields.String,
    'body': fields.List(fields.Nested(comment))
})

process_response_list = user.model(name='ApiResponseWithProcessList', model={
    'code': fields.String,
    'body': fields.List(fields.Nested(process))
})


@user.route('', methods=['POST'])
@user.response(200, 'Successful operation', user_response)
@user.response(400, 'Invalid user information', general_response)
@user.response(405, 'Method not allowed', general_response)
@user.response(500, 'Internal server error', general_response)
class User(Resource):
    @jwt_optional
    def post(self):
        """
            User sign up
        """

        # print("sign up1", get_jwt_identity())
        # print("sign up", get_raw_jwt(), blacklist)
        try:
            kw = ""
            if request.form != {}:
                kw = dict(request.form)
                print(kw)
            else:
                raw_data = request.data.decode("utf-8")
                kw = ast.literal_eval(raw_data)
                print(kw)

            user = service_user_reg(conf = config["default"], **kw)
            return user
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)


@user.route('/<string:user_id>', methods=['DELETE', 'GET', 'PUT'])
@user.param('user_id', 'User ID')
@user.response(200, 'Successful operation', user_response)
@user.response(400, 'Invalid user information', general_response)
@user.response(404, 'User not found', general_response)
@user.response(500, 'Internal server error', general_response)
class UserUserId(Resource):
    # TODO: implemented the test case
    # @jwt_required
    def get(self, user_id, conf=config["default"]):
        """
            Get user information by id
        """

        try:
            user_id = request.url.split('/')[-1]

            result = service_user_get_info(conf=conf, user_id=user_id)
            return util_serializer_api_response(200, body=result,
                                                msg="Get user info "
                                                    "successfully")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)

    @user.response(405, 'Method not allowed')
    def put(self, user_id):
        """
            Update user information by id
        """
        pass
        # return {}, 200, None

    @user.response(405, 'Method not allowed')
    def delete(self, user_id):
        """
            Delete user by id
        """
        pass
        # return {}, 200, None


@user.route('/login', methods=['POST'])
@user.response(200, 'Successful operation', user_response)
@user.response(400, 'Invalid user information', general_response)
@user.response(500, 'Internal server error', general_response)
class UserLogin(Resource):
    def post(self, conf=config["default"]):
        """
            User sign in
        """

        try:
            if request.form != {}:
                kw = dict(request.form)
            else:
                raw_data = request.data.decode("utf-8")
                kw = ast.literal_eval(raw_data)

            is_valid = service_user_check_password(conf=conf, **kw)
            print(kw['user_name'], kw['user_password'])
            if is_valid:
                expires = datetime.timedelta(seconds=20)
                # expires = datetime.timedelta(hours=20)
                token = create_access_token(identity=kw['user_name']
                                            , expires_delta=expires, fresh=True)
                return jsonify({
                    "code": 200,
                    "message": "login succeeded",
                    "token": token
                })
            else:
                return util_serializer_api_response(
                    500, msg="invalid password")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)


@user.route('/logout', methods=['POST'])
@user.response(200, 'Successful operation', user_response)
@user.response(400, 'Bad request', general_response)
@user.response(500, 'Internal server error', general_response)
class UserLogout(Resource):
    @jwt_required
    def post(self):
        """
            User log out
        """
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return util_get_formated_response(code=200,
                                          msg='logout succeeded')


@user.route('/<string:user_id>/like', methods=['GET'])
@user.param('user_id', 'User ID')
@user.response(200, 'Successful operation', like_response_list)
@user.response(400, 'Invalid user id', general_response)
@user.response(404, 'User not found', general_response)
@user.response(500, 'Internal server error', general_response)
class UserUserIdLike(Resource):

    def get(self, user_id, conf=config["default"]):
        """
            Get a list of like by user id
        """

        try:
            user_id = request.url.split('/')[-2]

            like_result = service_user_get_like(conf=conf, user_id=user_id)
            return util_serializer_api_response(200, body=like_result,
                                                msg="Get user likes "
                                                    "successfully")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)


@user.route('/<string:user_id>/dislike', methods=['GET'])
@user.param('user_id', 'User ID')
@user.response(200, 'Successful operation', dislike_response_list)
@user.response(400, 'Invalid user id', general_response)
@user.response(404, 'User not found', general_response)
@user.response(500, 'Internal server error', general_response)
class UserUserIdDislike(Resource):

    def get(self, user_id, conf=config["default"]):
        """
            Get a list of dislike by user id
        """

        try:
            user_id = request.url.split('/')[-2]

            dislike_result = service_user_get_dislike(conf=conf,
                                                      user_id=user_id)
            return util_serializer_api_response(200, body=dislike_result,
                                                msg="Get user dislikes "
                                                    "successfully")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)


@user.route('/<string:user_id>/star', methods=['GET'])
@user.param('user_id', 'User ID')
@user.response(200, 'Successful operation', star_response_list)
@user.response(400, 'Invalid user id', general_response)
@user.response(404, 'User not found', general_response)
@user.response(500, 'Internal server error', general_response)
class UserUserIdStar(Resource):

    def get(self, user_id, conf=config["default"]):
        """
            Get a list of star by user id
        """

        try:
            user_id = request.url.split('/')[-2]

            star_result = service_user_get_star(conf=conf, user_id=user_id)
            return util_serializer_api_response(200, body=star_result,
                                                msg="Get user comments "
                                                    "successfully")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)


@user.route('/<string:user_id>/comment', methods=['GET'])
@user.param('user_id', 'User ID')
@user.response(200, 'Successful operation', comment_response_list)
@user.response(400, 'Invalid user id', general_response)
@user.response(404, 'User not found', general_response)
@user.response(500, 'Internal server error', general_response)
class UserUserIdComment(Resource):

    def get(self, user_id, conf=config["default"]):
        """
            Get a list of comments by user id
        """

        try:
            user_id = request.url.split('/')[-2]

            comment_result = service_user_get_comment(conf=conf,
                                                      user_id=user_id)
            return util_serializer_api_response(200, body=comment_result,
                                                msg="Get user comments "
                                                    "successfully")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)


@user.route('/<string:user_id>/process', methods=['GET'])
@user.param('user_id', 'User ID')
@user.response(200, 'Successful operation', process_response_list)
@user.response(400, 'Invalid user id', general_response)
@user.response(404, 'User not found', general_response)
@user.response(500, 'Internal server error', general_response)
class UserUserIdProcess(Resource):

    def get(self, user_id, conf=config["default"]):
        """
            Get a list of comments by user id
        """

        try:
            user_id = request.url.split('/')[-2]

            process_result = service_user_get_process(conf=conf,
                                                      user_id=user_id)
            return util_serializer_api_response(200, body=process_result,
                                                msg="Get user processes "
                                                    "successfully")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)

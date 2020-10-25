# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import Flask, request, g, Blueprint
from flask_restx import Resource, Api, fields, marshal_with, reqparse, Namespace

from source.service.service_user import *
from source.utils.util_serializer import *
from source.utils.util_validator import *
from source.utils.util_error_handler import *
from source.settings import *

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

    def post(self):
        """
            User sign up
        """
        return {}, 200, None


@user.route('/<string:user_id>', methods=['DELETE', 'GET', 'PUT'])
@user.param('user_id', 'User ID')
@user.response(200, 'Successful operation', user_response)
@user.response(400, 'Invalid user information', general_response)
@user.response(404, 'User not found', general_response)
@user.response(500, 'Internal server error', general_response)
class UserUserId(Resource):

    def get(self, user_id):
        """
            Get user information by id
        """
        user_id = request.url.split('/')[-1]

        try:
            result = service_user_get_info(conf=config['default'], user_id=user_id)
            return util_serializer_api_response(200, body=result, msg="Successfully get user information")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)

    @user.response(405, 'Method not allowed')
    def put(self, user_id):
        """
            Update user information by id
        """
        return {}, 200, None

    @user.response(405, 'Method not allowed')
    def delete(self, user_id):
        """
            Delete user by id
        """
        return {}, 200, None


@user.route('/login', methods=['POST'])
@user.response(200, 'Successful operation', user_response)
@user.response(400, 'Invalid user information', general_response)
@user.response(500, 'Internal server error', general_response)
class UserLogin(Resource):
    def post(self):
        """
            User sign in
        """
        return None, 200


@user.route('/logout', methods=['POST'])
@user.response(200, 'Successful operation', user_response)
@user.response(400, 'Bad request', general_response)
@user.response(500, 'Internal server error', general_response)
class UserLogout(Resource):

    def post(self):
        """
            User log out
        """
        return None, 200


@user.route('/<string:user_id>/like', methods=['GET'])
@user.param('user_id', 'User ID')
@user.response(200, 'Successful operation', like_response_list)
@user.response(400, 'Invalid user id', general_response)
@user.response(404, 'User not found', general_response)
@user.response(500, 'Internal server error', )
class UserUserIdLike(Resource):

    def get(self, user_id):
        """
            Get a list of like by user id
        """
        user_id = request.url.split('/')[-2]

        try:
            like_result = service_user_get_like(conf=config['default'], user_id=user_id)
            return util_serializer_api_response(200, body=like_result, msg="Successfully get user likes")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)


@user.route('/<string:user_id>/dislike', methods=['GET'])
@user.param('user_id', 'User ID')
@user.response(200, 'Successful operation', dislike_response_list)
@user.response(400, 'Invalid user id', general_response)
@user.response(404, 'User not found', general_response)
@user.response(500, 'Internal server error', general_response)
class UserUserIdDislike(Resource):

    def get(self, user_id):
        """
            Get a list of dislike by user id
        """
        user_id = request.url.split('/')[-2]

        try:
            dislike_result = service_user_get_dislike(conf=config['default'], user_id=user_id)
            return util_serializer_api_response(200, body=dislike_result, msg="Successfully get user dislikes")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)


@user.route('/<string:user_id>/star', methods=['GET'])
@user.param('user_id', 'User ID')
@user.response(200, 'Successful operation', star_response_list)
@user.response(400, 'Invalid user id', general_response)
@user.response(404, 'User not found', general_response)
@user.response(500, 'Internal server error', general_response)
class UserUserIdStar(Resource):

    def get(self, user_id):
        """
            Get a list of star by user id
        """
        user_id = request.url.split('/')[-2]

        try:
            star_result = service_user_get_star(conf=config['default'], user_id=user_id)
            return util_serializer_api_response(200, body=star_result, msg="Successfully get user comments")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)

        return service_user_get_star(conf=config['default'], user_id=user_id)


@user.route('/<string:user_id>/comment', methods=['GET'])
@user.param('user_id', 'User ID')
@user.response(200, 'Successful operation', comment_response_list)
@user.response(400, 'Invalid user id', general_response)
@user.response(404, 'User not found', general_response)
@user.response(500, 'Internal server error', general_response)
class UserUserIdComment(Resource):

    def get(self, user_id):
        """
            Get a list of comments by user id
        """
        user_id = request.url.split('/')[-2]

        try:
            comment_result = service_user_get_comment(conf=config['default'], user_id=user_id)
            return util_serializer_api_response(200, body=comment_result, msg="Successfully get user comments")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)


@user.route('/<string:user_id>/process', methods=['GET'])
@user.param('user_id', 'User ID')
@user.response(200, 'Successful operation', process_response_list)
@user.response(400, 'Invalid user id', general_response)
@user.response(404, 'User not found', general_response)
@user.response(500, 'Internal server error', general_response)
class UserUserIdProcess(Resource):

    def get(self, user_id):
        """
            Get a list of comments by user id
        """
        user_id = request.url.split('/')[-2]

        try:
            process_result = service_user_get_comment(conf=config['default'], user_id=user_id)
            return util_serializer_api_response(200, body=process_result, msg="Successfully get user processes")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)

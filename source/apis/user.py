# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import Flask, request, g, Blueprint
from flask_restx import Resource, Api, fields, marshal_with, reqparse, Namespace
import json

user = Namespace('user', description='User APIs')

address_detail = user.model(name='AddressDetail', model={
    'street1': fields.String(required=True),
    'street2': fields.String(required=False),
    'city': fields.String(required=True),
    'state': fields.String(required=True),
    'country': fields.String(required=True),
    'zip': fields.String(required=True)
})

user_detail = user.model(name='UserDetail', model={
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'phone': fields.String(required=True),
    'address': fields.Nested(address_detail, required=False)
})

thumbnail = user.model(name='Thumbnail', model={
    'thumbnail_uri': fields.String(required=True),
    'thumbnail_type': fields.String(required=True)
})

user_info = user.model(name='User', model={
    'user_id': fields.String(required=True),
    'user_name': fields.String(required=True),
    'user_password': fields.String(required=True),
    'user_detail': fields.Nested(user_detail, required=False),
    'user_status': fields.String(required=False),
    'user_thumbnail': fields.Nested(thumbnail, required=False),
    'user_follower': fields.Integer(required=False),
    'user_reg_date': fields.DateTime(required=False),
    'user_recent_login': fields.List(fields.String(required=False))
})

general_response = user.model(name='ApiResponse', model={
    'code': fields.String(required=True),
    'body': fields.String(required=True)
})

general_response_user = user.model(name='ApiResponseWithUser', model={
    'code': fields.String(required=True),
    'body': fields.Nested(user_info, required=True)
})

general_response_list = user.model(name='ApiResponseWithList', model={
    'code': fields.String(required=True),
    'body': fields.List(fields.String(required=True))
})

@user.route('')
@user.response(200, 'Successful operation', general_response_user)
@user.response(400, 'Invalid user information', general_response)
@user.response(405, 'Method not allowed', general_response)
@user.response(500, 'Internal server error', general_response)
class User(Resource):

    def post(self):
        """
            User sign up
        """
        return {}, 200, None

@user.route('/<string:user_id>')
@user.param('user_id', 'User ID', general_response_user)
@user.response(200, 'Successful operation', general_response)
@user.response(400, 'Invalid user information', general_response)
@user.response(404, 'User not found', general_response)
@user.response(500, 'Internal server error', general_response)
class UserUserId(Resource):

    def get(self, user_id):
        """
            Get user information by id
        """
        return {}, 200, None


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


@user.route('/login')
@user.response(200, 'Successful operation', general_response_user)
@user.response(400, 'Invalid user information', general_response)
@user.response(500, 'Internal server error', general_response)
class UserLogin(Resource):
    def post(self):
        """
            User sign in
        """
        return None, 200


@user.route('/logout')
@user.response(200, 'Successful operation', general_response_user)
@user.response(400, 'Bad request', general_response)
@user.response(500, 'Internal server error', general_response)
class UserLogout(Resource):

    def post(self):
        """
            User log out
        """
        return None, 200

@user.route('/<string:user_id>/like')
@user.param('user_id', 'User ID')
@user.response(200, 'Successful operation', general_response_list)
@user.response(400, 'Invalid user id', general_response)
@user.response(404, 'User not found', general_response)
@user.response(500, 'Internal server error', )
class UserUserIdLike(Resource):

    def get(self, user_id):
        """
            Get a list of like by user id
        """
        return {}, 200, None

@user.route('/<string:user_id>/dislike')
@user.param('user_id', 'User ID')
@user.response(200, 'Successful operation', general_response_list)
@user.response(400, 'Invalid user id', general_response)
@user.response(404, 'User not found', general_response)
@user.response(500, 'Internal server error', general_response)
class UserUserIdDislike(Resource):

    def get(self, user_id):
        """
            Get a list of dislike by user id
        """
        return {}, 200, None

@user.route('/<string:user_id>/star')
@user.param('user_id', 'User ID')
@user.response(200, 'Successful operation', general_response_list)
@user.response(400, 'Invalid user id', general_response)
@user.response(404, 'User not found', general_response)
@user.response(500, 'Internal server error', general_response)
class UserUserIdStar(Resource):

    def get(self, user_id):
        """
            Get a list of star by user id
        """
        return {}, 200, None

@user.route('/<string:user_id>/comment')
@user.param('user_id', 'User ID')
@user.response(200, 'Successful operation', general_response_list)
@user.response(400, 'Invalid user id', general_response)
@user.response(404, 'User not found', general_response)
@user.response(500, 'Internal server error', general_response)
class UserUserIdComment(Resource):

    def get(self, user_id):
        """
            Get a list of comments by user id
        """
        return {}, 200, None
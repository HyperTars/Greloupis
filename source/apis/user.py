# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import Flask, request, g, Blueprint
from flask_restx import Resource, Api, fields, marshal_with, reqparse, Namespace
import json

user = Namespace('user', description='User APIs')

@user.route('')
@user.response(200, 'Successful operation')
@user.response(400, 'Invalid user information')
@user.response(405, 'Method not allowed')
@user.response(500, 'Internal server error')
class User(Resource):

    def post(self):
        """
            User sign up
        """
        return {}, 200, None

@user.route('/<string:user_id>')
@user.response(200, 'Successful operation')
@user.response(400, 'Invalid user information')
@user.response(404, 'User not found')
@user.response(500, 'Internal server error')
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
@user.response(200, 'Successful operation')
@user.response(400, 'Invalid user information')
@user.response(500, 'Internal server error')
class UserLogin(Resource):
    def post(self):
        """
            User sign in
        """
        return None, 200


@user.route('/logout')
@user.response(200, 'Successful operation')
@user.response(400, 'Bad request')
@user.response(500, 'Internal server error')
class UserLogout(Resource):

    def post(self):
        """
            User log out
        """
        return None, 200

@user.route('/<string:user_id>/like')
@user.response(200, 'Successful operation')
@user.response(400, 'Invalid user id')
@user.response(404, 'User not found')
@user.response(500, 'Internal server error')
class UserUserIdLike(Resource):

    def get(self, user_id):
        """
            Get a list of like by user id
        """
        return {}, 200, None

@user.route('/<string:user_id>/dislike')
@user.response(200, 'Successful operation')
@user.response(400, 'Invalid user id')
@user.response(404, 'User not found')
@user.response(500, 'Internal server error')
class UserUserIdDislike(Resource):

    def get(self, user_id):
        """
            Get a list of dislike by user id
        """
        return {}, 200, None

@user.route('/<string:user_id>/star')
@user.response(200, 'Successful operation')
@user.response(400, 'Invalid user id')
@user.response(404, 'User not found')
@user.response(500, 'Internal server error')
class UserUserIdStar(Resource):

    def get(self, user_id):
        """
            Get a list of star by user id
        """
        return {}, 200, None

@user.route('/<string:user_id>/comment')
@user.response(200, 'Successful operation')
@user.response(400, 'Invalid user id')
@user.response(404, 'User not found')
@user.response(500, 'Internal server error')
class UserUserIdComment(Resource):

    def get(self, user_id):
        """
            Get a list of comments by user id
        """
        return {}, 200, None
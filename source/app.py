# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import Flask, request, g
from flask_restx import Resource, Api, fields, marshal_with, reqparse, Namespace
import json

app = Flask(__name__)
api = Api(app)

@api.route('/user')
@api.response(200, 'Successful operation')
@api.response(400, 'Invalid user information')
@api.response(405, 'Method not allowed')
@api.response(500, 'Internal server error')
class User(Resource):
    """
        User sign up
    """
    def post(self):
        return {}, 200, None

@api.route('/user/<string:user_id>')
@api.response(200, 'Successful operation')
@api.response(400, 'Invalid user information')
@api.response(404, 'User not found')
@api.response(500, 'Internal server error')
class UserUserId(Resource):
    """
        Get user information by id
    """
    def get(self, user_id):
        return {}, 200, None

    """
        Update user information by id
    """
    @api.response(405, 'Method not allowed')
    def put(self, user_id):
        return {}, 200, None

    """
        Delete user by id
    """
    @api.response(405, 'Method not allowed')
    def delete(self, user_id):
        return {}, 200, None


@api.route('/user/login')
@api.response(200, 'Successful operation')
@api.response(400, 'Invalid user information')
@api.response(500, 'Internal server error')
class UserLogin(Resource):
    def post(self):
        """
            User sign in
        """
        return None, 200


@api.route('/user/logout')
@api.response(200, 'Successful operation')
@api.response(400, 'Bad request')
@api.response(500, 'Internal server error')
class UserLogout(Resource):

    def post(self):
        """
            User log out
        """
        return None, 200

@api.route('/user/<string:user_id>/like')
@api.response(200, 'Successful operation')
@api.response(400, 'Invalid user id')
@api.response(404, 'User not found')
@api.response(500, 'Internal server error')
class UserUserIdLike(Resource):

    """
        Get a list of like by user id
    """
    def get(self, user_id):
        return {}, 200, None

@api.route('/user/<string:user_id>/like')
@api.response(200, 'Successful operation')
@api.response(400, 'Invalid user id')
@api.response(404, 'User not found')
@api.response(500, 'Internal server error')
class UserUserIdDislike(Resource):

    """
        Get a list of dislike by user id
    """
    def get(self, user_id):
        return {}, 200, None

@api.route('/user/<string:user_id>/like')
@api.response(200, 'Successful operation')
@api.response(400, 'Invalid user id')
@api.response(404, 'User not found')
@api.response(500, 'Internal server error')
class UserUserIdStar(Resource):

    """
        Get a list of star by user id
    """
    def get(self, user_id):
        return {}, 200, None

@api.route('/user/<string:user_id>/like')
@api.response(200, 'Successful operation')
@api.response(400, 'Invalid user id')
@api.response(404, 'User not found')
@api.response(500, 'Internal server error')
class UserUserIdComment(Resource):

    """
        Get a list of comments by user id
    """
    def get(self, user_id):
        return {}, 200, None


if __name__ == '__main__':
    app.run(debug=True)

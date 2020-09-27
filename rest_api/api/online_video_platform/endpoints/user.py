import logging

from flask import request
from flask_restplus import Resource
from rest_api.api.restplus import api
from rest_api.api.online_video_platform.serializers import user
from rest_api.api.online_video_platform.serializers import user_login

log = logging.getLogger(__name__)

ns = api.namespace('user', description='Operations related to user')


@ns.route('/')
@api.response(400, 'Bad request')
@api.response(502, 'Internal server error')
class UserSignUp(Resource):

    @api.expect(user)
    @api.response(200, 'successful operation')
    def post(self):
        """
            User sign up
        """
        data = request.json
        print(data)
        return None, 200


@ns.route('/login')
@api.response(400, 'Invalid username/email/password supplied')
@api.response(502, 'Internal server error')
class UserLogin(Resource):

    @api.expect(user_login)
    @api.response(200, 'successful operation')
    def post(self):
        """
            User sign in
        """
        data = request.json
        print(data)
        return None, 200


@ns.route('/logout')
@api.response(400, 'Bad request')
@api.response(502, 'Internal server error')
class UserLogout(Resource):

    @api.expect(user_login)
    @api.response(200, 'successful operation')
    def post(self):
        """
            User log out
        """
        data = request.json
        print(data)
        return None, 200


@ns.route('/<int:user_id>')
@api.response(200, 'successful operation')
@api.response(400, 'Invalid username supplied')
@api.response(404, 'user not found.')
@api.response(502, 'Internal server error')
class UserOperation(Resource):

    @api.marshal_with(user)
    def get(self, user_id):
        """
        Browse user profile
        """
        data = {"user_name": user_id}
        return data, 200

    @api.response(405, 'method not allowed')
    def delete(self, user_id):
        """
        User delete account
        """
        print(user_id)
        return None, 200

    @api.expect(user)
    @api.response(405, 'method not allowed')
    def put(self, user_id):
        """
        Edit user profile
        """
        data = request.json
        print(user_id, data)
        return None, 200

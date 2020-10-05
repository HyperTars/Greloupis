# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import Flask, request, g
from flask_restx import Resource, Api, fields, marshal_with, reqparse, Namespace
import json

app = Flask(__name__)
api = Api(app)

"""
    User Module
"""
user = api.namespace('user', description='User APIs')

@user.route('')
@user.response(200, 'Successful operation')
@user.response(400, 'Invalid user information')
@user.response(405, 'Method not allowed')
@user.response(500, 'Internal server error')
class User(Resource):
    """
        User sign up
    """
    def post(self):
        return {}, 200, None

@user.route('/<string:user_id>')
@user.response(200, 'Successful operation')
@user.response(400, 'Invalid user information')
@user.response(404, 'User not found')
@user.response(500, 'Internal server error')
class UserUserId(Resource):
    """
        Get user information by id
    """
    def get(self, user_id):
        return {}, 200, None

    """
        Update user information by id
    """
    @user.response(405, 'Method not allowed')
    def put(self, user_id):
        return {}, 200, None

    """
        Delete user by id
    """
    @user.response(405, 'Method not allowed')
    def delete(self, user_id):
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

    """
        Get a list of like by user id
    """
    def get(self, user_id):
        return {}, 200, None

@user.route('/<string:user_id>/dislike')
@user.response(200, 'Successful operation')
@user.response(400, 'Invalid user id')
@user.response(404, 'User not found')
@user.response(500, 'Internal server error')
class UserUserIdDislike(Resource):

    """
        Get a list of dislike by user id
    """
    def get(self, user_id):
        return {}, 200, None

@user.route('/<string:user_id>/star')
@user.response(200, 'Successful operation')
@user.response(400, 'Invalid user id')
@user.response(404, 'User not found')
@user.response(500, 'Internal server error')
class UserUserIdStar(Resource):

    """
        Get a list of star by user id
    """
    def get(self, user_id):
        return {}, 200, None

@user.route('/<string:user_id>/comment')
@user.response(200, 'Successful operation')
@user.response(400, 'Invalid user id')
@user.response(404, 'User not found')
@user.response(500, 'Internal server error')
class UserUserIdComment(Resource):

    """
        Get a list of comments by user id
    """
    def get(self, user_id):
        return {}, 200, None



"""
    Video Module
"""
video = api.namespace('video', description='Video APIs')

@video.route('')
@video.response(200, 'Successful operation')
@video.response(400, 'Invalid video information')
@video.response(405, 'Method not allowed')
@video.response(500, 'Internal server error')
class Video(Resource):
    """
        User upload a video
    """
    def post(self):
        return {}, 200, None

@video.route('/<string:video_id>')
@video.response(200, 'Successful operation')
@video.response(400, 'Invalid video ID')
@video.response(404, 'Video not found')
@video.response(500, 'Internal server error')
class VideoVideoId(Resource):
    """
        Get video information by id
    """
    def get(self, video_id):
        return {}, 200, None

    """
        Update video information by id
    """
    @video.response(405, 'Method not allowed')
    def put(self, video_id):
        return {}, 200, None

    """
        Delete video by id
    """
    def delete(self, video_id):
        return {}, 200, None

@video.route('/<string:video_id>/view')
@video.response(200, 'Successful operation')
@video.response(400, 'Invalid video ID')
@video.response(404, 'Video not found')
@video.response(500, 'Internal server error')
class VideoVideoIdView(Resource):

    def get(self, video_id):
        return {}, 200, None

    @video.response(405, 'Method not allowed')
    def put(self, video_id):
        return {}, 200, None

@video.route('/<string:video_id>/comment')
@video.response(200, 'Successful operation')
@video.response(400, 'Invalid video ID')
@video.response(404, 'Video not found')
@video.response(500, 'Internal server error')
class VideoVideoIdComment(Resource):

    def get(self, video_id):
        return {}, 200, None

@video.route('/<string:video_id>/comment/<string:user_id>')
@video.response(200, 'Successful operation')
@video.response(400, 'Invalid video ID  or user ID')
@video.response(404, 'Video or user not found')
@video.response(500, 'Internal server error')
class VideoVideoIdCommentUserId(Resource):

    def get(self, video_id, user_id):
        return {}, 200, None

    @video.response(405, 'Method not allowed')
    def post(self, video_id, user_id):
        return {}, 200, None

    @video.response(405, 'Method not allowed')
    def put(self, video_id, user_id):
        return {}, 200, None

    @video.response(405, 'Method not allowed')
    def delete(self, video_id, user_id):
        return {}, 200, None

@video.route('/<string:video_id>/dislike')
@video.response(200, 'Successful operation')
@video.response(400, 'Invalid video ID')
@video.response(404, 'Video not found')
@video.response(500, 'Internal server error')
class VideoVideoIdDislike(Resource):

    def get(self, video_id):
        return {}, 200, None

@video.route('/<string:video_id>/dislike/<string:user_id>')
@video.response(200, 'Successful operation')
@video.response(400, 'Invalid video ID or user ID')
@video.response(404, 'Video or user not found')
@video.response(405, 'Method not allowed')
@video.response(500, 'Internal server error')
class VideoVideoIdDislikeUserId(Resource):
    
    def post(self, video_id, user_id):
        return {}, 200, None

    def delete(self, video_id, user_id):
        return {}, 200, None

@video.route('/<string:video_id>/like')
@video.response(200, 'Successful operation')
@video.response(400, 'Invalid video ID')
@video.response(404, 'Video not found')
@video.response(500, 'Internal server error')
class VideoVideoIdLike(Resource):

    def get(self, video_id):
        return {}, 200, None

@video.route('/<string:video_id>/like/<string:user_id>')
@video.response(200, 'Successful operation')
@video.response(400, 'Invalid video ID or user ID')
@video.response(404, 'Video or user not found')
@video.response(405, 'Method not allowed')
@video.response(500, 'Internal server error')
class VideoVideoIdLikeUserId(Resource):

    def post(self, video_id, user_id):
        return {}, 200, None

    def delete(self, video_id, user_id):
        return {}, 200, None

@video.route('/<string:video_id>/star')
@video.response(200, 'Successful operation')
@video.response(400, 'Invalid video ID')
@video.response(404, 'Video not found')
@video.response(500, 'Internal server error')
class VideoVideoIdStar(Resource):

    def get(self, video_id):
        return {}, 200, None

@video.route('/<string:video_id>/star/<string:user_id>')
@video.response(200, 'Successful operation')
@video.response(400, 'Invalid video ID or user ID')
@video.response(404, 'Video or user not found')
@video.response(405, 'Method not allowed')
@video.response(500, 'Internal server error')
class VideoVideoIdStarUserId(Resource):

    def post(self, video_id, user_id):
        return {}, 200, None

    def delete(self, video_id, user_id):
        return {}, 200, None
"""
    Search Module
"""
search = api.namespace('search', description='Search APIs')

'''
 @route     GET /search/video/<string:keyword>
 @desc      Search videos by keyword
 @access    Public
'''

@search.route('/video/<string:keyword>')
@search.response(400, 'Bad request.')
@search.response(500, 'Internal server error.')
class SearchVideo(Resource):
    @search.doc(responses={200: 'Successfully got video search results.'})
    def get(self, keyword):
        search_result = []
        return {}, 200, None


'''
 @route     GET /search/user/<string:keyword>
 @desc      Search users by keyword
 @access    Public
'''
@search.route('/user/<string:keyword>')
@search.response(400, 'Bad request.')
@search.response(500, 'Internal server error.')
class SearchUser(Resource):
    @search.doc(responses={200: 'Successfully got user search results.'})
    def get(self, keyword):
        search_result = []
        return {}, 200, None


if __name__ == '__main__':
    app.run(debug=True)

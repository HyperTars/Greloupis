# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import Flask, request, g, Blueprint
from flask_restx import Resource, Api, fields, marshal_with, reqparse, Namespace
import json

video = Namespace('video', description='Video APIs')

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
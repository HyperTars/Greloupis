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

    def post(self):
        """
            User upload a video
        """
        return {}, 200, None

@video.route('/<string:video_id>')
@video.param('video_id', 'Video ID')
@video.response(200, 'Successful operation')
@video.response(400, 'Invalid video ID')
@video.response(404, 'Video not found')
@video.response(500, 'Internal server error')
class VideoVideoId(Resource):

    def get(self, video_id):
        """
            Get video information by video ID
        """
        return {}, 200, None

    @video.response(405, 'Method not allowed')
    def put(self, video_id):
        """
            Update video information by video ID
        """        
        return {}, 200, None

    def delete(self, video_id):
        """
            Delete video information by video ID
        """        
        return {}, 200, None

@video.route('/<string:video_id>/view')
@video.param('video_id', 'Video ID')
@video.response(200, 'Successful operation')
@video.response(400, 'Invalid video ID')
@video.response(404, 'Video not found')
@video.response(500, 'Internal server error')
class VideoVideoIdView(Resource):

    def get(self, video_id):
        """
            Get video view count by video ID
        """
        return {}, 200, None

    @video.response(405, 'Method not allowed')
    def put(self, video_id):
        """
            Increment video view count by 1 by video ID
        """
        return {}, 200, None

@video.route('/<string:video_id>/comment')
@video.param('video_id', 'Video ID')
@video.response(200, 'Successful operation')
@video.response(400, 'Invalid video ID')
@video.response(404, 'Video not found')
@video.response(500, 'Internal server error')
class VideoVideoIdComment(Resource):

    def get(self, video_id):
        """
            Get video view comments list by video ID
        """        
        return {}, 200, None

@video.route('/<string:video_id>/comment/<string:user_id>')
@video.param('video_id', 'Video ID')
@video.param('user_id', 'User ID')
@video.response(200, 'Successful operation')
@video.response(400, 'Invalid video ID  or user ID')
@video.response(404, 'Video or user not found')
@video.response(500, 'Internal server error')
class VideoVideoIdCommentUserId(Resource):

    def get(self, video_id, user_id):
        """
            Get a comment by specified video id and user id
        """           
        return {}, 200, None

    @video.response(405, 'Method not allowed')
    def post(self, video_id, user_id):
        """
            Post a comment by specified video id and user id
        """            
        return {}, 200, None

    @video.response(405, 'Method not allowed')
    def put(self, video_id, user_id):
        """
            Update a comment by specified video id and user id
        """           
        return {}, 200, None

    @video.response(405, 'Method not allowed')
    def delete(self, video_id, user_id):
        """
            Delete a comment by specified video id and user id
        """   
        return {}, 200, None

@video.route('/<string:video_id>/dislike')
@video.param('video_id', 'Video ID')
@video.response(200, 'Successful operation')
@video.response(400, 'Invalid video ID')
@video.response(404, 'Video not found')
@video.response(500, 'Internal server error')
class VideoVideoIdDislike(Resource):

    def get(self, video_id):
        """
            Get a list of dislike by video id
        """   
        return {}, 200, None

@video.route('/<string:video_id>/dislike/<string:user_id>')
@video.param('video_id', 'Video ID')
@video.param('user_id', 'User ID')
@video.response(200, 'Successful operation')
@video.response(400, 'Invalid video ID or user ID')
@video.response(404, 'Video or user not found')
@video.response(405, 'Method not allowed')
@video.response(500, 'Internal server error')
class VideoVideoIdDislikeUserId(Resource):
    
    def post(self, video_id, user_id):
        """
            Post a dislike by specified user and video
        """           
        return {}, 200, None

    def delete(self, video_id, user_id):
        """
            Undo a dislike by specified user and video
        """          
        return {}, 200, None

@video.route('/<string:video_id>/like')
@video.param('video_id', 'Video ID')
@video.response(200, 'Successful operation')
@video.response(400, 'Invalid video ID')
@video.response(404, 'Video not found')
@video.response(500, 'Internal server error')
class VideoVideoIdLike(Resource):

    def get(self, video_id):
        """
            Get a list of like by video id
        """           
        return {}, 200, None

@video.route('/<string:video_id>/like/<string:user_id>')
@video.param('video_id', 'Video ID')
@video.param('user_id', 'User ID')
@video.response(200, 'Successful operation')
@video.response(400, 'Invalid video ID or user ID')
@video.response(404, 'Video or user not found')
@video.response(405, 'Method not allowed')
@video.response(500, 'Internal server error')
class VideoVideoIdLikeUserId(Resource):

    def post(self, video_id, user_id):
        """
            Post a like by specified user and video
        """         
        return {}, 200, None

    def delete(self, video_id, user_id):
        """
            Undo a like by specified user and video
        """             
        return {}, 200, None

@video.route('/<string:video_id>/star')
@video.param('video_id', 'Video ID')
@video.response(200, 'Successful operation')
@video.response(400, 'Invalid video ID')
@video.response(404, 'Video not found')
@video.response(500, 'Internal server error')
class VideoVideoIdStar(Resource):

    def get(self, video_id):
        """
            Get a list of star by video id
        """            
        return {}, 200, None

@video.route('/<string:video_id>/star/<string:user_id>')
@video.param('video_id', 'Video ID')
@video.param('user_id', 'User ID')
@video.response(200, 'Successful operation')
@video.response(400, 'Invalid video ID or user ID')
@video.response(404, 'Video or user not found')
@video.response(405, 'Method not allowed')
@video.response(500, 'Internal server error')
class VideoVideoIdStarUserId(Resource):

    def post(self, video_id, user_id):
        """
            Post a star by specified user and video
        """           
        return {}, 200, None

    def delete(self, video_id, user_id):
        """
            Undo a star by specified user and video
        """           
        return {}, 200, None
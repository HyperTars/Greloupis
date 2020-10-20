# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import Flask, request, g, Blueprint
from flask_restx import Resource, Api, fields, marshal_with, reqparse, Namespace
import json

from .route_user import thumbnail, general_response, star, comment, like, dislike, \
    star_response_list, comment_response_list, like_response_list, dislike_response_list

from source.service.service_video import *
from source.service.service_video_op import *
from source.utils.util_serializer import *
from source.settings import *

video = Namespace('video', description='Video APIs')

video_uri = video.model(name='VideoURI', model={
    'video_low': fields.String,
    'video_mid': fields.String,
    'video_high': fields.String,
})

video_info = video.model(name='Video', model={
    'video_id': fields.String,
    'user_id': fields.String,
    'video_title': fields.String,
    'video_raw_content': fields.String,
    'video_raw_status': fields.String,
    'video_raw_size': fields.Float,
    'video_duration': fields.Integer,
    'video_channel': fields.String,
    'video_tag': fields.List(fields.String),
    'video_category': fields.List(fields.String),
    'video_description': fields.String,
    'video_language': fields.String,
    'video_status': fields.String,
    'video_view': fields.Integer,
    'video_comment': fields.Integer,
    'video_like': fields.Integer,
    'video_dislike': fields.Integer,
    'video_star': fields.Integer,
    'video_thumbnail': fields.Nested(thumbnail),
    'video_upload_date': fields.DateTime,
    'video_uri': fields.Nested(video_uri)
})

view = video.model(name='View', model={
    'video_id': fields.String,
    'view_count': fields.Integer
})

view_response = video.model(name='ApiResponseWithView', model={
    'code': fields.String,
    'body': fields.Nested(view)
})

like_response = video.model(name='ApiResponseWithLike', model={
    'code': fields.String,
    'body': fields.Nested(like)
})

dislike_response = video.model(name='ApiResponseWithDislike', model={
    'code': fields.String,
    'body': fields.Nested(dislike)
})

star_response = video.model(name='ApiResponseWithStar', model={
    'code': fields.String,
    'body': fields.Nested(star)
})

comment_response = video.model(name='ApiResponseWithComment', model={
    'code': fields.String,
    'body': fields.Nested(comment)
})


@video.route('', methods=['POST'])
@video.response(200, 'Successful operation', video_info)
@video.response(400, 'Invalid video information', general_response)
@video.response(405, 'Method not allowed', general_response)
@video.response(500, 'Internal server error', general_response)
class Video(Resource):

    def post(self):
        """
            User upload a video
        """
        mock_body = {
            "user_id": "5f88f883e6ac4f89900ac983",
            "video_title": "mock_video_2",
            "video_raw_content": "https://s3.amazon.com/mock_video.mp4",
            "video_raw_size": 13.23
        }

        # user_id = request.form.get("user_id")

        return service_video_upload(conf=config['default'], body=mock_body)


@video.route('/<string:video_id>', methods=['DELETE', 'GET', 'PUT'])
@video.param('video_id', 'Video ID')
@video.response(200, 'Successful operation', video_info)
@video.response(400, 'Invalid video ID', general_response)
@video.response(404, 'Video not found', general_response)
@video.response(500, 'Internal server error', general_response)
class VideoVideoId(Resource):

    def get(self, video_id):
        """
            Get video information by video ID
        """
        video_id = request.url.split('/')[-1]

        return service_video_info(conf=config['default'], video_id=video_id)

    @video.response(405, 'Method not allowed')
    def put(self, video_id):
        """
            Update video information by video ID
        """
        video_id = request.url.split('/')[-1]

        mock_body = {
            "video_title": "mock_video_updated",
            "video_status": "public",
            "video_raw_size": 51.23
        }

        return service_video_update(conf=config['default'], video_id=video_id, body=mock_body)

    def delete(self, video_id):
        """
            Delete video information by video ID
        """
        video_id = request.url.split('/')[-1]

        return service_video_delete(conf=config['default'], video_id=video_id)


@video.route('/<string:video_id>/view', methods=['GET', 'PUT'])
@video.param('video_id', 'Video ID')
@video.response(200, 'Successful operation', view_response)
@video.response(400, 'Invalid video ID', general_response)
@video.response(404, 'Video not found', general_response)
@video.response(500, 'Internal server error', general_response)
class VideoVideoIdView(Resource):

    def get(self, video_id):
        """
            Get video view count by video ID
        """
        video_id = request.url.split('/')[-2]

        return service_video_op_get_view(conf=config['default'], video_id=video_id)

    @video.response(405, 'Method not allowed')
    def put(self, video_id):
        """
            Increment video view count by 1 by video ID
        """
        video_id = request.url.split('/')[-2]

        return service_video_op_add_view(conf=config['default'], video_id=video_id)


@video.route('/<string:video_id>/comment', methods=['GET'])
@video.param('video_id', 'Video ID')
@video.response(200, 'Successful operation', comment_response_list)
@video.response(400, 'Invalid video ID', general_response)
@video.response(404, 'Video not found', general_response)
@video.response(500, 'Internal server error', general_response)
class VideoVideoIdComment(Resource):

    def get(self, video_id):
        """
            Get video view comments list by video ID
        """
        video_id = request.url.split('/')[-2]

        return service_video_comments(conf=config['default'], video_id=video_id)


@video.route('/<string:video_id>/comment/<string:user_id>', methods=['DELETE', 'GET', 'PUT', 'POST'])
@video.param('video_id', 'Video ID')
@video.param('user_id', 'User ID')
@video.response(200, 'Successful operation', comment_response)
@video.response(400, 'Invalid video ID  or user ID', general_response)
@video.response(404, 'Video or user not found', general_response)
@video.response(500, 'Internal server error', general_response)
class VideoVideoIdCommentUserId(Resource):

    def get(self, video_id, user_id):
        """
            Get a comment by specified video id and user id
        """
        video_id = request.url.split('/')[-3]
        user_id = request.url.split('/')[-1]

        return service_video_op_get_comment(conf=config['default'], video_id=video_id, user_id=user_id)

    @video.response(405, 'Method not allowed')
    def post(self, video_id, user_id):
        """
            Post a comment by specified video id and user id
        """
        video_id = request.url.split('/')[-3]
        user_id = request.url.split('/')[-1]

        mock_body = {
            "comment": "This video is so funny"
        }

        return service_video_op_add_comment(conf=config['default'], video_id=video_id, user_id=user_id, body=mock_body)

    @video.response(405, 'Method not allowed')
    def put(self, video_id, user_id):
        """
            Update a comment by specified video id and user id
        """
        video_id = request.url.split('/')[-3]
        user_id = request.url.split('/')[-1]

        mock_body = {
            "comment": "This video is so funny updated"
        }

        return service_video_op_update_comment(conf=config['default'], video_id=video_id,
                                               user_id=user_id, body=mock_body)

    @video.response(405, 'Method not allowed')
    def delete(self, video_id, user_id):
        """
            Delete a comment by specified video id and user id
        """
        video_id = request.url.split('/')[-3]
        user_id = request.url.split('/')[-1]

        return service_video_op_cancel_comment(conf=config['default'], video_id=video_id, user_id=user_id)


@video.route('/<string:video_id>/dislike', methods=['GET'])
@video.param('video_id', 'Video ID')
@video.response(200, 'Successful operation', dislike_response_list)
@video.response(400, 'Invalid video ID', general_response)
@video.response(404, 'Video not found', general_response)
@video.response(500, 'Internal server error', general_response)
class VideoVideoIdDislike(Resource):

    def get(self, video_id):
        """
            Get a list of dislike by video id
        """
        return {}, 200, None


@video.route('/<string:video_id>/dislike/<string:user_id>', methods=['DELETE', 'POST'])
@video.param('video_id', 'Video ID')
@video.param('user_id', 'User ID')
@video.response(200, 'Successful operation', dislike_response)
@video.response(400, 'Invalid video ID or user ID', general_response)
@video.response(404, 'Video or user not found', general_response)
@video.response(405, 'Method not allowed', general_response)
@video.response(500, 'Internal server error', general_response)
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


@video.route('/<string:video_id>/process/<string:user_id>', methods=['DELETE', 'POST', 'PUT', 'GET'])
@video.param('video_id', 'Video ID')
@video.param('user_id', 'User ID')
@video.response(200, 'Successful operation', general_response)
@video.response(400, 'Invalid video ID or user ID', general_response)
@video.response(404, 'Video or user not found', general_response)
@video.response(405, 'Method not allowed', general_response)
@video.response(500, 'Internal server error', general_response)
class VideoVideoIdProcessUserId(Resource):

    def post(self, video_id, user_id):
        """
            Post a new video watching process
        """
        return {}, 200, None

    def get(self, video_id, user_id):
        """
            Get a new video watching process
        """
        return {}, 200, None

    def put(self, video_id, user_id):
        """
            Update a video watching process
        """
        return {}, 200, None

    def delete(self, video_id, user_id):
        """
            Delete a video watching process
        """
        return {}, 200, None


@video.route('/<string:video_id>/like', methods=['GET'])
@video.param('video_id', 'Video ID')
@video.response(200, 'Successful operation', like_response_list)
@video.response(400, 'Invalid video ID', general_response)
@video.response(404, 'Video not found', general_response)
@video.response(500, 'Internal server error', general_response)
class VideoVideoIdLike(Resource):

    def get(self, video_id):
        """
            Get a list of like by video id
        """
        return {}, 200, None


@video.route('/<string:video_id>/like/<string:user_id>', methods=['DELETE', 'POST'])
@video.param('video_id', 'Video ID')
@video.param('user_id', 'User ID')
@video.response(200, 'Successful operation', like_response)
@video.response(400, 'Invalid video ID or user ID', general_response)
@video.response(404, 'Video or user not found', general_response)
@video.response(405, 'Method not allowed', general_response)
@video.response(500, 'Internal server error', general_response)
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


@video.route('/<string:video_id>/star', methods=['GET'])
@video.param('video_id', 'Video ID')
@video.response(200, 'Successful operation', star_response_list)
@video.response(400, 'Invalid video ID', general_response)
@video.response(404, 'Video not found', general_response)
@video.response(500, 'Internal server error', general_response)
class VideoVideoIdStar(Resource):

    def get(self, video_id):
        """
            Get a list of star by video id
        """
        return {}, 200, None


@video.route('/<string:video_id>/star/<string:user_id>', methods=['DELETE', 'POST'])
@video.param('video_id', 'Video ID')
@video.param('user_id', 'User ID')
@video.response(200, 'Successful operation', star_response)
@video.response(400, 'Invalid video ID or user ID', general_response)
@video.response(404, 'Video or user not found', general_response)
@video.response(405, 'Method not allowed', general_response)
@video.response(500, 'Internal server error', general_response)
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

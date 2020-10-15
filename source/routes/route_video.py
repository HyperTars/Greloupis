# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import Flask, request, g, Blueprint
from flask_restx import Resource, Api, fields, marshal_with, reqparse, Namespace
import json

from .route_user import thumbnail, general_response, star, comment, like, dislike, \
    star_response_list, comment_response_list, like_response_list, dislike_response_list

from source.service.service_video import *
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


@video.route('')
@video.response(200, 'Successful operation', video_info)
@video.response(400, 'Invalid video information', general_response)
@video.response(405, 'Method not allowed', general_response)
@video.response(500, 'Internal server error', general_response)
class Video(Resource):

    def post(self):
        """
            User upload a video
        """
        return {}, 200, None


@video.route('/<string:video_id>')
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
        # if 'video_id' not in req_dict:
        #     return {ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_code():
        #             ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg()}, 200, None

        search_result = service_video_info(conf=config['default'], video_id=video_id)
        search_result_json = util_serializer_mongo_results_to_array(search_result, format="json")

        return util_serializer_api_response(search_result_json, 200)

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
@video.response(200, 'Successful operation', view_response)
@video.response(400, 'Invalid video ID', general_response)
@video.response(404, 'Video not found', general_response)
@video.response(500, 'Internal server error', general_response)
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
@video.response(200, 'Successful operation', comment_response_list)
@video.response(400, 'Invalid video ID', general_response)
@video.response(404, 'Video not found', general_response)
@video.response(500, 'Internal server error', general_response)
class VideoVideoIdComment(Resource):

    def get(self, video_id):
        """
            Get video view comments list by video ID
        """
        return {}, 200, None


@video.route('/<string:video_id>/comment/<string:user_id>')
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


@video.route('/<string:video_id>/dislike/<string:user_id>')
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


@video.route('/<string:video_id>/like')
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


@video.route('/<string:video_id>/like/<string:user_id>')
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


@video.route('/<string:video_id>/star')
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


@video.route('/<string:video_id>/star/<string:user_id>')
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

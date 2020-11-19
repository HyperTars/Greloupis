# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import request
from flask_jwt_extended import jwt_required, jwt_optional, get_jwt_identity
from flask_restx import Resource, fields, Namespace

# from service.service_user import service_user_get_info
from .route_user import thumbnail, general_response, star, comment, like, \
    dislike, star_response_list, comment_response_list, like_response_list, \
    dislike_response_list
from service.service_video import service_video_info, service_video_delete, \
    service_video_comments, service_video_dislikes, service_video_likes, \
    service_video_stars, service_video_update, service_video_upload, \
    service_video_auth_get, service_video_auth_modify
from service.service_video_op import service_video_op_add_comment, \
    service_video_op_add_dislike, service_video_op_add_like, \
    service_video_op_add_process, service_video_op_add_star, \
    service_video_op_add_view, service_video_op_cancel_comment, \
    service_video_op_cancel_dislike, service_video_op_cancel_like, \
    service_video_op_cancel_process, service_video_op_cancel_star, \
    service_video_op_get_comment, service_video_op_get_process, \
    service_video_op_get_view, service_video_op_update_comment, \
    service_video_op_update_process, service_video_op_auth_get, \
    service_video_op_auth_post, service_video_op_auth_modify
from utils.util_error_handler import util_error_handler
from utils.util_serializer import util_serializer_api_response, \
    util_serializer_mongo_results_to_array
from settings import config
from models.model_errors import ServiceError, RouteError, MongoError, \
    ErrorCode

import ast

# from flask import Flask, g, Blueprint
# from flask_restx import Api, marshal_with, reqparse
# from source.utils.util_serializer import *
# import json

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


#########
# Video #
#########
@video.route('', methods=['POST'])
@video.response(200, 'Successful operation', video_info)
@video.response(400, 'Invalid video information', general_response)
@video.response(405, 'Method not allowed', general_response)
@video.response(500, 'Internal server error', general_response)
class Video(Resource):

    @jwt_required
    def post(self, conf=config["default"]):
        """
            User upload a video
        """

        try:
            if request.form != {}:
                kw = dict(request.form)
            else:
                raw_data = request.data.decode("utf-8")
                kw = ast.literal_eval(raw_data)

            # check authority
            if get_jwt_identity is None:
                raise RouteError(ErrorCode.ROUTE_TOKEN_REQUIRED)

            kw['user_id'] = get_jwt_identity()
            upload_result = service_video_upload(conf=conf, **kw)
            if upload_result is not None and upload_result != {}:
                return_body = util_serializer_mongo_results_to_array(
                    upload_result, format="json")
                return util_serializer_api_response(
                    200, body=return_body, msg="Successfully uploaded video")
            else:
                return util_serializer_api_response(
                    500, msg="Failed to upload video")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)


@video.route('/<string:video_id>', methods=['DELETE', 'GET', 'PUT'])
@video.param('video_id', 'Video ID')
@video.response(200, 'Successful operation', video_info)
@video.response(400, 'Invalid video ID', general_response)
@video.response(404, 'Video not found', general_response)
@video.response(500, 'Internal server error', general_response)
class VideoVideoId(Resource):

    @jwt_optional
    def get(self, video_id, conf=config["default"]):
        """
            Get video information by video ID
        """
        try:
            video_id = request.url.split('/')[-1]
            token = get_jwt_identity()

            # check authority
            if service_video_auth_get(token, video_id) is False:
                raise RouteError(ErrorCode.ROUTE_PRIVATE_VIDEO)

            video = service_video_info(
                conf=conf, video_id=request.url.split('/')[-1])

            return util_serializer_api_response(
                    200, body=video, msg="Successfully got video by ID.")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)

    @jwt_required
    @video.response(405, 'Method not allowed')
    def put(self, video_id, conf=config["default"]):
        """
            Update video information by video ID
        """

        try:
            if request.form != {}:
                kw = dict(request.form)
            else:
                raw_data = request.data.decode("utf-8")
                kw = ast.literal_eval(raw_data)

            video_id = request.url.split('/')[-1]
            token = get_jwt_identity()

            # check authority
            if not service_video_auth_modify(token, video_id):
                raise RouteError(ErrorCode.ROUTE_TOKEN_NOT_PERMITTED)

            kw["video_id"] = video_id
            if "video_tag" in kw.keys():
                kw["video_tag"] = request.form.getlist("video_tag")
            if "video_category" in kw.keys():
                kw["video_category"] = request.form.getlist("video_category")

            update_result = service_video_update(conf=conf, **kw)
            if len(update_result) == 1:
                return_body = util_serializer_mongo_results_to_array(
                    update_result, format="json")
                return util_serializer_api_response(
                    200, body=return_body, msg="Successfully updated video")
            else:
                return util_serializer_api_response(
                    500, msg="Failed to update video")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)

    @jwt_required
    def delete(self, video_id, conf=config["default"]):
        """
            Delete video information by video ID
        """

        try:
            video_id = request.url.split('/')[-1]
            token = get_jwt_identity()

            # check authority
            if service_video_auth_modify(token, video_id) is False:
                raise RouteError(ErrorCode.ROUTE_TOKEN_NOT_PERMITTED)

            delete_result = service_video_delete(
                conf=conf, video_id=request.url.split('/')[-1])
            if delete_result == 1:
                return util_serializer_api_response(
                    200, msg="Successfully deleted video")
            else:
                return util_serializer_api_response(
                    500, msg="Failed to delete video")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)


@video.route('/<string:video_id>/view', methods=['GET', 'PUT'])
@video.param('video_id', 'Video ID')
@video.response(200, 'Successful operation', view_response)
@video.response(400, 'Invalid video ID', general_response)
@video.response(404, 'Video not found', general_response)
@video.response(500, 'Internal server error', general_response)
class VideoVideoIdView(Resource):

    @jwt_optional
    def get(self, video_id, conf=config["default"]):
        """
            Get video view count by video ID
        """
        try:
            video_id = request.url.split('/')[-2]
            token = get_jwt_identity()

            # check authority
            if service_video_auth_get(token, video_id) is False:
                raise RouteError(ErrorCode.ROUTE_PRIVATE_VIDEO)

            view_result = service_video_op_get_view(
                conf=conf, video_id=video_id)

            return util_serializer_api_response(
                200, body=view_result, msg="Successfully get video view count")

        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)

    @video.response(405, 'Method not allowed')
    def put(self, video_id, conf=config["default"]):
        """
            Increment video view count by 1 by video ID
        """

        try:
            video_id = request.url.split('/')[-2]

            add_result = service_video_op_add_view(
                conf=conf, video_id=video_id)

            return util_serializer_api_response(
                200, body=add_result,
                msg="Successfully add video view count by 1")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)


@video.route('/<string:video_id>/comment', methods=['GET'])
@video.param('video_id', 'Video ID')
@video.response(200, 'Successful operation', comment_response_list)
@video.response(400, 'Invalid video ID', general_response)
@video.response(404, 'Video not found', general_response)
@video.response(500, 'Internal server error', general_response)
class VideoVideoIdComment(Resource):

    @jwt_optional
    def get(self, video_id, conf=config['default']):
        """
            Get video view comments list by video ID
        """
        # TODO
        # print("get user name", get_jwt_identity())
        try:
            video_id = request.url.split('/')[-2]
            token = get_jwt_identity()

            # check authority
            if service_video_auth_get(token, video_id) is False:
                raise RouteError(ErrorCode.ROUTE_PRIVATE_VIDEO)

            comments_result = service_video_comments(
                conf=conf, video_id=video_id)

            return util_serializer_api_response(
                200, body=comments_result,
                msg="Successfully got video comments")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)


@video.route('/<string:video_id>/dislike', methods=['GET'])
@video.param('video_id', 'Video ID')
@video.response(200, 'Successful operation', dislike_response_list)
@video.response(400, 'Invalid video ID', general_response)
@video.response(404, 'Video not found', general_response)
@video.response(500, 'Internal server error', general_response)
class VideoVideoIdDislike(Resource):

    @jwt_optional
    def get(self, video_id, conf=config['default']):
        """
            Get a list of dislike by video id
        """
        try:
            video_id = request.url.split('/')[-2]
            token = get_jwt_identity()

            # check authority
            if service_video_auth_get(token, video_id) is False:
                raise RouteError(ErrorCode.ROUTE_PRIVATE_VIDEO)

            dislike_result = service_video_dislikes(
                conf=conf, video_id=video_id)

            return util_serializer_api_response(
                200, body=dislike_result,
                msg="Successfully got video dislikes")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)


@video.route('/<string:video_id>/like', methods=['GET'])
@video.param('video_id', 'Video ID')
@video.response(200, 'Successful operation', like_response_list)
@video.response(400, 'Invalid video ID', general_response)
@video.response(404, 'Video not found', general_response)
@video.response(500, 'Internal server error', general_response)
class VideoVideoIdLike(Resource):

    @jwt_optional
    def get(self, video_id, conf=config['default']):
        """
            Get a list of like by video id
        """
        try:
            video_id = request.url.split('/')[-2]
            token = get_jwt_identity()

            # check authority
            if service_video_auth_get(token, video_id) is False:
                raise RouteError(ErrorCode.ROUTE_PRIVATE_VIDEO)

            like_result = service_video_likes(conf=conf, video_id=video_id)
            return util_serializer_api_response(
                200, body=like_result, msg="Successfully got video likes")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)


@video.route('/<string:video_id>/star', methods=['GET'])
@video.param('video_id', 'Video ID')
@video.response(200, 'Successful operation', star_response_list)
@video.response(400, 'Invalid video ID', general_response)
@video.response(404, 'Video not found', general_response)
@video.response(500, 'Internal server error', general_response)
class VideoVideoIdStar(Resource):

    @jwt_optional
    def get(self, video_id, conf=config['default']):
        """
            Get a list of star by video id
        """
        try:
            video_id = request.url.split('/')[-2]
            token = get_jwt_identity()

            # check authority
            if service_video_auth_get(token, video_id) is False:
                raise RouteError(ErrorCode.ROUTE_PRIVATE_VIDEO)

            star_result = service_video_stars(conf=conf, video_id=video_id)

            return util_serializer_api_response(
                200, body=star_result, msg="Successfully got video stars")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)


###########
# VideoOp #
###########
@video.route('/<string:video_id>/comment/<string:user_id>',
             methods=['DELETE', 'GET', 'PUT', 'POST'])
@video.param('video_id', 'Video ID')
@video.param('user_id', 'User ID')
@video.response(200, 'Successful operation', comment_response)
@video.response(400, 'Invalid video ID  or user ID', general_response)
@video.response(404, 'Video or user not found', general_response)
@video.response(500, 'Internal server error', general_response)
class VideoVideoIdCommentUserId(Resource):

    @jwt_optional
    def get(self, video_id, user_id, conf=config['default']):
        """
            Get a comment by specified video id and user id
        """
        try:
            video_id = request.url.split('/')[-3]
            user_id = request.url.split('/')[-1]
            token = get_jwt_identity()

            # check authority
            if not service_video_op_auth_get(token, user_id, video_id):
                raise RouteError(ErrorCode.ROUTE_TOKEN_REQUIRED)

            comments_result = service_video_op_get_comment(
                conf=conf, video_id=video_id, user_id=user_id)

            return util_serializer_api_response(
                200, body=comments_result,
                msg="Successfully get comments of the user")

        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)

    @jwt_required
    @video.response(405, 'Method not allowed')
    def post(self, video_id, user_id, conf=config['default']):
        """
            Post a comment by specified video id and user id
        """

        try:
            if request.form != {}:
                kw = dict(request.form)
            else:
                raw_data = request.data.decode("utf-8")
                kw = ast.literal_eval(raw_data)

            video_id = request.url.split('/')[-3]
            user_id = request.url.split('/')[-1]
            token = get_jwt_identity()

            # check authority
            if not service_video_op_auth_post(token, user_id, video_id):
                raise RouteError(ErrorCode.ROUTE_TOKEN_REQUIRED)

            kw['video_id'] = video_id
            kw['user_id'] = user_id
            comments_result = service_video_op_add_comment(conf=conf, **kw)

            return util_serializer_api_response(
                200, body=comments_result, msg="Successfully post a comment")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)

    @jwt_required
    @video.response(405, 'Method not allowed')
    def put(self, video_id, user_id, conf=config['default']):
        """
            Update a comment by specified video id and user id
        """

        try:
            if request.form != {}:
                kw = dict(request.form)
            else:
                raw_data = request.data.decode("utf-8")
                kw = ast.literal_eval(raw_data)

            video_id = request.url.split('/')[-3]
            user_id = request.url.split('/')[-1]
            token = get_jwt_identity()

            # check authority
            if not service_video_op_auth_modify(token, user_id):
                raise RouteError(ErrorCode.ROUTE_TOKEN_REQUIRED)

            kw['video_id'] = video_id
            kw['user_id'] = user_id
            comments_result = service_video_op_update_comment(conf=conf, **kw)

            return util_serializer_api_response(
                200, body=comments_result, msg="Successfully update a comment")

        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)

    @jwt_required
    @video.response(405, 'Method not allowed')
    def delete(self, video_id, user_id, conf=config['default']):
        """
            Delete a comment by specified video id and user id
        """

        try:
            video_id = request.url.split('/')[-3]
            user_id = request.url.split('/')[-1]
            token = get_jwt_identity()

            # check authority
            if not service_video_op_auth_modify(token, user_id):
                raise RouteError(ErrorCode.ROUTE_TOKEN_REQUIRED)

            comments_result = service_video_op_cancel_comment(
                conf=conf, video_id=video_id, user_id=user_id)

            return util_serializer_api_response(
                200, body=comments_result, msg="Successfully delete a comment")

        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)


@video.route('/<string:video_id>/process/<string:user_id>',
             methods=['DELETE', 'POST', 'PUT', 'GET'])
@video.param('video_id', 'Video ID')
@video.param('user_id', 'User ID')
@video.response(200, 'Successful operation', general_response)
@video.response(400, 'Invalid video ID or user ID', general_response)
@video.response(404, 'Video or user not found', general_response)
@video.response(405, 'Method not allowed', general_response)
@video.response(500, 'Internal server error', general_response)
class VideoVideoIdProcessUserId(Resource):

    @jwt_optional
    def get(self, video_id, user_id, conf=config['default']):
        """
            Get a new video watching process
        """
        try:
            video_id = request.url.split('/')[-3]
            user_id = request.url.split('/')[-1]
            token = get_jwt_identity()

            # check authority
            if not service_video_op_auth_get(token, user_id, video_id):
                raise RouteError(ErrorCode.ROUTE_TOKEN_REQUIRED)

            process_result = service_video_op_get_process(
                conf=conf, video_id=video_id, user_id=user_id)

            return util_serializer_api_response(
                200, body=process_result, msg="Successfully get video process")

        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)

    @jwt_required
    def post(self, video_id, user_id, conf=config['default']):
        """
            Post a new video watching process
        """

        try:
            if request.form != {}:
                kw = dict(request.form)
            else:
                raw_data = request.data.decode("utf-8")
                kw = ast.literal_eval(raw_data)

            video_id = request.url.split('/')[-3]
            user_id = request.url.split('/')[-1]
            token = get_jwt_identity()

            # check authority
            if not service_video_op_auth_post(token, user_id, video_id):
                raise RouteError(ErrorCode.ROUTE_TOKEN_REQUIRED)

            kw['video_id'] = video_id
            kw['user_id'] = user_id
            process_result = service_video_op_add_process(conf=conf, **kw)

            return util_serializer_api_response(
                200, body=process_result, msg="Successfully add video process")

        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)

    @jwt_required
    def put(self, video_id, user_id, conf=config['default']):
        """
            Update a video watching process
        """

        try:
            if request.form != {}:
                kw = dict(request.form)
            else:
                raw_data = request.data.decode("utf-8")
                kw = ast.literal_eval(raw_data)
            video_id = request.url.split('/')[-3]
            user_id = request.url.split('/')[-1]
            token = get_jwt_identity()

            # check authority
            if not service_video_op_auth_modify(token, user_id):
                raise RouteError(ErrorCode.ROUTE_TOKEN_REQUIRED)

            kw['video_id'] = video_id
            kw['user_id'] = user_id
            process_result = service_video_op_update_process(conf=conf, **kw)

            return util_serializer_api_response(
                200, body=process_result,
                msg="Successfully update video process")

        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)

    @jwt_required
    def delete(self, video_id, user_id, conf=config['default']):
        """
            Delete a video watching process
        """

        try:
            video_id = request.url.split('/')[-3]
            user_id = request.url.split('/')[-1]
            token = get_jwt_identity()

            # check authority
            if not service_video_op_auth_modify(token, user_id):
                raise RouteError(ErrorCode.ROUTE_TOKEN_REQUIRED)

            process_result = service_video_op_cancel_process(
                conf=conf, video_id=video_id, user_id=user_id)

            return util_serializer_api_response(
                200, body=process_result,
                msg="Successfully delete video process")

        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)


@video.route('/<string:video_id>/like/<string:user_id>',
             methods=['DELETE', 'POST'])
@video.param('video_id', 'Video ID')
@video.param('user_id', 'User ID')
@video.response(200, 'Successful operation', like_response)
@video.response(400, 'Invalid video ID or user ID', general_response)
@video.response(404, 'Video or user not found', general_response)
@video.response(405, 'Method not allowed', general_response)
@video.response(500, 'Internal server error', general_response)
class VideoVideoIdLikeUserId(Resource):

    @jwt_required
    def post(self, video_id, user_id, conf=config['default']):
        """
            Post a like by specified user and video
        """

        try:
            video_id = request.url.split('/')[-3]
            user_id = request.url.split('/')[-1]
            token = get_jwt_identity()

            # check authority
            if not service_video_op_auth_post(token, user_id, video_id):
                raise RouteError(ErrorCode.ROUTE_TOKEN_REQUIRED)

            like_result = service_video_op_add_like(
                conf=conf, video_id=video_id, user_id=user_id)

            return util_serializer_api_response(
                200, body=like_result, msg="Successfully post a like")

        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)

    @jwt_required
    def delete(self, video_id, user_id, conf=config['default']):
        """
            Undo a like by specified user and video
        """

        try:
            video_id = request.url.split('/')[-3]
            user_id = request.url.split('/')[-1]
            token = get_jwt_identity()

            # check authority
            if not service_video_op_auth_modify(token, user_id):
                raise RouteError(ErrorCode.ROUTE_TOKEN_REQUIRED)

            like_result = service_video_op_cancel_like(
                conf=conf, user_id=user_id, video_id=video_id)

            return util_serializer_api_response(
                200, body=like_result, msg="Successfully cancel a like")

        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)


@video.route('/<string:video_id>/dislike/<string:user_id>',
             methods=['DELETE', 'POST'])
@video.param('video_id', 'Video ID')
@video.param('user_id', 'User ID')
@video.response(200, 'Successful operation', dislike_response)
@video.response(400, 'Invalid video ID or user ID', general_response)
@video.response(404, 'Video or user not found', general_response)
@video.response(405, 'Method not allowed', general_response)
@video.response(500, 'Internal server error', general_response)
class VideoVideoIdDislikeUserId(Resource):

    @jwt_required
    def post(self, video_id, user_id, conf=config['default']):
        """
            Post a dislike by specified user and video
        """

        try:
            video_id = request.url.split('/')[-3]
            user_id = request.url.split('/')[-1]
            token = get_jwt_identity()

            # check authority
            if not service_video_op_auth_post(token, user_id, video_id):
                raise RouteError(ErrorCode.ROUTE_TOKEN_REQUIRED)

            dislike_result = service_video_op_add_dislike(
                conf=conf, video_id=video_id, user_id=user_id)

            return util_serializer_api_response(
                200, body=dislike_result, msg="Successfully post a dislike")

        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)

    @jwt_required
    def delete(self, video_id, user_id, conf=config['default']):
        """
            Undo a dislike by specified user and video
        """

        try:
            video_id = request.url.split('/')[-3]
            user_id = request.url.split('/')[-1]
            token = get_jwt_identity()

            # check authority
            if not service_video_op_auth_modify(token, user_id):
                raise RouteError(ErrorCode.ROUTE_TOKEN_REQUIRED)

            dislike_result = service_video_op_cancel_dislike(
                conf=conf, video_id=video_id, user_id=user_id)

            return util_serializer_api_response(
                200, body=dislike_result, msg="Successfully cancel a dislike")

        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)


@video.route('/<string:video_id>/star/<string:user_id>',
             methods=['DELETE', 'POST'])
@video.param('video_id', 'Video ID')
@video.param('user_id', 'User ID')
@video.response(200, 'Successful operation', star_response)
@video.response(400, 'Invalid video ID or user ID', general_response)
@video.response(404, 'Video or user not found', general_response)
@video.response(405, 'Method not allowed', general_response)
@video.response(500, 'Internal server error', general_response)
class VideoVideoIdStarUserId(Resource):

    @jwt_required
    def post(self, video_id, user_id, conf=config['default']):
        """
            Post a star by specified user and video
        """

        try:
            video_id = request.url.split('/')[-3]
            user_id = request.url.split('/')[-1]
            token = get_jwt_identity()

            # check authority
            if not service_video_op_auth_post(token, user_id, video_id):
                raise RouteError(ErrorCode.ROUTE_TOKEN_REQUIRED)

            star_result = service_video_op_add_star(
                conf=conf, video_id=video_id, user_id=user_id)

            return util_serializer_api_response(
                200, body=star_result, msg="Successfully add a star")

        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)

    @jwt_required
    def delete(self, video_id, user_id, conf=config['default']):
        """
            Undo a star by specified user and video
        """

        try:
            video_id = request.url.split('/')[-3]
            user_id = request.url.split('/')[-1]
            token = get_jwt_identity()

            # check authority
            if not service_video_op_auth_modify(token, user_id):
                raise RouteError(ErrorCode.ROUTE_TOKEN_REQUIRED)

            star_result = service_video_op_cancel_star(
                conf=conf, user_id=user_id, video_id=video_id)

            return util_serializer_api_response(
                200, body=star_result, msg="Successfully cancel a star")

        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)

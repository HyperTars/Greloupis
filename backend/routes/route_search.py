# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_optional
from flask_restx import Resource, fields, Namespace
from .route_user import user_info, general_response
from .route_video import video_info
from service.service_search import service_search_user, \
    service_search_video, service_search_hide_video, \
    service_search_hide_user
from utils.util_serializer import util_serializer_request, \
    util_serializer_api_response
from utils.util_error_handler import util_error_handler
from models.model_errors import ErrorCode, RouteError, ServiceError, MongoError

# from flask import Flask, g, Blueprint
# from flask_restx import Api, marshal_with, reqparse
# import json

search = Namespace('search', description='Search APIs')

user_response_list = search.model(name='ApiResponseWithUserList', model={
    'code': fields.String,
    'body': fields.List(fields.Nested(user_info))
})

video_response_list = search.model(name='ApiResponseWithVideoList', model={
    'code': fields.String,
    'body': fields.List(fields.Nested(video_info))
})


@search.route('/user', methods=['GET'])
@search.param('keyword', 'Searching keyword')
@search.response(200, 'Successfully got user search results.',
                 user_response_list)
@search.response(400, 'Bad request.', general_response)
@search.response(500, 'Internal server error.', general_response)
class RouteSearchUser(Resource):
    @search.doc(responses={200: 'Successfully got user search results.'})
    def get(self):
        """
            Search users by keyword
        """
        # TODO
        print("get user name", get_jwt_identity())
        try:
            req_dict = util_serializer_request(request.args)

            if 'keyword' not in req_dict:
                raise RouteError(ErrorCode.ROUTE_INVALID_REQUEST_PARAM)
            if 'param' not in req_dict:
                param = 'all'
            else:
                param = req_dict['param']

            if param == 'all':
                search_result = service_search_user(
                    name=req_dict['keyword'], ignore_case=True)
                search_result.extend(service_search_user(
                    email=req_dict['keyword'], ignore_case=True))
                search_result.extend(service_search_user(
                    first_name=req_dict['keyword'],
                    ignore_case=True))
                search_result.extend(service_search_user(
                    last_name=req_dict['keyword'],
                    ignore_case=True))
                search_result.extend(service_search_user(
                    phone=req_dict['keyword'], ignore_case=True))
                search_result.extend(service_search_user(
                    street1=req_dict['keyword'], ignore_case=True))
                search_result.extend(service_search_user(
                    street2=req_dict['keyword'], ignore_case=True))
                search_result.extend(service_search_user(
                    city=req_dict['keyword'], ignore_case=True))
                search_result.extend(service_search_user(
                    state=req_dict['keyword'], ignore_case=True))
                search_result.extend(service_search_user(
                    country=req_dict['keyword'],
                    ignore_case=True))
                search_result.extend(service_search_user(
                    zip=req_dict['keyword'], ignore_case=True))
                search_result.extend(service_search_user(
                    status=req_dict['keyword'], ignore_case=True))
                search_result = list(
                    {v['user_id']: v for v in search_result}.values())
            elif param == 'name' or param == 'user_name':
                search_result = service_search_user(
                    name=req_dict['keyword'], ignore_case=True)
            elif param == 'email' or param == 'user_email':
                search_result = service_search_user(
                    email=req_dict['keyword'], ignore_case=True)
            elif param == 'first_name' or param == 'user_first_name':
                search_result = service_search_user(
                    first_name=req_dict['keyword'],
                    ignore_case=True)
            elif param == 'last_name' or param == 'user_last_name':
                search_result = service_search_user(
                    last_name=req_dict['keyword'], ignore_case=True)
            elif param == 'phone' or param == 'user_phone':
                search_result = service_search_user(
                    phone=req_dict['keyword'], ignore_case=True)
            elif param == 'street1' or param == 'user_street1':
                search_result = service_search_user(
                    street1=req_dict['keyword'], ignore_case=True)
            elif param == 'street2' or param == 'user_street2':
                search_result = service_search_user(
                    street2=req_dict['keyword'], ignore_case=True)
            elif param == 'city' or param == 'user_city':
                search_result = service_search_user(
                    city=req_dict['keyword'], ignore_case=True)
            elif param == 'state' or param == 'user_state':
                search_result = service_search_user(
                    state=req_dict['keyword'], ignore_case=True)
            elif param == 'country' or param == 'user_country':
                search_result = service_search_user(
                    country=req_dict['keyword'], ignore_case=True)
            elif param == 'zip' or param == 'user_zip':
                search_result = service_search_user(
                    zip=req_dict['keyword'], ignore_case=True)
            elif param == 'status' or param == 'user_status':
                search_result = service_search_user(
                    status=req_dict['keyword'], ignore_case=True)
            else:
                raise RouteError(ErrorCode.ROUTE_INVALID_REQUEST_PARAM)

            return util_serializer_api_response(
                200,
                body=service_search_hide_user(
                    get_jwt_identity(), search_result),
                msg="Search user successfully")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)


@search.route('/video', methods=['GET'])
@search.param('keyword', 'Searching keyword')
@search.param('param', 'Searching param')
@search.response(200, 'Successfully got video search results.',
                 video_response_list)
@search.response(400, 'Bad request.', general_response)
@search.response(500, 'Internal server error.', general_response)
class RouteSearchVideo(Resource):
    @search.doc(responses={200: 'Successfully got video search results.'})
    @jwt_optional
    def get(self):
        """
            Search videos by keyword
        """
        try:
            req_dict = util_serializer_request(request.args)
            if 'keyword' not in req_dict:
                raise RouteError(ErrorCode.ROUTE_INVALID_REQUEST_PARAM)
            if 'param' not in req_dict:
                param = 'all'
            else:
                param = req_dict['param']

            if param == 'all':
                search_result = service_search_video(
                    title=req_dict['keyword'], ignore_case=True,
                    slice=True)
                search_result.extend(service_search_video(
                    channel=req_dict['keyword'], ignore_case=True,
                    slice=True))
                search_result.extend(service_search_video(
                    description=req_dict['keyword'],
                    ignore_case=True, slice=True))
                search_result.extend(service_search_video(
                    category=req_dict['keyword'], ignore_case=True))
                search_result.extend(service_search_video(
                    tag=req_dict['keyword'], ignore_case=True))
                search_result = list(
                    {v['video_id']: v for v in search_result}.values())
            elif param == 'title' or param == 'video_title':
                search_result = service_search_video(
                    title=req_dict['keyword'], ignore_case=True,
                    slice=True)
            elif param == 'channel' or param == 'video_channel':
                search_result = service_search_video(
                    channel=req_dict['keyword'], ignore_case=True,
                    slice=True)
            elif param == 'description' or param == 'video_descripton':
                search_result = service_search_video(
                    description=req_dict['keyword'],
                    ignore_case=True, slice=True)
            elif param == 'category' or param == 'video_category':
                search_result = service_search_video(
                    category=req_dict['keyword'], ignore_case=True)
            elif param == 'tag' or param == 'video_tag':
                search_result = service_search_video(
                    tag=req_dict['keyword'], ignore_case=True)
            else:
                raise RouteError(ErrorCode.ROUTE_INVALID_REQUEST_PARAM)
            return util_serializer_api_response(
                200,
                body=service_search_hide_video(
                    get_jwt_identity(), search_result),
                msg="Search video successfully")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)


@search.route('/video/top', methods=['GET'])
@search.param('keyword', 'Searching keyword')
@search.response(200, 'Successfully got video search results.',
                 video_response_list)
@search.response(400, 'Bad request.', general_response)
@search.response(500, 'Internal server error.', general_response)
class RouteSearchTopVideos(Resource):
    @search.doc(responses={200: 'Successfully got video search results.'})
    def get(self):

        try:
            req_dict = util_serializer_request(request.args)
            if 'keyword' not in req_dict:
                raise RouteError(ErrorCode.ROUTE_INVALID_REQUEST_PARAM)
            if req_dict['keyword'] == 'video_upload_time' or \
                    req_dict['keyword'] == 'upload_time' or \
                    req_dict['keyword'] == 'time':
                keyword = 'video_upload_time'
            elif req_dict['keyword'] == 'video_like' or \
                    req_dict['keyword'] == 'video_likes' or \
                    req_dict['keyword'] == 'like' or \
                    req_dict['keyword'] == 'likes':
                keyword = 'video_like'
            elif req_dict['keyword'] == 'video_share' or \
                    req_dict['keyword'] == 'video_shares' or \
                    req_dict['keyword'] == 'share' or \
                    req_dict['keyword'] == 'shares':
                keyword = 'video_share'
            elif req_dict['keyword'] == 'video_star' or \
                    req_dict['keyword'] == 'video_stars' or \
                    req_dict['keyword'] == 'star' or \
                    req_dict['keyword'] == 'stars':
                keyword = 'video_star'
            elif req_dict['keyword'] == 'video_view' or \
                    req_dict['keyword'] == 'video_views' or \
                    req_dict['keyword'] == 'view' or \
                    req_dict['keyword'] == 'views':
                keyword = 'video_view'
            elif req_dict['keyword'] == 'video_duration' or \
                    req_dict['keyword'] == 'duration':
                keyword = 'video_duration'
            else:
                raise RouteError(ErrorCode.ROUTE_INVALID_REQUEST_PARAM)
            search_dict = [
                {
                    "$sort":
                        {
                            keyword: -1
                        }
                },
                {
                    "$limit": 100
                }
            ]
            search_result = service_search_video(
                aggregate=True, search_dict=search_dict)
            if keyword == 'video_upload_time':
                search_result.reverse()
            return util_serializer_api_response(
                200,
                body=service_search_hide_video(
                    get_jwt_identity(), search_result),
                msg="Search video successfully")
        except (ServiceError, MongoError, RouteError, Exception) as e:
            return util_error_handler(e)

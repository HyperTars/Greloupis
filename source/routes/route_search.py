# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import Flask, request, g, Blueprint
from flask_restx import Resource, Api, fields, marshal_with, reqparse, Namespace
import json

from .route_user import user_info, general_response
from .route_video import video_info, general_response
from source.service.service_search import *
from source.config import *
from source.utils.util_serializer import *

import logging

search = Namespace('search', description='Search APIs')

user_response_list = search.model(name='ApiResponseWithUserList', model={
    'code': fields.String,
    'body': fields.List(fields.Nested(user_info))
})

video_response_list = search.model(name='ApiResponseWithVideoList', model={
    'code': fields.String,
    'body': fields.List(fields.Nested(video_info))
})


@search.route('/video')
@search.param('keyword', 'Searching keyword')
@search.response(200, 'Successfully got video search results.', video_response_list)
@search.response(400, 'Bad request.', general_response)
@search.response(500, 'Internal server error.', general_response)
class RouteSearchVideo(Resource):
    @search.doc(responses={200: 'Successfully got video search results.'})
    def get(self):
        """
            Search videos by keyword
        """
        req_dict = util_serializer_request(request.args)
        if 'keyword' not in req_dict:
            return {ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_code():
                    ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg()}, 200, None

        # search_result_dict = search_video(title=keyword, ignore_case=True, format="dict", exact=True)
        search_result_json = service_search_video(conf=config['default'], title=req_dict['keyword'],
                                                  ignore_case=True, format="json", slice=True)
        return util_serializer_api_response(search_result_json, 200)


@search.route('/user')
@search.param('keyword', 'Searching keyword')
@search.response(200, 'Successfully got user search results.', user_response_list)
@search.response(400, 'Bad request.', general_response)
@search.response(500, 'Internal server error.', general_response)
class RouteSearchUser(Resource):
    @search.doc(responses={200: 'Successfully got user search results.'})
    def get(self):
        """
            Search users by keyword
        """
        req_dict = util_serializer_request(request.args)
        # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # logging.debug(type(request.args))

        if 'keyword' not in req_dict:
            return {ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_code():
                    ErrorCode.ROUTE_INVALID_REQUEST_PARAM.get_msg()}, 200, None

        search_result_json = service_search_user(conf=config['default'], name=req_dict['keyword'],
                                                 ignore_case=True, exact=False, format="json")

        # search_result_dict = search_user(email=keyword, ignore_case=True, format="dict", exact=True)
        return util_serializer_api_response(search_result_json, 200)

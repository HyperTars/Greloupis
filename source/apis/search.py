# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import Flask, request, g, Blueprint
from flask_restx import Resource, Api, fields, marshal_with, reqparse, Namespace
import json

from .user import user_info, general_response
from .video import video_info, general_response
from source.service.service_search import *

search = Namespace('search', description='Search APIs')

user_response_list = search.model(name='ApiResponseWithUserList', model={
    'code': fields.String,
    'body': fields.List(fields.Nested(user_info))
})

video_response_list = search.model(name='ApiResponseWithVideoList', model={
    'code': fields.String,
    'body': fields.List(fields.Nested(video_info))
})

@search.route('/video?q=<string:keyword>')
@search.param('keyword', 'Searching keyword')
@search.response(200, 'Successfully got video search results.', video_response_list)
@search.response(400, 'Bad request.', general_response)
@search.response(500, 'Internal server error.', general_response)
class SearchVideo(Resource):
    def get(self, keyword):
        """
            Search videos by keyword
        """
        search_result_dict = search_video(title=keyword, type="dict")
        search_result_json = search_video(title=keyword, type="json")
        print(search_result_json)
        return {}, 200, None


@search.route('/user?q=<string:keyword>')
@search.param('keyword', 'Searching keyword')
@search.response(200, 'Successfully got user search results.', user_response_list)
@search.response(400, 'Bad request.', general_response)
@search.response(500, 'Internal server error.', general_response)
class SearchUser(Resource):
    @search.doc(responses={200: 'Successfully got user search results.'})
    def get(self, keyword):
        search_result_dict = search_user(name=keyword, ignore_case=True, type="dict")
        search_result_json = search_user(email=keyword, ignore_case=True, type="json", exact=True)
        print(search_result_json)
        return {}, 200, search_result_json
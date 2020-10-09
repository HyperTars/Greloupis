# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import Flask, request, g, Blueprint
from flask_restx import Resource, Api, fields, marshal_with, reqparse, Namespace
import json

search = Namespace('search', description='Search APIs')

general_response = search.model(name='ApiResponse', model={
    'code': fields.String(required=True),
    'body': fields.String(required=True)
})

general_response_list = search.model(name='ApiResponseWithList', model={
    'code': fields.String(required=True),
    'body': fields.List(fields.String(required=True))
})

@search.route('/video?q=<string:keyword>')
@search.param('keyword', 'Searching keyword')
@search.response(200, 'Successfully got video search results.', general_response_list)
@search.response(400, 'Bad request.', general_response)
@search.response(500, 'Internal server error.', general_response)
class SearchVideo(Resource):
    def get(self, keyword):
        """
            Search videos by keyword
        """
        search_result = []
        return {}, 200, None


@search.route('/user?q=<string:keyword>')
@search.param('keyword', 'Searching keyword')
@search.response(200, 'Successfully got user search results.', general_response_list)
@search.response(400, 'Bad request.', general_response)
@search.response(500, 'Internal server error.', general_response)
class SearchUser(Resource):
    @search.doc(responses={200: 'Successfully got user search results.'})
    def get(self, keyword):
        """
            Search users by keyword
        """
        search_result = []
        return {}, 200, None
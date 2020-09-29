from flask import Flask, request
from flask_restx import Resource, Api, fields, marshal_with, reqparse, Namespace
from __future__ import absolute_import, print_function
from flask import request, g
import json

parser = reqparse.RequestParser()
parser.add_argument('keyword', type=str, help='searching keyword')
args = parser.parse_args()


'''
 @route     GET /search/video/<string:keyword>
 @desc      Search videos by keyword
 @access    Public
'''
@api.route('/api/search/video/<string:keyword>')
@api.response(400, 'Bad request.')
@api.response(500, 'Internal server error.')
class SearchVideo(Resource):
    @api.expect(parser)
    @api.doc(responses={200: 'Successfully got video search results.'})
    def get(self, keyword):
        search_result = []
        return {}, 200, None


'''
 @route     GET /search/user/<string:keyword>
 @desc      Search users by keyword
 @access    Public
'''
@api.route('api/search/user')
@api.response(400, 'Bad request.')
@api.response(500, 'Internal server error.')
class SearchUser(Resource):
    @api.expect(parser)
    @api.doc(responses={200: 'Successfully got user search results.'})
    def get(self, keyword):
        search_result = []
        return {}, 200, None
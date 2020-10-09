# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import Flask, request, g, Blueprint
from flask_restx import Resource, Api, fields, marshal_with, reqparse, Namespace
import json

search = Namespace('search', description='Search APIs')

'''
 @route     GET /search/video?q=<string:keyword>
 @desc      Search videos by keyword
 @access    Public
'''

@search.route('/video?q=<string:keyword>')
@search.response(400, 'Bad request.')
@search.response(500, 'Internal server error.')
class SearchVideo(Resource):
    @search.doc(responses={200: 'Successfully got video search results.'})
    def get(self, keyword):
        search_result = []
        return {}, 200, None


'''
 @route     GET /search/user?q=<string:keyword>
 @desc      Search users by keyword
 @access    Public
'''
@search.route('/user?q=<string:keyword>')
@search.response(400, 'Bad request.')
@search.response(500, 'Internal server error.')
class SearchUser(Resource):
    @search.doc(responses={200: 'Successfully got user search results.'})
    def get(self, keyword):
        search_result = []
        return {}, 200, None
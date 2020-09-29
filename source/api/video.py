# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import Flask, request, g
from flask_restx import Resource, Api, fields, marshal_with, reqparse, Namespace
import json

@api.route('/video')
@api.response(200, 'Successful operation')
@api.response(400, 'Invalid video information')
@api.response(405, 'Method not allowed')
@api.response(500, 'Internal server error')
class Video(Resource):
    """
        User upload a video
    """
    @api.expect(video)
    def post(self):
        return {}, 200, None

@api.route('/video/<string:video_id>')
@api.response(200, 'Successful operation')
@api.response(400, 'Invalid video information')
@api.response(404, 'User not found')
@api.response(500, 'Internal server error')
class VideoVideoId(Resource):
    """
        Get video information by id
    """
    def get(self, video_id):
        return {}, 200, None

    """
        Update video information by id
    """
    @api.response(405, 'Method not allowed')
    @api.expect(video)
    def put(self, video_id):
        return {}, 200, None

    """
        Delete video by id
    """
    def delete(self, video_id):
        return {}, 200, None
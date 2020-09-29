# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas


class VideoVideoIdDislikeUserId(Resource):

    def post(self, video_id, user_id):

        return {}, 200, None

    def delete(self, video_id, user_id):

        return {}, 200, None
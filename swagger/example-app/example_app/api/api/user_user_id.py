# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas


class UserUserId(Resource):

    def get(self, user_id):

        return {}, 200, None

    def put(self, user_id):
        print(g.json)

        return {}, 200, None

    def delete(self, user_id):

        return {}, 200, None
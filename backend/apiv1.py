# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import Blueprint
from flask_restx import Api

# from source.routes.route_auth import auth
from routes.route_user import user
from routes.route_video import video
from routes.route_search import search

blueprint = Blueprint('api', __name__, url_prefix='/')
api = Api(blueprint)

api.add_namespace(user)
api.add_namespace(video)
api.add_namespace(search)

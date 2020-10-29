# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import Blueprint
from flask_restx import Api
from source.settings import config

# from source.routes.route_auth import auth
from source.routes.route_user import user
from source.routes.route_video import video
from source.routes.route_search import search

conf = config['default']
blueprint = Blueprint('api', __name__, url_prefix='/')
api = Api(blueprint)

# api.add_namespace(auth)
api.add_namespace(user)
api.add_namespace(video)
api.add_namespace(search)

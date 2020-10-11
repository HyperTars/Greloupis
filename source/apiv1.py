# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import Flask, request, g, Blueprint
from flask_restx import Resource, Api, fields, marshal_with, reqparse, Namespace
import json

from source.routes.route_user import user
from source.routes.route_video import video
from source.routes.route_search import search

blueprint = Blueprint('api', __name__, url_prefix='/')
api = Api(blueprint)

api.add_namespace(user)
api.add_namespace(video)
api.add_namespace(search)
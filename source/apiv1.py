# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import Flask, request, g, Blueprint
from flask_restx import Resource, Api, fields, marshal_with, reqparse, Namespace
import json

from apis.user import user
from apis.video import video
from apis.search import search

blueprint = Blueprint('api', __name__, url_prefix='/')
api = Api(blueprint)

api.add_namespace(user)
api.add_namespace(video)
api.add_namespace(search)
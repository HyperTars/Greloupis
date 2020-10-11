# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import Flask, request, g
from flask_restx import Resource, Api, fields, marshal_with, reqparse, Namespace
from source.apiv1 import blueprint
import json

app = Flask(__name__)

if __name__ == '__main__':
    app.register_blueprint(blueprint)
    app.run(debug=True)

# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import Flask, request
from apiv1 import blueprint
from settings import config
from flask_cors import CORS
import os

# from source.utils.util_request_filter import *
# from flask import request, redirect, session

app = Flask(__name__)
app.config.from_object(config['test'])
app.register_blueprint(blueprint)
# CORS(app, resources={r'/*': {'origins': config['test'].FRONTEND}},
#      supports_credentials=True)
"""
@app.before_request
def before_request():
    util_request_filter_xss()
    util_request_filter_malicious_ip()

    TODO: redesign paths
    if request.path == "/video" or request.path == "/search":
        return None
    if not session.get("user_id"):
        return redirect("/user/login")
"""


@app.after_request
def add_cors_headers(response):
    r = request.referrer[:-1]
    if r in config['test'].FRONTEND:
        response.headers.add('Access-Control-Allow-Origin', r)
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Headers', 'Cache-Control')
        response.headers.add('Access-Control-Allow-Headers',
                             'X-Requested-With')
        response.headers.add('Access-Control-Allow-Headers', 'Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, OPTIONS, PUT, DELETE')
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', '5000'))

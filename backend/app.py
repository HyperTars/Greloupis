# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import yaml
from flask import Flask, request
from flask_jwt_extended import JWTManager

from apiv1 import blueprint
from routes.route_user import blacklist
from settings import config
import os
import logging.config
from pathlib import Path
from db.mongo import init_db
# from source.utils.util_request_filter import *
# from flask import request, redirect, session
from utils.util_jwt import util_get_formated_response

app = Flask(__name__)
app.config.from_object(config['default'])
app.register_blueprint(blueprint)
with app.app_context():
    init_db()

with open('configs/logging.yml', 'r') as f:
    Path("logs").mkdir(parents=True, exist_ok=True)
    conf = yaml.safe_load(f.read())
    logging.config.dictConfig(conf)

# CORS(app, resources={r'/*': {'origins': config['test'].FRONTEND}},
#      supports_credentials=True)
jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@jwt.expired_token_loader
def expired_token_callback():
    return util_get_formated_response(code=-10000,
                                      msg='The token has expired')


@jwt.revoked_token_loader
def revoked_token_callback():
    return util_get_formated_response(code=-10000,
                                      msg='The token has been revoked')


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
    if request is None or request.referrer is None:
        return response

    r = request.referrer[:-1]
    if r in app.config['FRONTEND']:
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

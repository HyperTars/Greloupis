# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import Flask, render_template
from apiv1 import blueprint
from settings import config
from flask_cors import CORS
import os

# from source.utils.util_request_filter import *
# from flask import request, redirect, session

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': config['test'].FRONTEND}},
     supports_credentials=True)


@app.route("/")
def index():
    return render_template('index.html')


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

if __name__ == '__main__':
    app.config.from_object(config['test'])
    app.register_blueprint(blueprint)
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', '5000'))

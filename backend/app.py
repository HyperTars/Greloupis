# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import Flask
from apiv1 import blueprint
from settings import config
from flask_cors import CORS
import os
# from source.utils.util_request_filter import *
# from flask import request, redirect, session

frontend_conf = {
    'ORIGINS': [
        'http://localhost:3000',  # React
        'http://127.0.0.1:3000',  # React
    ],
}

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': frontend_conf['ORIGINS']}},
     supports_credentials=True)

# @app.route("/")
# def index():
#     APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     print(APP_PATH)
#     TEMPLATE_PATH = os.path.join(APP_PATH, 'source/templates/')
#     return render_template('index.html')
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

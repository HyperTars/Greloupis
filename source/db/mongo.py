# dnspython-2.0.0

from flask import Flask
from flask_mongoengine import MongoEngine
from source.configs import *


def get_db(conf=config['default']):
    app = Flask(__name__)
    app.config['MONGODB_SETTINGS'] = conf.MONGODB_SETTINGS
    db = MongoEngine(app)
    return db

# dnspython-2.0.0

from flask import Flask
from flask_mongoengine import MongoEngine
from source.config import config, DevConfig, ProdConfig, TestConfig


def get_db(Config):
    app = Flask(__name__)
    app.config['MONGODB_SETTINGS'] = Config.MONGODB_SETTINGS
    db = MongoEngine(app)
    return db

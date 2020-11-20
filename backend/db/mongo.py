# dnspython-2.0.0

from flask import Flask, current_app
from flask_mongoengine import MongoEngine
from settings import config


def get_db():
    db_app = Flask(__name__)
    db_app.config = current_app.config
    db = MongoEngine(db_app)
    return db

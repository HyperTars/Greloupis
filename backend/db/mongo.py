from flask import Flask, current_app
from flask_mongoengine import MongoEngine
from mongoengine.connection import disconnect


def init_db():
    disconnect(alias='default')
    db_app = Flask(__name__)
    db_app.config = current_app.config
    db = MongoEngine(db_app)
    return db

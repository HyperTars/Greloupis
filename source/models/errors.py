from flask import Flask
from flask_mongoengine import MongoEngine
from flask_mongoengine.wtf.fields import DictField, DateTime
from mongoengine.fields import DateTimeField

# Error Model
class Error(Document):
    call = DictField(required=True)
    response = DictField(required=True)
    date = DateTimeField(default=datetime.now(), required=True)
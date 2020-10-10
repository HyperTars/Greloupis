from flask_mongoengine import MongoEngine
import datetime

db = MongoEngine


# Error Model
class Error(db.Document):
    call = db.DictField(required=True)
    response = db.DictField(required=True)
    date = db.DateTimeField(default=datetime.now(), required=True)

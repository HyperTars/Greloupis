# Flask-pymongo-2.3.0
# PyMongo-3.11
from flask_pymongo import pymongo

MONGO_ENDPOINT = "mongodb+srv://devops:DevOps@mongodbcluster.v4vtj.mongodb.net/online_video_platform?retryWrites=true&w=majority"
MONGO_DATABASE = "online_video_platform"

MONGO_TABLE_USER = "users"
MONGO_TABLE_VIDEO = "videos"
MONGO_TABLE_HISTORY = "histories"
MONGO_TABLE_REVIEW = "reviews"

client = pymongo.MongoClient(MONGO_ENDPOINT)
db = client.get_database(MONGO_DATABASE)

user = pymongo.collection.Collection(db, MONGO_TABLE_USER)
video = pymongo.collection.Collection(db, MONGO_TABLE_VIDEO)
history = pymongo.collection.Collection(db, MONGO_TABLE_HISTORY)
review = pymongo.collection.Collection(db, MONGO_TABLE_REVIEW)


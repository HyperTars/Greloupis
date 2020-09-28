# Flask-pymongo-2.3.0
# PyMongo-3.11
# dnspython-2.0.0


from flask_pymongo import pymongo

MONGO_ENDPOINT = "mongodb+srv://devops:DevOps@mongodbcluster.v4vtj.mongodb.net/online_video_platform?retryWrites=true&w=majority"
MONGO_DATABASE = "online_video_platform"

MONGO_TABLE_USER = "users"
MONGO_TABLE_VIDEO = "videos"
MONGO_TABLE_HISTORY = "histories"
MONGO_TABLE_REVIEW = "reviews"
MONGO_TABLE_FOLLOW = "follow"
MONGO_TABLE_COMMENT = "comments"
MONGO_TABLE_LIKE = "likes"
MONGO_TABLE_DISLIKE = "dislikes"
MONGO_TABLE_STAR = "stars"

client = pymongo.MongoClient(MONGO_ENDPOINT)
db = client.get_database(MONGO_DATABASE)

user = pymongo.collection.Collection(db, MONGO_TABLE_USER)
video = pymongo.collection.Collection(db, MONGO_TABLE_VIDEO)

# Lazy loading
history = pymongo.collection.Collection(db, MONGO_TABLE_HISTORY)
review = pymongo.collection.Collection(db, MONGO_TABLE_REVIEW)
follow = pymongo.collection.Collection(db, MONGO_TABLE_FOLLOW)
comment = pymongo.collection.Collection(db, MONGO_TABLE_COMMENT)
like = pymongo.collection.Collection(db, MONGO_TABLE_LIKE)
dislike = pymongo.collection.Collection(db, MONGO_TABLE_DISLIKE)
star = pymongo.collection.Collection(db, MONGO_TABLE_STAR)

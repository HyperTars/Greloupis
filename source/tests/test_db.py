# Flask-pymongo-2.3.0
# PyMongo-3.11
# dnspython-2.0.0

from flask import Flask
from flask_mongoengine import MongoEngine
from wtforms.fields import FieldList, FormField
from dateutil.parser import parse
from time import sleep

MONGO_ENDPOINT = "mongodb+srv://devops:DevOps@mongodbcluster.v4vtj.mongodb.net/online_video_platform?retryWrites=true&w=majority"
MONGO_DATABASE = "online_video_platform"

MONGO_TABLE_USER = "user"
MONGO_TABLE_VIDEO = "video"
MONGO_TABLE_VIDEO_OP = "video_op"

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': MONGO_DATABASE,
    'host': MONGO_ENDPOINT
}

db = MongoEngine(app)


class VideoOp(db.Document):
    _id = db.StringField(max_length=100, required=True)
    user_id = db.StringField(max_length=100, required=True)
    video_id = db.StringField(max_length=100, required=True)
    process = db.IntField(required=False, default=0)
    comment = db.StringField(max_length=1000, required=True)
    like = db.BooleanField(default=False)
    dislike = db.BooleanField(default=False)
    star = db.BooleanField(default=False)
    history_date = db.DateTimeField(required=False)
    comment_date = db.DateTimeField(required=False)
    like_date = db.DateTimeField(required=False)
    dislike_date = db.DateTimeField(required=False)
    star_date = db.DateTimeField(required=False)
    
    def to_dict(self):
        video_op_dict = {}
        video_op_dict['video_op_id'] = str(self._id)
        video_op_dict['user_id'] = self.user_id
        video_op_dict['video_id'] = self.video_id
        video_op_dict['process'] = self.process
        video_op_dict['comment'] = self.comment
        video_op_dict['like'] = self.like
        video_op_dict['dislike'] = self.dislike
        video_op_dict['star'] = self.star
        video_op_dict['history_date'] = self.history_date
        video_op_dict['comment_date'] = self.comment_date
        video_op_dict['like_date'] = self.like_date
        video_op_dict['dislike_date'] = self.dislike_date
        video_op_dict['star_date'] = self.star_date
        return video_op_dict

class UserDetail(db.EmbeddedDocument):
    first_name = db.StringField(max_length=50, required=True)
    last_name = db.StringField(max_length=50, required=True)
    phone = db.StringField(max_length=50, required=True, unique=True)
    street1 = db.StringField(max_length=100)
    street2 = db.StringField(max_length=100)
    city = db.StringField(max_length=50)
    state = db.StringField(max_length=50)
    country = db.StringField(max_length=50)
    zip = db.StringField(max_length=20)


class Thumbnail(db.EmbeddedDocument):
    thumbnail_uri = db.StringField(max_length=200, required=True)
    thumbnail_type = db.StringField(max_length=50, required=True)


class LoginDetail(db.EmbeddedDocument):
    login_ip = db.StringField(max_length=50, required=True)
    login_time = db.DateTimeField()


class User(db.Document):
    _id = db.StringField()
    user_email = db.StringField(max_length=50, required=True, unique=True)
    user_name = db.StringField(max_length=60, required=True, unique=True)
    user_password = db.StringField(max_length=200, required=True)
    user_detail = db.EmbeddedDocumentField('UserDetail', required=True)
    user_status = db.StringField(max_length=50, required=True)
    user_thumbnail = db.EmbeddedDocumentField('Thumbnail', required=True)
    user_reg_date = db.DateTimeField(required=True)
    user_recent_login = db.ListField(db.EmbeddedDocumentField('LoginDetail'))
    user_following = db.ListField(db.StringField())
    user_follower = db.ListField(db.StringField())

tu_detail = UserDetail(first_name="test_user", last_name="test_user", phone="+1xxxxxx", street1="str1", street2="str2", city="cty", state="stt", country="ctry", zip="zip")
tu_thumbnail = Thumbnail(thumbnail_uri="test_uri", thumbnail_type="test_type")
tu_login = LoginDetail(login_ip="1.1.1.1", login_time=parse("20201008153008"))
tu = User(user_email="xx.gmail.com", user_name="test_user", user_password="askdkj091", user_detail=tu_detail, user_status="active", user_thumbnail=tu_thumbnail, user_reg_date=parse("20201008141231"), user_recent_login=[tu_login], user_following=[], user_follower=[])
# tu.save()

print("test: get video_op")
vo = VideoOp.objects()
for v in vo:
    print(v.to_dict())

print("test: get user")
usr = User()
usr = User.objects()
len(usr)
for u in usr:
    print(u._id)


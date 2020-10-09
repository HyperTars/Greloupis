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

    def to_dict(self):
        user_dict = {}
        user_detail_dict = {}
        user_thumbnail_dict = {}
        user_recent_login_array = []
        user_following_array = []
        user_follower_array = []

        user_detail_dict['user_first_name'] = self.user_detail.first_name or None
        user_detail_dict['user_last_name'] = self.user_detail.last_name or None
        user_detail_dict['user_phone'] = self.user_detail.phone or None
        user_detail_dict['user_street1'] = self.user_detail.street1 or None
        user_detail_dict['user_street2'] = self.user_detail.street2 or None
        user_detail_dict['user_city'] = self.user_detail.city or None
        user_detail_dict['user_state'] = self.user_detail.state or None
        user_detail_dict['user_country'] = self.user_detail.country or None
        user_detail_dict['user_zip'] = self.user_detail.zip or None

        user_thumbnail_dict['user_thumbnail_uri'] = self.user_thumbnail.thumbnail_uri or None
        user_thumbnail_dict['user_thumbnail_type'] = self.user_thumbnail.thumbnail_type or None

        for login in self.user_recent_login:
            temp_login_detail = {}
            temp_login_detail['login_ip'] = login.login_ip
            temp_login_detail['login_time'] = login.login_time
            user_recent_login_array.append(temp_login_detail)
        
        for following in self.user_following:
            user_following_array.append(following)

        for follower in self.user_follower:
            user_follower_array.append(follower)

        user_dict['user_id'] = str(self._id)
        user_dict['user_email'] = self.user_email
        user_dict['user_name'] = self.user_name
        user_dict['user_password'] = self.user_password 
        user_dict['user_detail'] = user_detail_dict
        user_dict['user_status'] = self.user_status
        user_dict['user_thumbnail'] = user_thumbnail_dict
        user_dict['user_reg_date'] = self.user_reg_date
        user_dict['user_recent_login'] = user_recent_login_array
        user_dict['user_following'] = user_following_array
        user_dict['user_follower'] = user_follower_array
        return user_dict


tu_detail = UserDetail(first_name="test_user", last_name="test_user", phone="+1xxxxxx", street1="str1", street2="str2", city="cty", state="stt", country="ctry", zip="zip")
tu_thumbnail = Thumbnail(thumbnail_uri="test_uri", thumbnail_type="test_type")
tu_login = LoginDetail(login_ip="1.1.1.1", login_time=parse("20201008153008"))
tu = User(user_email="xx.gmail.com", user_name="test_user", user_password="askdkj091", user_detail=tu_detail, user_status="active", user_thumbnail=tu_thumbnail, user_reg_date=parse("20201008141231"), user_recent_login=[tu_login], user_following=["kl12j3lk12j3l12k"], user_follower=["89889a7d98as789d", "1h312jj3h12kj312h"])
# tu.save()

print("=============== test: get video_op ===============\n")
vo = VideoOp.objects()
for v in vo:
    print(v.to_dict())
    print("\n")

print("=============== test: get user ===============\n")
usr = User()
usr = User.objects()
len(usr)
for u in usr:
    print(u.to_dict())
    print("\n")


# Flask-pymongo-2.3.0
# PyMongo-3.11
# dnspython-2.0.0

from flask import Flask
from flask_mongoengine import MongoEngine
from wtforms.fields import FieldList, FormField
from dateutil.parser import parse
import datetime
import bson

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
    first_name = db.StringField(max_length=50, default="")
    last_name = db.StringField(max_length=50, default="")
    phone = db.StringField(max_length=50, unique=True, default="")
    street1 = db.StringField(max_length=100, default="")
    street2 = db.StringField(max_length=100, default="")
    city = db.StringField(max_length=50, default="")
    state = db.StringField(max_length=50, default="")
    country = db.StringField(max_length=50, default="")
    zip = db.StringField(max_length=20, default="")


class Thumbnail(db.EmbeddedDocument):
    thumbnail_uri = db.StringField(max_length=200, required=True, default="")
    thumbnail_type = db.StringField(max_length=50, required=True, default="default")


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


class VideoURI(db.EmbeddedDocument):
    video_low = db.StringField(max_length=200, required=True)
    video_mid = db.StringField(max_length=200, required=True)
    video_high = db.StringField(max_length=200, required=True)


class Video(db.Document):
    _id = db.StringField()
    user_id = db.StringField(max_length=100, required=True)
    video_title = db.StringField(max_length=50, required=True, unique=True)
    video_tag = db.ListField(db.StringField())
    video_category = db.ListField(db.StringField())
    video_description = db.StringField(max_length=1000, default="")
    video_language = db.StringField(max_length=20)
    video_status = db.StringField(max_length=20, default="public", required=True)
    video_content = db.StringField()
    video_content_status = db.StringField(max_length=20, required=True)
    video_size = db.FloatField(default=0)
    video_view = db.LongField(default=0)
    video_like = db.LongField(default=0)
    video_dislike = db.LongField(default=0)
    video_comment = db.LongField(default=0)
    video_star = db.LongField(default=0)
    video_share = db.LongField(default=0)
    video_thumbnail = db.EmbeddedDocumentField('Thumbnail', required=True)
    video_upload_date = db.DateTimeField(required=True)
    video_uri = db.EmbeddedDocumentField('VideoURI', required=False)

    def to_dict(self):
        video_dict = {}
        video_tag_array = []
        video_category_array = []
        video_thumbnail_dict = {}
        video_uri_dict = {}

        for tag in self.video_tag:
            video_tag_array.append(tag)
        
        for category in self.video_category:
            video_category_array.append(category)
        
        video_thumbnail_dict['video_thumbnail_uri'] = self.video_thumbnail.thumbnail_uri or None
        video_thumbnail_dict['video_thumbnail_type'] = self.video_thumbnail.thumbnail_type or None

        video_uri_dict['video_uri_high'] = self.video_uri.video_high
        video_uri_dict['video_uri_mid'] = self.video_uri.video_mid
        video_uri_dict['video_uri_low'] = self.video_uri.video_low

        video_dict['video_id'] = str(self._id)
        video_dict['video_title'] = self.video_title
        video_dict['video_tag'] = video_tag_array
        video_dict['video_category'] = video_category_array
        video_dict['video_description'] = self.video_description
        video_dict['video_language'] = self.video_language
        video_dict['video_status'] = self.video_status
        video_dict['video_content'] = self.video_content
        video_dict['video_content_status'] = self.video_content_status
        video_dict['video_size'] = self.video_size or None
        video_dict['video_view'] = self.video_view
        video_dict['video_like'] = self.video_like
        video_dict['video_dislike'] = self.video_dislike
        video_dict['video_comment'] = self.video_comment
        video_dict['video_star'] = self.video_star
        video_dict['video_share'] = self.video_share
        video_dict['video_thumbnail'] = video_thumbnail_dict
        video_dict['video_upload_date'] = self.video_upload_date
        video_dict['video_uri'] = video_uri_dict

        return video_dict



def get_user_by_name(user_name: str):
    user = User.objects(user_name=user_name)
    return user


def get_user_by_email(user_email: str):
    user = User.objects(user_email=user_email)
    return user


def get_user_by_id(user_id: str):
    user = User.objects.get(_id = bson.ObjectId(user_id))
    return user


def create_user(user_name: str, user_email: str, user_password: str, user_ip="0.0.0.0"):
    if len(get_user_by_name(user_name)) > 0:
        print("user name is taken")
        return -1
        # Throw Error here
    elif len(get_user_by_email(user_email)) > 0:
        print("user email is taken")
        return -1
        # Throw Error here
    print("can register")
    login = []
    login.append(LoginDetail(login_ip=user_ip, login_time=datetime.datetime.now()))
    user = User(user_name=user_name, user_email=user_email, user_password=user_password, user_status="active", user_detail = UserDetail(), user_thumbnail=Thumbnail(), user_recent_login=login, user_reg_date=datetime.datetime.now())
    user.save()

create_user("test2", "test2@email.com", "testpasscode")


    
    
    


tu_detail = UserDetail(first_name="first_name", last_name="test_user", phone="+1xxxxxx", street1="str1", street2="str2", city="cty", state="stt", country="ctry", zip="zip")
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
usr = User.objects()
for u in usr:
    print(u.to_dict())
    print("\n")

print("=============== test: get user ===============\n")
video = Video.objects()
for v in video:
    print(v.to_dict())
    print("\n")
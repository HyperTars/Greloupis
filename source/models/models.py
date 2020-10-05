"""example
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(320), unique=True)
    password = db.Column(db.String(32), nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(320), unique=True)
    password = db.Column(db.String(32), nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username"""

# mongoengine-0.20.0

from mongoengine import *
from datetime import datetime


# Basic Models
class AddressDetail(Document):
    street1 = StringField(max_length=100)
    street2 = StringField(max_length=100)
    city = StringField(max_length=50)
    state = StringField(max_length=50)
    country = StringField(max_length=50)
    zip = StringField(max_length=20)
    

class UserDetail(Document):
    first_name = StringField(max_length=50, required=True)
    last_name = StringField(max_length=50, required=True)
    phone = StringField(max_length=50, required=True, unique=True)
    address = EmbeddedDocumentField(AddressDetails, required=False)


class LoginDetail(Document):
    login_ip = StringField(max_length=50, required=True)
    login_time = DateTimeField()


class VideoURI(Document):
    video_low = StringField(max_length=200, required=True)
    video_mid = StringField(max_length=200, required=True)
    video_high = StringField(max_length=200, required=True)


class Thumbnail(Document):
    thumbnail_uri = StringField(max_length=200, required=True)
    thumbnail_type = StringField(max_length=50, required=True)


# User Models
class User(Document):
    user_id = StringField(max_length=100, required=True, unique=True, primary_key=True)
    user_email = StringField(max_length=50, required=True, unique=True)
    user_name = StringField(max_length=60, required=True, unique=True)
    user_password = StringField(max_length=200, required=True)
    user_detail = EmbeddedDocumentField(UserDetails, required=True)
    user_status = StringField(max_length=50, required=True)
    user_thumbnail = EmbeddedDocumentField(Thumbnail, required=True)
    user_follower = LongField(default=0, required=True)
    user_reg_date = DateTimeField(default=datetime.now(), required=True)
    user_recent_login = ListField(EmbeddedDocumentField(LoginDetails))


class Follow(Document):
    follow_uploader = StringField(max_length=100, required=True)
    follow_by = StringField(max_length=100, required=True)
    follow_date = DateTimeField(default=datetime.now(), required=True)


class History(Document):
    history_id = LongField(max_length=100, required=True, unique=True, primary_key=True)
    user_id = StringField(max_length=100, required=True)
    video_id = StringField(max_length=100, required=True)
    process = DateTimeField(default=0, required=True)
    history_date = DateTimeField(default=datetime.now(), required=True)


# Video Models
class Video(Document):
    video_id = StringField(max_length=100, required=True, unique=True, primary_key=True)
    user_id = StringField(max_length=100, required=True)
    video_title = StringField(max_length=50, required=True, unique=True)
    video_tag = ListField(StringField)
    video_category = ListField(StringField)
    video_description = StringField(max_length=1000, default="")
    video_language = StringField(max_length=20)
    video_status = StringField(max_length=20, default="public", required=True)
    video_content = StringField()
    video_content_status = StringField(max_length=20, required=True)
    video_size = FloatField(default=0)
    video_view = LongField(default=0)
    video_like = LongField(default=0)
    video_dislike = LongField(default=0)
    video_comment = LongField(default=0)
    video_star = LongField(default=0)
    video_share = LongField(default=0)
    video_thumbnail = EmbeddedDocumentField(Thumbnail, required=True)
    video_upload_date = DateTimeField(default=datetime.now())
    video_uri = EmbeddedDocumentField(VideoURI, required=False)


class Comment(Document):
    comment_id = StringField(max_length=100, required=True, unique=True, primary_key=True)
    user_id = StringField(max_length=100, required=True)
    video_id = StringField(max_length=100,required=True)
    comment = StringField(max_length=1000, required=True)
    comment_date = DateTimeField(default=datetime, required=True)


class Like(Document):
    like_id = StringField(max_length=100, required=True, unique=True, primary_key=True)
    user_id = StringField(max_length=100, required=True)
    video_id = StringField(max_length=100,required=True)
    like_date = DateTimeField(default=datetime, required=True)


class Dislike(Document):
    dislike_id = StringField(max_length=100, required=True, unique=True, primary_key=True)
    user_id = StringField(max_length=100, required=True)
    video_id = StringField(max_length=100,required=True)
    dislike_date = DateTimeField(default=datetime, required=True)


class Star(Document):
    star_id = StringField(max_length=100, required=True, unique=True, primary_key=True)
    user_id = StringField(max_length=100, required=True)
    video_id = StringField(max_length=100,required=True)
    star_date = DateTimeField(default=datetime, required=True)


# Error Model
class Error(Document):
    call = DictField(required=True)
    response = DictField(required=True)
    date = DateTimeField(default=datetime.now(), required=True)
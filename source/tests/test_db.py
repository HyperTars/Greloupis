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

###############
# User Models #
###############
class UserDetail(db.EmbeddedDocument):
    first_name = db.StringField(max_length=50, default="")
    last_name = db.StringField(max_length=50, default="")
    phone = db.StringField(max_length=50, default="")
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


################
# Video Models #
################
class VideoURI(db.EmbeddedDocument):
    video_low = db.StringField(max_length=200, required=True)
    video_mid = db.StringField(max_length=200, required=True)
    video_high = db.StringField(max_length=200, required=True)


video_delete(video_id: str):
video_update(video_id: str, **kw):
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

##############
# Video CRUD #
##############
def video_get_by_id(video_id: str):
    """
    :return: an array of such Video (len == 0 or 1), len == 0 if no such video_id, len == 1 if found
    """
    return Video.objects(_id=bson.ObjectId(video_id))

##############
# Video Test #
##############
video_get_by_id("5f72999541bc583c4819d915")

#########################
# Video Operation Model #
#########################
class VideoOp(db.Document):
    _id = db.StringField()
    user_id = db.StringField(max_length=100, required=True)
    video_id = db.StringField(max_length=100, required=True)
    process = db.IntField(required=False, default=0)
    comment = db.StringField(max_length=1000, required=True)
    like = db.BooleanField(default=False)
    dislike = db.BooleanField(default=False)
    star = db.BooleanField(default=False)
    process_date = db.DateTimeField(required=False)
    comment_date = db.DateTimeField(required=False)
    like_date = db.DateTimeField(required=False)
    dislike_date = db.DateTimeField(required=False)
    star_date = db.DateTimeField(required=False)
    
    # Convert to dict
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
        video_op_dict['process_date'] = self.process_date
        video_op_dict['comment_date'] = self.comment_date
        video_op_dict['like_date'] = self.like_date
        video_op_dict['dislike_date'] = self.dislike_date
        video_op_dict['star_date'] = self.star_date
        return video_op_dict


#############
# User CRUD #
#############
def user_get_by_name(user_name: str):
    """
    :return: an array of such User, len == 0 if no such user_name, len == 1 if found
    """
    return User.objects(user_name=user_name)


def user_get_by_email(user_email: str):
    """
    :return: an array of such User (len == 0 or 1), len == 0 if no such user_email, len == 1 if found
    """
    return User.objects(user_email=user_email)


def user_get_by_id(user_id: str):
    """
    :return: an array of such User (len == 0 or 1), len == 0 if no such user_id, len == 1 if found
    """
    return User.objects(_id=bson.ObjectId(user_id))


def user_create(user_name: str, user_email: str, user_password: str, user_ip="0.0.0.0"):
    """
    :param user_name: user's unique nickname
    :param user_email: user's unique email
    :param user_password: user's password
    :param user_ip: user's ip address (defaut 0.0.0.0)
    :return: user object if succeeded, -1 if name already taken, -2 if email already taken
    """
    if len(user_get_by_name(user_name)) > 0:
        # print("user name is taken")
        return -1 # TODO: error_code
    elif len(user_get_by_email(user_email)) > 0:
        # print("user email is taken")
        return -2 # TODO: error_code
    login = []
    login.append(LoginDetail(login_ip=user_ip, login_time=datetime.datetime.utcnow()))
    user = User(user_name=user_name, user_email=user_email, user_password=user_password, user_status="private", user_detail = UserDetail(), user_thumbnail=Thumbnail(), user_recent_login=login, user_reg_date=datetime.datetime.utcnow())
    return user.save()


def user_update_status(user_id: str, user_status: str):
    """
    :param user_id: user's unique id
    :return: 1 if succeeded, -1 if no such user
    """
    if len(user_get_by_id(user_id)) == 0:
        # print("No such user")
        return -1 # TODO: error_code
    valid_status = ["public", "private", "closed"]
    if user_status not in valid_status:
        # print("Not valid status")
        return -2 # TODO: error_code
    return User.objects(_id=bson.ObjectId(user_id)).update(user_status=user_status)


def user_add_follow(follower_id: str, following_id: str):
    """
    :param follower_id: follower's user id
    :param following_id: uploader's user_id
    :return: 1 if succeeded, -1 if no such follower, -2 if no such uploader, -3 already followed
    """
    follower = user_get_by_id(follower_id)
    following = user_get_by_id(following_id)
    if len(follower) == 0:
        return -1
    if len(following) == 0:
        return -2
    if following_id in follower[0].user_following and follower_id in following[0].user_follower:
        # print("already followed")
        return -3
    if following_id in follower[0].user_following or follower_id in following[0].user_follower:
        # print("following relationship broken, try to remove")
        user_delete_follow(follower_id, following_id)
    r1 = User.objects(_id=bson.ObjectId(follower_id)).update(add_to_set__user_following=following_id)
    r2 = User.objects(_id=bson.ObjectId(following_id)).update(add_to_set__user_follower=follower_id)
    if r1 != 1:
        return r1
    elif r2 != 1:
        return r2
    return 1


def user_delete_follow(follower_id: str, following_id: str):
    """
    :param follower_id: follower's user id
    :param following_id: uploader's user_id
    :return: 1 if succeeded, -1 if no such follower, -2 if no such uploader
    """
    follower = user_get_by_id(follower_id)
    following = user_get_by_id(following_id)
    if len(follower) == 0:
        return -1
    if len(following) == 0:
        return -2
    r1 = User.objects(_id=bson.ObjectId(follower_id)).update(pull__user_following=following_id)
    r2 = User.objects(_id=bson.ObjectId(following_id)).update(pull__user_follower=follower_id)
    if r1 != 1:
        return r1
    elif r2 != 1:
        return r2
    return 1


def user_update_name(user_id: str, user_name: str):
    """
    :param user_id: user's id
    :param user_name: user's name
    :return: 1 if succeeded, -1 if no such user, -2 if same name as current, -3 if name already taken
    """
    users = user_get_by_id(user_id)
    if len(users) == 0:
        # print("No such user")
        return -1 # TODO: error_code
    old_name = users[0].user_name
    if user_name == old_name:
        # print("Same name as the current")
        return -2 # TODO: error_code
    if len(user_get_by_name(user_name)) > 0:
        # print("Name already taken")
        return -3 # TODO: error_code
    return User.objects(_id=bson.ObjectId(user_id)).update(user_name=user_name)


def user_update_password(user_id: str, user_password: str):
    """
    :param user_id: user's id
    :param user_password: user's password
    :return: 1 if succeeded, -1 if no such user, -2 if same password as current
    """
    users = user_get_by_id(user_id)
    if len(users) == 0:
        # print("No such user")
        return -1 # TODO: error_code
    old_password = users[0].user_password
    if user_password == old_password:
        # print("Same password as the current")
        return -2 # TODO: error_code
    return User.objects(_id=bson.ObjectId(user_id)).update(user_password=user_password)


def user_update_details(user_id: str, **kw):
    """
    :param user_first_name (optional): new user's first name
    :param user_last_name (optional): new user's last_name
    :param user_phone (optional): new user's phone
    :param user_street1 (optional): new user's street1
    :param user_street2 (optional): new user's street2
    :param user_city (optional): new user's city
    :param user_state (optional): new user's state
    :param user_country (optional): new user's country
    :param user_zip (optional): new user's zip
    :return 1 if succeeded, -1 if no such user
    """
    users = user_get_by_id(user_id)
    id = bson.ObjectId(user_id)
    if len(users) == 0:
        # print("No such user")
        return -1 # TODO: error_code
    if 'user_first_name' in kw:
        User.objects(_id=id).update(set__user_detail__first_name=kw['user_first_name'])
    if 'user_last_name' in kw:
        User.objects(_id=id).update(set__user_detail__last_name=kw['user_last_name'])
    if 'user_phone' in kw:
        User.objects(_id=id).update(set__user_detail__phone=kw['user_phone'])
    if 'user_street1' in kw:
        User.objects(_id=id).update(set__user_detail__street1=kw['user_street1'])
    if 'user_street2' in kw:
        User.objects(_id=id).update(set__user_detail__street2=kw['user_street2'])
    if 'user_city' in kw:
        User.objects(_id=id).update(set__user_detail__city=kw['user_city'])
    if 'user_state' in kw:
        User.objects(_id=id).update(set__user_detail__state=kw['user_state'])
    if 'user_country' in kw:
        User.objects(_id=id).update(set__user_detail__country=kw['user_country'])
    if 'user_zip' in kw:
        User.objects(_id=id).update(set__user_detail__zip=kw['user_zip'])
    return 1


def user_update_thumbnail(user_id: str, **kw):
    """
    :param user_id: user's unique id
    :param user_thumbnail_uri: thumbnail uri
    :param user_thumbnail_type: must be in ['default', 'user', 'system']
    :return 1 if succeeded, -1 if no such user, -2 if invalid thumbnail type
    """
    users = user_get_by_id(user_id)
    id = bson.ObjectId(user_id)
    if len(users) == 0:
        # print("No such user")
        return -1 # TODO: error_code
    valid_type=['default', 'user', 'system']
    if 'user_thumbnail_uri' in kw:
        User.objects(_id=id).update(set__user_thumbnail__thumbnail_uri=kw['user_thumbnail_uri'])
    if 'user_thumbnail_type' in kw:
        if kw['user_thumbnail_type'] not in valid_type:
            # print("Invalid thumbnail type")
            return -2 # TODO: error_code
        User.objects(_id=id).update(set__user_thumbnail__thumbnail_type=kw['user_thumbnail_type'])
    return 1


def user_add_login(user_id: str, ip="0.0.0.0", time=datetime.datetime.utcnow()):
    """
    :param user_id: user's unique id
    :param ip: user's login ip address
    :param time: user's login time (utc, optional), default: current system time (utc)
    :return: 0 if succeeded, -1 if no such user, -2 if time already exist
    """
    users = user_get_by_id(user_id)
    if len(users) == 0:
        # print("No such user")
        return -1 # TODO: error_code
    # only keep 10 login info
    login_history = users[0].user_recent_login
    oldest_login_time = login_history[0].login_time
    latest_login_time = login_history[-1].login_time
    if len(login_history) >= 10:
        # print("Delete oldest history")
        User.objects(_id=bson.ObjectId(user_id)).update(pull__user_recent_login__login_time=oldest_login_time)
    # add new login info
    # print(time)
    # print(latest_login_time)
    if time == latest_login_time:
        # print("Login info already added")
        return -2
    new_login = {'login_ip': ip, 'login_time': time}
    User.objects(_id=bson.ObjectId(user_id)).update(add_to_set__user_recent_login=[new_login])
    return 0


def user_delete(user_id: str):
    """
    :param user_id: user's unique id
    :return: 1 if succeeded, -1 if no such user
    """
    users = user_get_by_id(user_id)
    if len(users) == 0:
        # print("No such user")
        return -1 # TODO: error_code
    return User.objects(_id=bson.ObjectId(user_id)).delete()


################
# VideoOp CRUD #
################
def video_op_create(user_id: str, video_id: str, init_time=datetime.datetime.now()):
    if len(user_get_by_id(user_id)) == 0:
        # print("No such user")
        return -1 # TODO: error_code
    if len(video_get_by_id(video_id)) == 0:
        # print("No such video")
        return -2 # TODO: error_code
    if len(video_op_get_by_user_video(user_id, video_id)) > 0:
        # print("video_op exists")
        return -3 # TODO: error_code
    video_op = VideoOp(user_id=user_id, video_id=video_id, process=0, comment="", like=False, dislike=False, star=False, process_date=init_time, comment_date=init_time, like_date=init_time, dislike_date=init_time, star_date=init_time)
    return video_op.save()

def video_op_get_by_user_id(user_id: str):
    """
    :param: user_id, user's unique id
    :return: an array of such video_op, len == 0 if no such video_op
    """
    return VideoOp.objects(user_id=user_id)

def video_op_get_by_video_id( video_id: str):
    """
    :param: video_id, video's unique id
    :return: an array of such video_op, len == 0 if no such video_op
    """
    return VideoOp.objects(video_id=video_id)

def video_op_get_by_user_video(user_id: str, video_id: str):
    """
    :param: user_id, user's unique id
    :param: video_id, video's unique id
    :return: an array of such video_op (len == 0 or 1), len == 0 if no such video_op, len == 1 if found
    """
    return VideoOp.objects(user_id=user_id, video_id=video_id)

def video_op_get_by_op_id(op_id: str):
    """
    :param: op_id, video operation unique id
    :return: an array of such video_op (len == 0 or 1), len == 0 if no such video_op_id, len == 1 if found
    """
    return VideoOp.objects(_id=bson.ObjectId(op_id))

def video_op_update_process(op_id: str, process: int, process_date=datetime.datetime.now()):
    """
    :param: op_id, video op unique id
    :param: process, video watching process
    :param: process_date (optional, default utc now)
    :return: 1 if succeeded, -1 if no such video_op
    """
    if len(video_op_get_by_op_id(op_id)) == 0:
        # No such video op
        return -1 # TODO: error_code
    return VideoOp.objects(_id=bson.ObjectId(op_id)).update(process=process, process_date=process_date)

def video_op_update_comment(op_id: str, comment: str, comment_date=datetime.datetime.now()):
    """
    :param: op_id, video op unique id
    :param: comment, video comment
    :param: comment_date (optional, default utc now)
    :return: 1 if succeeded, -1 if no such video_op
    """
    if len(video_op_get_by_op_id(op_id)) == 0:
        # No such video op
        return -1 # TODO: error_code
    return VideoOp.objects(_id=bson.ObjectId(op_id)).update(comment=comment, comment_date=comment_date)

def video_op_update_like(op_id: str, like: bool, like_date=datetime.datetime.now()):
    """
    :param: op_id, video op unique id
    :param: like, video like (boolean)
    :param: like_date (optional, default utc now)
    :return: 1 if succeeded, -1 if no such video_op
    """
    if len(video_op_get_by_op_id(op_id)) == 0:
        # No such video op
        return -1 # TODO: error_code
    return VideoOp.objects(_id=bson.ObjectId(op_id)).update(like=like, like_date=like_date)

def video_op_update_dislike(op_id: str, dislike: bool, dislike_date=datetime.datetime.now()):
    """
    :param: op_id, video op unique id
    :param: dislike, video dislike (boolean)
    :param: dislike_date (optional, default utc now)
    :return: 1 if succeeded, -1 if no such video_op
    """
    if len(video_op_get_by_op_id(op_id)) == 0:
        # No such video op
        return -1 # TODO: error_code
    return VideoOp.objects(_id=bson.ObjectId(op_id)).update(dislike=dislike, dislike_date=dislike_date)

def video_op_update_star(op_id: str, star: bool, star_date=datetime.datetime.now()):
    """
    :param: op_id, video op unique id
    :param: star, video star (boolean)
    :param: star_date (optional, default utc now)
    :return: 1 if succeeded, -1 if no such video_op
    """
    if len(video_op_get_by_op_id(op_id)) == 0:
        # No such video op
        return -1 # TODO: error_code
    return VideoOp.objects(_id=bson.ObjectId(op_id)).update(star=star, star_date=star_date)


############
# RAW TEST #
############
print("=============== RAW TEST =================")
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


#############
# User Test #
#############
print("=============== test: update user thumbnail ===============\n")
user_update_thumbnail("5f808f78c2ac20387eb8f3c8", user_thumbnail_uri="s3.amazon.com/aidjasjds", user_thumbnail_type="origin") # invalid type error
user_update_thumbnail("5f808f78c2ac20387eb8f3c8", user_thumbnail_uri="s3.amazon.com/aidjasjds", user_thumbnail_type="default") # invalid type error

print("=============== test: update user detail ===============\n")
user_update_details("5f808f78c2ac20387eb8f3c8", user_first_name="fffff", user_last_name="kkk", user_phone="+1313123123", user_zip="11201")

print("=============== test: update user status ===============\n")
user_update_status("5f808f78c2ac20387eb8f3c8", "active") # invalid status
user_update_status("5f808f78c2ac20387eb8f3c8", "public") # success
user_update_status("5f808f78c2ac20387eb8f3c8", "private") # success

print("=============== test: update user name ===============\n")
user_update_name("5f808f78c2ac20387eb8f3c8", "test4") # name conflict
user_update_name("5f808f78c2ac20387eb8f3c8", "test2") # same as current conflict
user_update_name("5f808f78c2ac20387eb8f3c8", "test1") # success
user_update_name("5f808f78c2ac20387eb8f3c8", "test2") # change back

print("=============== test: update user password ===============\n")
user_update_password("5f808f78c2ac20387eb8f3c8", "testpasscode") # same as current conflict
user_update_password("5f808f78c2ac20387eb8f3c8", "test77888") # success
user_update_password("5f808f78c2ac20387eb8f3c8", "testpasscode") # change back

print("=============== test: add user login ===============\n")
user_add_login("5f808f78c2ac20387eb8f3c8", ip="127.0.1.1")

print("=============== test: add/delete user following ===============\n")
user_add_follow("5f808f78c2ac20387eb8f3c8", "5f808f045e03b2165ca4275a")
user_delete_follow("5f808f78c2ac20387eb8f3c8", "5f808f045e03b2165ca4275a")

# print("=============== test: RAW DATA CONSTRUCT TEST ===============\n")
# tu_detail = UserDetail(first_name="first_name", last_name="test_user", phone="+1xxxxxx", street1="str1", street2="str2", city="cty", state="stt", country="ctry", zip="zip")
# tu_thumbnail = Thumbnail(thumbnail_uri="test_uri", thumbnail_type="test_type")
# tu_login = LoginDetail(login_ip="1.1.1.1", login_time=parse("20201008153008"))
# tu = User(user_email="xx.gmail.com", user_name="test_user", user_password="askdkj091", user_detail=tu_detail, user_status="active", user_thumbnail=tu_thumbnail, user_reg_date=parse("20201008141231"), user_recent_login=[tu_login], user_following=["kl12j3lk12j3l12k"], user_follower=["89889a7d98as789d", "1h312jj3h12kj312h"])
# tu.save()

print("=============== test: delete user ===============\n")
user_delete("5f808f78c2ac20387eb8f3c8")

print("=============== test: create user ===============\n")
user_create("test2", "test2@email.com", "testpasscode")
user_create("test3", "test2@email.com", "testpasscode") # email conflict
user_create("test2", "test3@email.com", "testpasscode") # name conflict
user_create("test4", "test4@email.com", "testpasscode")

print("=============== test: delete user (set status deleted)===============\n")
user_delete("5f808f78c2ac20387eb8f3c8")


#################
# Video Op Test #
#################
print("=============== test: Video Op CRUD ===============\n")
video_op_create("5f808f79c2ac20387eb8f3c9", "5f72999541bc583c4819d915")
video_op_get_by_user_id("5f808f79c2ac20387eb8f3c9")[0].to_json()
video_op_get_by_video_id("5f72999541bc583c4819d915")[0].to_json()
video_op_get_by_user_video("5f808f79c2ac20387eb8f3c9", "5f72999541bc583c4819d915")[0].to_json()
video_op_get_by_op_id("5f80f7b05490b2aef73d6314")[0].to_json()
video_op_update_process("5f80fd775490b2aef73d6315", 142)
video_op_update_comment("5f80fd775490b2aef73d6315", "Interesting.")
video_op_update_like("5f80fd775490b2aef73d6315", True)
video_op_update_dislike("5f80fd775490b2aef73d6315", True)
video_op_update_star("5f80fd775490b2aef73d6315", True)
video_op_update_like("5f80fd775490b2aef73d6315", False)
video_op_update_dislike("5f80fd775490b2aef73d6315", False)
video_op_update_star("5f80fd775490b2aef73d6315", False)
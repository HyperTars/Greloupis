# Flask-pymongo-2.3.0
# PyMongo-3.11
# dnspython-2.0.0

from flask import Flask
from flask_mongoengine import MongoEngine
from wtforms.fields import FieldList, FormField
from dateutil.parser import parse
import datetime
import bson
from source.db.query_user import *
from source.db.query_video import *
from source.db.query_video_op import *

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


##############
# Video Test #
##############
video_get_by_id("5f72999541bc583c4819d915")[0].to_dict()
video_get_by_title("XiXiHaHa")[0].to_dict()
video_delete("5f810903cd3d45e0e5989891")
video_create("5f808f79c2ac20387eb8f3c9", "test video", "https://s3.amazon.com/test_video.mp4")
video_create("5f808f79c2ac20387eb8f3c9", "test film", "https://s3.amazon.com/test_film.mp4", video_tag=['movie'], video_category=['funny', 'action'])

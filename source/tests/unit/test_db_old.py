# dnspython-2.0.0

import re

from source.settings import *
from source.db.mongo import get_db
from source.db.query_user import *
from source.db.query_video import *
from source.db.query_video_op import *


############
# RAW TEST #
############
def test_raw():
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
def test_user():
    print("=============== test: update user thumbnail ===============\n")
    print(query_user_update_thumbnail("5f808f79c2ac20387eb8f3c9", user_thumbnail_uri="s3.amazon.com/aidjasjds",
                                      user_thumbnail_type="origin"))  # invalid type error
    print(query_user_update_thumbnail("5f808f79c2ac20387eb8f3c9", user_thumbnail_uri="s3.amazon.com/aidjasjds",
                                      user_thumbnail_type="default"))

    print("=============== test: update user detail ===============\n")
    print(query_user_update_details("5f808f79c2ac20387eb8f3c9", user_first_name="fffff", user_last_name="kkk",
                                    user_phone="+1313123123", user_zip="11201"))

    print("=============== test: update user status ===============\n")
    print(query_user_update_status("5f808f79c2ac20387eb8f3c9", "active"))  # invalid status
    print(query_user_update_status("5f808f79c2ac20387eb8f3c9", "public"))  # success
    print(query_user_update_status("5f808f79c2ac20387eb8f3c9", "private"))  # success

    print("=============== test: update user name ===============\n")
    print(query_user_update_name("5f80bef29342f187a0fa2d70", "test4"))  # name conflict
    print(query_user_update_name("5f80bef29342f187a0fa2d70", "test2"))  # same as current conflict
    print(query_user_update_name("5f80bef29342f187a0fa2d70", "test1"))  # success
    print(query_user_update_name("5f80bef29342f187a0fa2d70", "test2"))  # change back

    print("=============== test: update user password ===============\n")
    print(query_user_update_password("5f80bef29342f187a0fa2d70", "testpasscode"))  # same as current conflict
    print(query_user_update_password("5f80bef29342f187a0fa2d70", "test77888"))  # success
    print(query_user_update_password("5f80bef29342f187a0fa2d70", "testpasscode"))  # change back

    print("=============== test: add user login ===============\n")
    print(query_user_add_login("5f80bef29342f187a0fa2d70", ip="127.0.1.1"))

    print("=============== test: add/delete user following ===============\n")
    print(query_user_add_follow("5f80bef29342f187a0fa2d70", "5f808f045e03b2165ca4275a"))
    print(query_user_delete_follow("5f80bef29342f187a0fa2d70", "5f808f045e03b2165ca4275a"))

    """
    print("=============== test: RAW DATA CONSTRUCT TEST ===============\n")
    tu_detail = UserDetail(first_name="first_name", last_name="test_user", phone="+1xxxxxx", street1="str1",
                           street2="str2", city="cty", state="stt", country="ctry", zip="zip")
    tu_thumbnail = Thumbnail(thumbnail_uri="test_uri", thumbnail_type="test_type")
    tu_login = LoginDetail(login_ip="1.1.1.1", login_time=parse("20201008153008"))
    tu = User(user_email="xx.gmail.com", user_name="test_user", user_password="askdkj091", user_detail=tu_detail,
              user_status="active", user_thumbnail=tu_thumbnail, user_reg_date=parse("20201008141231"),
              user_recent_login=[tu_login], user_following=["kl12j3lk12j3l12k"],
              user_follower=["89889a7d98as789d", "1h312jj3h12kj312h"])
    tu.save()
    """

    print("=============== test: create user ===============\n")
    print(query_user_create("test2", "test2@email.com", "testpasscode"))
    print(query_user_create("test3", "test2@email.com", "testpasscode"))  # email conflict
    print(query_user_create("test2", "test3@email.com", "testpasscode"))  # name conflict
    print(query_user_create("test4", "test4@email.com", "testpasscode"))

    print("=============== test: delete user ===============\n")
    print(query_user_delete("5f826e97e6c6dfa87b7ffde4"))


#################
# Video Op Test #
#################
def test_video_op():
    print("=============== test: Video Op CRUD ===============\n")
    print(query_video_op_create("5f808f79c2ac20387eb8f3c9", "5f72999541bc583c4819d915"))
    print(query_video_op_get_by_user_id("5f808f79c2ac20387eb8f3c9")[0].to_json())
    print(query_video_op_get_by_video_id("5f72999541bc583c4819d915")[0].to_json())
    print(query_video_op_get_by_user_video("5f808f79c2ac20387eb8f3c9", "5f72999541bc583c4819d915")[0].to_json())
    print(query_video_op_get_by_op_id("5f80fd775490b2aef73d6315")[0].to_json())
    print(query_video_op_update_process("5f80fd775490b2aef73d6315", 142))
    print(query_video_op_update_comment("5f80fd775490b2aef73d6315", "Interesting."))
    print(query_video_op_update_like("5f80fd775490b2aef73d6315", True))
    print(query_video_op_update_dislike("5f80fd775490b2aef73d6315", True))
    print(query_video_op_update_star("5f80fd775490b2aef73d6315", True))
    print(query_video_op_update_like("5f80fd775490b2aef73d6315", False))
    print(query_video_op_update_dislike("5f80fd775490b2aef73d6315", False))
    print(query_video_op_update_star("5f80fd775490b2aef73d6315", False))


##############
# Video Test #
##############
def test_video():
    print("=============== test: Video CRUD ===============\n")
    print(query_video_get_by_id("5f72999541bc583c4819d915")[0].to_dict())
    print(query_video_get_by_title("XiXiHaHa")[0].to_dict())
    print(query_video_delete("5f810903cd3d45e0e5989891"))
    print(query_video_create("5f808f79c2ac20387eb8f3c9", "test video", "https://s3.amazon.com/test_video.mp4"))
    print(query_video_create("5f808f79c2ac20387eb8f3c9", "test film", "https://s3.amazon.com/test_film.mp4",
                             video_tag=['movie'], video_category=['funny', 'action']))
    print(query_video_update("5f72999541bc583c4819d915", video_uri_low="https://s3.amazon.com/test_low_quality.mp4"))
    print(query_video_cnt_incr_by_one("5f72999541bc583c4819d915", "view"))
    print(query_video_cnt_incr_by_one("5f72999541bc583c4819d915", "comments"))
    print(query_video_cnt_incr_by_one("5f72999541bc583c4819d915", "likes"))
    print(query_video_cnt_incr_by_one("5f72999541bc583c4819d915", "video_dislike"))
    print(query_video_cnt_incr_by_one("5f72999541bc583c4819d915", "video_star"))
    print(query_video_cnt_incr_by_one("5f72999541bc583c4819d915", "share"))
    print(query_video_cnt_decr_by_one("5f72999541bc583c4819d915", "video_star"))
    print(query_video_cnt_decr_by_one("5f72999541bc583c4819d915", "video_star"))
    print(query_video_cnt_decr_by_one("5f72999541bc583c4819d915", "video_star"))
    print(query_video_cnt_decr_by_one("5f72999541bc583c4819d915", "video_star"))
    print(query_video_cnt_decr_by_one("5f72999541bc583c4819d915", "video_star"))


###############
# Search Test #
###############
def test_search():
    # Search by keyword (case sensitive)
    print(query_user_search_by_contains(keyword_name="test"))
    print(query_user_search_by_contains(keyword_email="test"))

    # Search by pattern (can ignore case)
    print(query_user_search_by_pattern(pattern_zip=re.compile(".*11201.*", re.IGNORECASE)))
    print(query_user_search_by_pattern(pattern_name=re.compile('.*E.*T.*', re.IGNORECASE)))  # Ignore case

    # Search by aggregate (can search multi attributes)
    pipeline1 = [
        {
            "$match":
                {
                    "user_name": {"$regex": "es"},
                    "user_status": "active"
                }
        }
    ]
    pipeline2 = [
        {"$unwind": "$user_detail"},
        {
            "$match":
                {
                    "user_detail.street1": {"$regex": "343"},
                    "user_status": "public"
                }
        }
    ]
    print("\nAggregate search:")
    print(query_user_search_by_aggregate(pipeline2))


if __name__ == "__main__":
    db = get_db(TestConfig)
    print(db.app.config)
    print(query_user_create("test2", "test2@email.com", "testpasscode"))
    print(query_user_create("test3", "test2@email.com", "testpasscode"))  # email conflict
    print(query_user_create("test2", "test3@email.com", "testpasscode"))  # name conflict
    print(query_user_create("test4", "test4@email.com", "testpasscode"))
    #print(query_video_create("5f808f79c2ac20387eb8f3c9", "test video", "https://s3.amazon.com/test_video.mp4"))
    #print(query_video_create("5f808f79c2ac20387eb8f3c9", "test film", "https://s3.amazon.com/test_film.mp4",
    #                         video_tag=['movie'], video_category=['funny', 'action']))
    #print(query_video_op_create("5f808f79c2ac20387eb8f3c9", "5f72999541bc583c4819d915"))
    #test_raw()
    #test_user()
    #test_video_op()
    #test_video()
    #test_search()


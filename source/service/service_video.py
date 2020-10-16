from source.db.mongo import get_db
from source.db.query_user import *
from source.db.query_video import *
from source.utils.util_pattern import *
from source.utils.util_serializer import *


def service_video_upload(conf, **kw):
    db = get_db(conf)

    if "body" in kw:
        query_video_create(kw["body"]["user_id"], kw["body"]["video_title"], kw["body"]["video_raw_content"])

        # get the video by title
        result = query_video_get_by_title(kw["body"]["video_title"])
    else:
        result = [{}]

    return result


def service_video_info(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw:
        result = query_video_get_by_id(kw["video_id"])
    else:
        result = [{}]

    return result


def service_video_update():
    return


def service_video_delete():
    return

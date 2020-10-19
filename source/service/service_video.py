from source.db.mongo import get_db
from source.db.query_user import *
from source.db.query_video import *
from source.utils.util_pattern import *
from source.utils.util_serializer import *
from source.models.model_errors import *


def service_video_upload(conf, **kw):
    db = get_db(conf)

    if "body" in kw:
        user_id = kw["body"]["user_id"]
        video_title = kw["body"]["video_title"]
        video_raw_content = kw["body"]["video_raw_content"]

        try:
            query_video_create(user_id=user_id, video_title=video_title, video_raw_content=video_raw_content)

            # get the video by title
            result = query_video_get_by_title(kw["body"]["video_title"])

        except Exception as e:
            return extract_error_msg(str(e)[1:-1])

    else:
        result = [{}]

    return result


def service_video_info(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw:
        try:
            result = query_video_get_by_video_id(kw["video_id"])
        except Exception as e:
            return extract_error_msg(str(e)[1:-1])
    else:
        result = [{}]

    return result


def service_video_update(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw and "body" in kw:
        try:
            result = query_video_get_by_video_id(kw["video_id"])
            original = json.loads(util_serializer_mongo_results_to_array(result, format="json")[0])

            video_title = kw["body"]["video_title"] if 'video_title' in kw["body"] \
                else original["video_title"]
            video_raw_content = kw["body"]["video_raw_content"] if 'video_raw_content' in kw["body"] \
                else original["video_raw_content"]
            video_raw_status = kw["body"]["video_raw_status"] if 'video_raw_status' in kw["body"] \
                else original["video_raw_status"]
            video_raw_size = kw["body"]["video_raw_size"] if 'video_raw_size' in kw["body"] \
                else original["video_raw_size"]
            video_duration = int(kw["body"]["video_duration"]) if 'video_duration' in kw["body"] \
                else int(original["video_duration"])
            video_channel = kw["body"]["video_channel"] if 'video_channel' in kw["body"] \
                else original["video_channel"]
            video_tag = kw["body"]["video_tag"] if 'video_tag' in kw["body"] \
                else original["video_tag"]
            video_category = kw["body"]["video_category"] if 'video_category' in kw["body"] \
                else original["video_category"]
            video_description = kw["body"]["video_description"] if 'video_description' in kw["body"] \
                else original["video_description"]
            video_language = kw["body"]["video_language"] if 'video_language' in kw["body"] \
                else original["video_language"]
            video_status = kw["body"]["video_status"] if 'video_status' in kw["body"] \
                else original["video_status"]
            video_thumbnail = kw["body"]["video_thumbnail"] if 'video_thumbnail' in kw["body"] \
                else original["video_thumbnail"]
            video_uri_low = kw["body"]["video_uri_low"] if 'video_uri_low' in kw["body"] \
                else original["video_uri"]["video_uri_low"]
            video_uri_mid = kw["body"]["video_uri_mid"] if 'video_uri_mid' in kw["body"] \
                else original["video_uri"]["video_uri_mid"]
            video_uri_high = kw["body"]["video_uri_high"] if 'video_uri_high' in kw["body"] \
                else original["video_uri"]["video_uri_high"]

            query_video_update(video_id=kw["video_id"], video_title=video_title,
                               video_raw_content=video_raw_content, video_raw_status=video_raw_status,
                               video_raw_size=video_raw_size, video_channel=video_channel,
                               video_duration=video_duration, video_tag=video_tag,
                               video_category=video_category, video_description=video_description,
                               video_language=video_language, video_status=video_status,
                               video_thumbnail=video_thumbnail, video_uri_low=video_uri_low,
                               video_uri_mid=video_uri_mid, video_uri_high=video_uri_high)

            # get the video by ID
            result = query_video_get_by_video_id(kw["video_id"])

        except Exception as e:
            return extract_error_msg(str(e))

    else:
        result = [{}]

    return result


def service_video_delete(conf, **kw):
    db = get_db(conf)

    if "video_id" in kw:
        try:
            result = query_video_delete(kw["video_id"])
        except Exception as e:
            return extract_error_msg(str(e)[1:-1])

    else:
        result = -1

    return result

from db.mongo import get_db
from db.query_video import query_video_update, query_video_delete, \
    query_video_create, query_video_get_by_title, \
    query_video_get_by_user_id, query_video_get_by_video_id
from db.query_video_op import query_video_op_get_by_video_id, \
    query_video_op_delete
from db.query_user import query_user_get_by_id
from utils.util_pattern import util_pattern_format_param
from utils.util_serializer import util_serializer_mongo_results_to_array
from utils.util_validator import is_valid_id
from models.model_errors import ServiceError, ErrorCode, MongoError

VALID_VIDEO_STATUS = ['public', 'private', 'processing', 'deleted']


def service_video_auth_get(token, video_id):
    videos = query_video_get_by_video_id(video_id)
    if len(videos) == 0:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_NOT_FOUND)
    video = videos[0].to_dict()
    user = video['user_id']
    status = video['video_status']
    if status != 'public' and user != token:
        return False
    return True


def service_video_auth_modify(token, video_id):
    videos = query_video_get_by_video_id(video_id)
    if len(videos) == 0:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_NOT_FOUND)
    video = videos[0].to_dict()
    if video['user_id'] == token:
        return True
    return False


def service_video_upload(conf, **kw):
    get_db(conf)
    kw['service'] = 'video'
    kw = util_pattern_format_param(**kw)

    # keyword check and formatting
    if 'user_id' not in kw or 'video_title' not in kw \
            or 'video_raw_content' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    # perform db operations and get result
    query_video_create(kw['user_id'], kw['video_title'],
                       kw['video_raw_content'])
    uploaded_result = query_video_get_by_title(kw['video_title'])
    if len(uploaded_result) == 0:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_NOT_FOUND)
    return uploaded_result


def service_video_info(conf, **kw):
    get_db(conf)
    kw['service'] = 'video'
    kw = util_pattern_format_param(**kw)
    # keyword check and formatting
    if 'video_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    if not is_valid_id(kw["video_id"]):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)
    # perform db operations and get result
    video = query_video_get_by_video_id(kw["video_id"])
    if len(video) == 0:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_NOT_FOUND)

    res = video[0].to_dict()
    user_id = res["user_id"]
    user_obj = query_user_get_by_id(user_id)[0].to_dict()
    res["user_name"] = user_obj["user_name"]
    res["user_thumbnail"] = user_obj["user_thumbnail"]
    return res


def service_video_get_by_user(conf, **kw):
    get_db(conf)
    kw['service'] = 'video'
    kw = util_pattern_format_param(**kw)
    # keyword check and formatting
    if 'user_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)
    videos = query_video_get_by_user_id(kw['user_id'])
    if len(videos) == 0:
        return [{}]
    video_array = util_serializer_mongo_results_to_array(videos)
    return video_array    


def service_video_update(conf, **kw):
    get_db(conf)
    kw['service'] = 'video'
    kw = util_pattern_format_param(**kw)

    # keyword check and formatting
    if 'video_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    if 'video_status' in kw and kw['video_status'] not in VALID_VIDEO_STATUS:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_INVALID_STATUS)

    if not is_valid_id(kw["video_id"]):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    # perform db operations and get result
    video_get_result = query_video_get_by_video_id(kw["video_id"])
    if len(video_get_result) == 0:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_NOT_FOUND)
    original = util_serializer_mongo_results_to_array(video_get_result)[0]

    # override original data or not
    video_title = kw["video_title"] if 'video_title' in kw \
        else original["video_title"]
    video_raw_content = kw["video_raw_content"] if 'video_raw_content' in kw \
        else original["video_raw_content"]
    video_raw_status = kw["video_raw_status"] if 'video_raw_status' in kw \
        else original["video_raw_status"]
    video_raw_size = kw["video_raw_size"] if 'video_raw_size' in kw \
        else original["video_raw_size"]
    video_duration = int(kw["video_duration"]) if 'video_duration' in kw \
        else int(original["video_duration"])
    video_channel = kw["video_channel"] if 'video_channel' in kw \
        else original["video_channel"]
    video_tag = kw["video_tag"] if 'video_tag' in kw else original["video_tag"]
    video_category = kw["video_category"] if 'video_category' in kw \
        else original["video_category"]
    video_description = kw["video_description"] if 'video_description' in kw \
        else original["video_description"]
    video_language = kw["video_language"] if 'video_language' in kw \
        else original["video_language"]
    video_status = kw["video_status"] if 'video_status' in kw \
        else original["video_status"]
    video_thumbnail = kw["video_thumbnail"] if 'video_thumbnail' in kw \
        else original["video_thumbnail"]
    video_uri_low = kw["video_uri_low"] if 'video_uri_low' in kw \
        else original["video_uri"]["video_uri_low"]
    video_uri_mid = kw["video_uri_mid"] if 'video_uri_mid' in kw \
        else original["video_uri"]["video_uri_mid"]
    video_uri_high = kw["video_uri_high"] if 'video_uri_high' in kw \
        else original["video_uri"]["video_uri_high"]

    query_video_update(video_id=kw["video_id"], video_title=video_title,
                       video_raw_content=video_raw_content,
                       video_raw_status=video_raw_status,
                       video_raw_size=video_raw_size,
                       video_channel=video_channel,
                       video_duration=video_duration,
                       video_tag=video_tag,
                       video_category=video_category,
                       video_description=video_description,
                       video_language=video_language,
                       video_status=video_status,
                       video_thumbnail=video_thumbnail,
                       video_uri_low=video_uri_low,
                       video_uri_mid=video_uri_mid,
                       video_uri_high=video_uri_high)

    return query_video_get_by_video_id(kw["video_id"])


def service_video_comments(conf, **kw):
    get_db(conf)
    kw['service'] = 'video'
    kw = util_pattern_format_param(**kw)

    # keyword check and formatting
    if 'video_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    if not is_valid_id(kw["video_id"]):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    # perform db operations and get result
    search_mongo = query_video_op_get_by_video_id(kw["video_id"])
    if len(search_mongo) == 0:
        return []

    search_result = util_serializer_mongo_results_to_array(search_mongo)

    comments_result = []
    for each in search_result:
        if each["comment"] != "":
            user_obj = query_user_get_by_id(each["user_id"])[0].to_dict()
            comments_result.append({
                "video_id": each["video_id"],
                "user_id": each["user_id"],
                "user_name": user_obj["user_name"],
                "user_thumbnail": user_obj["user_thumbnail"],
                "comment": each["comment"],
                "comment_date": str(each["comment_date"])
            })

    return comments_result


def service_video_likes(conf, **kw):
    get_db(conf)
    kw['service'] = 'video'
    kw = util_pattern_format_param(**kw)

    # keyword check and formatting
    if 'video_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    if not is_valid_id(kw["video_id"]):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    # perform db operations and get result
    search_mongo = query_video_op_get_by_video_id(kw["video_id"])
    if len(search_mongo) == 0:
        return []

    search_result = util_serializer_mongo_results_to_array(search_mongo)

    like_result = []
    for each in search_result:
        if each["like"]:
            user_obj = query_user_get_by_id(each["user_id"])[0].to_dict()
            like_result.append({
                "video_id": each["video_id"],
                "user_id": each["user_id"],
                "user_name": user_obj["user_name"],
                "like_date": str(each["like_date"])
            })

    return like_result


def service_video_dislikes(conf, **kw):
    get_db(conf)
    kw['service'] = 'video'
    kw = util_pattern_format_param(**kw)

    # keyword check and formatting
    if 'video_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    if not is_valid_id(kw["video_id"]):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    # perform db operations and get result
    search_mongo = query_video_op_get_by_video_id(kw["video_id"])
    if len(search_mongo) == 0:
        return []

    search_result = util_serializer_mongo_results_to_array(search_mongo)

    dislike_result = []
    for each in search_result:
        if each["dislike"]:
            user_obj = query_user_get_by_id(each["user_id"])[0].to_dict()
            dislike_result.append({
                "video_id": each["video_id"],
                "user_id": each["user_id"],
                "user_name": user_obj["user_name"],
                "dislike_date": str(each["dislike_date"])
            })

    return dislike_result


def service_video_stars(conf, **kw):
    get_db(conf)
    kw['service'] = 'video'
    kw = util_pattern_format_param(**kw)

    # keyword check and formatting
    if 'video_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    if not is_valid_id(kw["video_id"]):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    # perform db operations and get result
    search_mongo = query_video_op_get_by_video_id(kw["video_id"])
    if len(search_mongo) == 0:
        return []

    search_result = util_serializer_mongo_results_to_array(search_mongo)

    star_result = []
    for each in search_result:
        if each["star"]:
            user_obj = query_user_get_by_id(each["user_id"])[0].to_dict()
            star_result.append({
                "video_id": each["video_id"],
                "user_id": each["user_id"],
                "user_name": user_obj["user_name"],
                "star_date": str(each["star_date"])
            })

    return star_result


def service_video_delete(conf, **kw):
    get_db(conf)
    kw['service'] = 'video'
    kw = util_pattern_format_param(**kw)

    # keyword check and formatting
    if 'video_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    if not is_valid_id(kw["video_id"]):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    # perform db operations and get result
    delete_result = query_video_delete(kw["video_id"])
    if delete_result == 1:
        # delete all video_op related to this video
        video_op_objects = query_video_op_get_by_video_id(kw["video_id"])
        video_op_results = util_serializer_mongo_results_to_array(
            video_op_objects)
        for each in video_op_results:
            query_video_op_delete(each["video_op_id"])

        return delete_result
    else:
        raise MongoError(ErrorCode.MONGODB_VIDEO_DELETE_FAILURE)

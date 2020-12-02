from db.query_video import query_video_update, query_video_delete, \
    query_video_create, query_video_get_by_user_id, \
    query_video_get_by_video_id
from db.query_video_op import query_video_op_get_by_video_id, \
    query_video_op_delete
from db.query_user import query_user_get_by_id
from utils.util_pattern import util_pattern_format_param
from utils.util_serializer import util_serializer_mongo_results_to_array
from utils.util_validator import is_valid_id
from models.model_errors import ServiceError, ErrorCode
from settings import config

conf = config['default']
VALID_VIDEO_STATUS = conf.VIDEO_STATUS
VALID_VIDEO_RAW_STATUS = conf.VIDEO_RAW_STATUS


def service_video_upload(user_id: str):

    if not is_valid_id(user_id):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    # perform db operations and get result
    vid = query_video_create(user_id)
    return vid


def service_video_info(**kw):

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


def service_video_get_by_user(**kw):

    kw['service'] = 'video'
    kw = util_pattern_format_param(**kw)
    # keyword check and formatting
    if 'user_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)
    if not is_valid_id(kw["user_id"]):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)
    videos = query_video_get_by_user_id(kw['user_id'])
    if len(videos) == 0:
        return []
    video_array = util_serializer_mongo_results_to_array(videos)
    return video_array


def service_video_update(**kw):

    kw['service'] = 'video'
    kw = util_pattern_format_param(**kw)

    # keyword check and formatting
    if 'video_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    if not is_valid_id(kw["video_id"]):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    if 'video_status' in kw and kw['video_status'] not in VALID_VIDEO_STATUS:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_INVALID_STATUS)

    if 'video_raw_status' in kw and \
       kw['video_raw_status'] not in VALID_VIDEO_RAW_STATUS:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_INVALID_STATUS)

    query_video_update(**kw)

    return query_video_get_by_video_id(kw["video_id"])


def service_video_comments(**kw):

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


def service_video_likes(**kw):

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


def service_video_dislikes(**kw):

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


def service_video_stars(**kw):

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


def service_video_delete(**kw):

    kw['service'] = 'video'
    kw = util_pattern_format_param(**kw)

    # keyword check and formatting
    if 'video_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    if not is_valid_id(kw['video_id']):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    # delete by setting status
    if 'method' in kw and kw['method'] == 'status':
        res = query_video_update(kw['video_id'], video_status='deleted')
    # delete by removing from database
    else:
        res = query_video_delete(kw['video_id'], silent=True)

    # delete all op in this video immediately
    ops = query_video_op_get_by_video_id(kw['video_id'])
    for op in ops:
        opid = op.to_dict()['video_op_id']
        query_video_op_delete(opid, silent=True)
    return res

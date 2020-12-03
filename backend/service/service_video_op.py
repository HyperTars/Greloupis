from db.query_video import query_video_get_by_video_id, \
    query_video_cnt_decr_by_one, query_video_cnt_incr_by_one
from db.query_video_op import query_video_op_update_star, \
    query_video_op_update_dislike, query_video_op_update_like, \
    query_video_op_update_comment, query_video_op_update_process, \
    query_video_op_get_by_user_video, query_video_op_create, \
    query_video_op_get_by_user_id
from utils.util_validator import is_valid_id
from utils.util_serializer import util_serializer_mongo_results_to_array
from utils.util_pattern import util_pattern_format_param
from utils.util_time import get_time_now_utc
from models.model_errors import ErrorCode, ServiceError


def service_video_op_create(user_id: str, video_id: str):
    query_video_op_create(user_id, video_id)
    return query_video_op_get_by_user_video(user_id, video_id)


def service_video_op_get_by_user(**kw):

    kw['service'] = 'video_op'
    kw = util_pattern_format_param(**kw)
    # keyword check and formatting
    if 'user_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    ops = query_video_op_get_by_user_id(kw['user_id'])
    if len(ops) == 0:
        return []

    op_array = util_serializer_mongo_results_to_array(ops)

    # get video name and video thumbnail for each op video
    for op in op_array:
        videos = query_video_get_by_video_id(op['video_id'])
        if len(videos) == 0:
            raise ServiceError(ErrorCode.SERVICE_VIDEO_NOT_FOUND)
        video = videos[0].to_dict()

        op['video_title'] = video['video_title']
        op['video_thumbnail'] = video['video_thumbnail']

    return op_array


def service_video_op_add_view(**kw):

    # keyword check and formatting
    if 'video_id' not in kw and 'id' not in kw and '_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    kw['service'] = 'video_op'
    kw = util_pattern_format_param(**kw)

    if not is_valid_id(kw["video_id"]):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    # perform db operations and get result
    query_video_cnt_incr_by_one(kw["video_id"], "video_view")

    search_result = util_serializer_mongo_results_to_array(
        query_video_get_by_video_id(kw["video_id"]))
    video_view = search_result[0]["video_view"]
    return_body = {
        "video_id": kw["video_id"],
        "view_count": video_view
    }
    return return_body


def service_video_op_get_view(**kw):

    # keyword check and formatting
    if 'video_id' not in kw and 'id' not in kw and '_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    kw['service'] = 'video_op'
    kw = util_pattern_format_param(**kw)

    if not is_valid_id(kw["video_id"]):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    # perform db operations and get result
    videos = query_video_get_by_video_id(kw["video_id"])

    if len(videos) == 0:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_NOT_FOUND)

    search_result = util_serializer_mongo_results_to_array(videos)
    video_view = search_result[0]["video_view"]
    return_body = {
        "video_id": kw["video_id"],
        "view_count": video_view
    }
    return return_body


def service_video_op_add_comment(**kw):

    # keyword check and formatting
    if 'video_id' not in kw or 'user_id' not in kw or 'comment' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    kw['service'] = 'video_op'
    kw = util_pattern_format_param(**kw)

    if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    # check if the video_op object exists
    query_video_op = query_video_op_get_by_user_video(kw["user_id"],
                                                      kw["video_id"])
    if len(query_video_op) == 0:
        # create a new video_op object for current user and video
        query_video_op = service_video_op_create(kw["user_id"], kw["video_id"])

    video_op_result = util_serializer_mongo_results_to_array(query_video_op)
    video_op_id = video_op_result[0]["video_op_id"]

    # check if successfully update comment
    query_video_op_update_comment(
        video_op_id, kw["video_op_comment"], get_time_now_utc())

    query_video_cnt_incr_by_one(kw["video_id"], "video_comment")

    query_video_op = query_video_op_get_by_user_video(
        kw["user_id"], kw["video_id"])

    if len(query_video_op) == 0:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_OP_NOT_FOUND)

    video_op_obj = util_serializer_mongo_results_to_array(query_video_op)[0]

    return_body = {
        "user_id": video_op_obj["user_id"],
        "video_id": video_op_obj["video_id"],
        "comment": video_op_obj["comment"],
        "comment_date": str(video_op_obj["comment_date"])
    }
    return return_body


def service_video_op_get_comment(**kw):

    # keyword check and formatting
    if 'video_id' not in kw or 'user_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    kw['service'] = 'video_op'
    kw = util_pattern_format_param(**kw)

    if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    # check if the video_op object exists
    query_video_op = query_video_op_get_by_user_video(kw["user_id"],
                                                      kw["video_id"])

    if len(query_video_op) == 0:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_OP_NOT_FOUND)

    video_op_result = util_serializer_mongo_results_to_array(
            query_video_op)
    return_body = {
        "user_id": video_op_result[0]["user_id"],
        "video_id": video_op_result[0]["video_id"],
        "comment": video_op_result[0]["comment"],
        "comment_date": str(video_op_result[0]["comment_date"])
    }
    return return_body


def service_video_op_update_comment(**kw):

    # keyword check and formatting
    if 'video_id' not in kw or 'user_id' not in kw or 'comment' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    kw['service'] = 'video_op'
    kw = util_pattern_format_param(**kw)

    if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    # check if the video_op object exists
    query_video_op = query_video_op_get_by_user_video(kw["user_id"],
                                                      kw["video_id"])
    if len(query_video_op) == 0:
        # create a new video_op object for current user and video
        query_video_op = service_video_op_create(kw["user_id"], kw["video_id"])

    video_op_result = util_serializer_mongo_results_to_array(query_video_op)
    video_op_id = video_op_result[0]["video_op_id"]

    # check if successfully update comment
    query_video_op_update_comment(
        video_op_id,  kw["video_op_comment"], get_time_now_utc())

    if len(query_video_op) == 0:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_OP_NOT_FOUND)

    query_video_op = query_video_op_get_by_user_video(
        kw["user_id"], kw["video_id"])

    video_op_obj = util_serializer_mongo_results_to_array(query_video_op)[0]

    return_body = {
        "user_id": video_op_obj["user_id"],
        "video_id": video_op_obj["video_id"],
        "comment": video_op_obj["comment"],
        "comment_date": str(video_op_obj["comment_date"])
    }
    return return_body


def service_video_op_cancel_comment(**kw):

    # keyword check and formatting
    if 'video_id' not in kw or 'user_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    kw['service'] = 'video_op'
    kw = util_pattern_format_param(**kw)

    if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    # check if the video_op object exists
    query_video_op = query_video_op_get_by_user_video(kw["user_id"],
                                                      kw["video_id"])
    if len(query_video_op) == 0:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_OP_NOT_FOUND)

    video_op_result = util_serializer_mongo_results_to_array(
        query_video_op)
    video_op_id = video_op_result[0]["video_op_id"]

    query_video_op_update_comment(
        video_op_id, "", get_time_now_utc())

    query_video_cnt_decr_by_one(kw["video_id"], "video_comment")

    query_video_op = query_video_op_get_by_user_video(
        kw["user_id"], kw["video_id"])

    video_op_obj = util_serializer_mongo_results_to_array(
        query_video_op)[0]

    return_body = {
        "user_id": video_op_obj["user_id"],
        "video_id": video_op_obj["video_id"],
        "comment": video_op_obj["comment"],
        "comment_date": str(video_op_obj["comment_date"])
        }
    return return_body


def service_video_op_add_process(**kw):

    # keyword check and formatting
    if 'video_id' not in kw or 'user_id' not in kw or 'process' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    kw['service'] = 'video_op'
    kw = util_pattern_format_param(**kw)

    if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    # check if the video_op object exists
    query_video_op = query_video_op_get_by_user_video(kw["user_id"],
                                                      kw["video_id"])

    if len(query_video_op) == 0:
        # create a new video_op object for current user and video
        query_video_op = service_video_op_create(kw["user_id"], kw["video_id"])

    video_op_result = util_serializer_mongo_results_to_array(query_video_op)
    video_op_id = video_op_result[0]["video_op_id"]

    if video_op_result[0]["process"] != 0:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_OP_EXISTS)

    # check if successfully update process
    if int(kw["process"]) >= 0:
        query_video_op_update_process(
            video_op_id, kw["process"], get_time_now_utc())
    else:
        raise ServiceError(ErrorCode.SERVICE_INVALID_SEARCH_PARAM)

    query_video_op = query_video_op_get_by_user_video(
        kw["user_id"], kw["video_id"])
    video_op_obj = util_serializer_mongo_results_to_array(query_video_op)[0]

    return_body = {
        "user_id": video_op_obj["user_id"],
        "video_id": video_op_obj["video_id"],
        "process": video_op_obj["process"],
        "process_date": str(video_op_obj["process_date"])
    }
    return return_body


def service_video_op_get_process(**kw):

    # keyword check and formatting
    if 'video_id' not in kw or 'user_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    kw['service'] = 'video_op'
    kw = util_pattern_format_param(**kw)

    if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    # check if the video_op object exists
    query_video_op = query_video_op_get_by_user_video(kw["user_id"],
                                                      kw["video_id"])
    if len(query_video_op) == 0:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_OP_NOT_FOUND)

    video_op_result = util_serializer_mongo_results_to_array(
        query_video_op)
    video_op_obj = video_op_result[0]

    return_body = {
        "user_id": video_op_obj["user_id"],
        "video_id": video_op_obj["video_id"],
        "process": video_op_obj["process"],
        "process_date": str(video_op_obj["process_date"])
    }
    return return_body


def service_video_op_update_process(**kw):

    # keyword check and formatting
    if 'video_id' not in kw or 'user_id' not in kw or 'process' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    kw['service'] = 'video_op'
    kw = util_pattern_format_param(**kw)

    if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    # check if the video_op object exists
    query_video_op = query_video_op_get_by_user_video(kw["user_id"],
                                                      kw["video_id"])

    if len(query_video_op) == 0:
        # create a new video_op object for current user and video
        query_video_op = service_video_op_create(kw["user_id"], kw["video_id"])

    video_op_result = util_serializer_mongo_results_to_array(query_video_op)
    video_op_id = video_op_result[0]["video_op_id"]

    # check if successfully update process
    if int(kw["process"]) >= 0:
        query_video_op_update_process(
            video_op_id, kw["process"], get_time_now_utc())
    else:
        raise ServiceError(ErrorCode.SERVICE_INVALID_SEARCH_PARAM)

    query_video_op = query_video_op_get_by_user_video(
        kw["user_id"], kw["video_id"])
    video_op_obj = util_serializer_mongo_results_to_array(query_video_op)[0]

    return_body = {
        "user_id": video_op_obj["user_id"],
        "video_id": video_op_obj["video_id"],
        "process": video_op_obj["process"],
        "process_date": str(video_op_obj["process_date"])
    }
    return return_body


def service_video_op_cancel_process(**kw):

    # keyword check and formatting
    if 'video_id' not in kw or 'user_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    kw['service'] = 'video_op'
    kw = util_pattern_format_param(**kw)

    if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    # check if the video_op object exists
    query_video_op = query_video_op_get_by_user_video(kw["user_id"],
                                                      kw["video_id"])

    if len(query_video_op) == 0:
        # create a new video_op object for current user and video
        query_video_op = service_video_op_create(kw["user_id"], kw["video_id"])

    video_op_result = util_serializer_mongo_results_to_array(query_video_op)
    video_op_id = video_op_result[0]["video_op_id"]

    if video_op_result[0]["process"] == 0:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_PROCESS_DELETE_FAILURE)

    # check if successfully delete process
    query_video_op_update_process(
        video_op_id, 0, get_time_now_utc())

    query_video_op = query_video_op_get_by_user_video(
        kw["user_id"], kw["video_id"])
    video_op_obj = util_serializer_mongo_results_to_array(query_video_op)[0]

    return_body = {
        "user_id": video_op_obj["user_id"],
        "video_id": video_op_obj["video_id"],
        "process": video_op_obj["process"],
        "process_date": str(video_op_obj["process_date"])
    }
    return return_body


def service_video_op_add_like(**kw):

    # keyword check and formatting
    if 'video_id' not in kw or 'user_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    kw['service'] = 'video_op'
    kw = util_pattern_format_param(**kw)

    if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    # check if the video_op object exists
    query_video_op = query_video_op_get_by_user_video(kw["user_id"],
                                                      kw["video_id"])

    if len(query_video_op) == 0:
        # create a new video_op object for current user and video
        query_video_op = service_video_op_create(kw["user_id"], kw["video_id"])

    video_op_result = util_serializer_mongo_results_to_array(query_video_op)
    video_op_id = video_op_result[0]["video_op_id"]

    # If already liked, like operation cannot be duplicated
    if video_op_result[0]["like"]:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_LIKE_UPDATE_FAILURE)

    # If already disliked, dislike operation should be set to False
    if video_op_result[0]["dislike"]:
        query_video_op_update_dislike(video_op_id, False)
        query_video_cnt_decr_by_one(kw["video_id"], "video_dislike")

    # check if successfully add like
    query_video_op_update_like(
        video_op_id, True, get_time_now_utc())

    query_video_cnt_incr_by_one(kw["video_id"], "video_like")

    query_video_op = query_video_op_get_by_user_video(
        kw["user_id"], kw["video_id"])
    video_op_obj = util_serializer_mongo_results_to_array(query_video_op)[0]

    return_body = {
        "user_id": video_op_obj["user_id"],
        "video_id": video_op_obj["video_id"],
        "like": video_op_obj["like"],
        "like_date": str(video_op_obj["like_date"]),
        "dislike": video_op_obj["dislike"],
        "dislike_date": str(video_op_obj["dislike_date"])
    }
    return return_body


def service_video_op_cancel_like(**kw):

    # keyword check and formatting
    if 'video_id' not in kw or 'user_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    kw['service'] = 'video_op'
    kw = util_pattern_format_param(**kw)

    if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    # check if the video_op object exists
    query_video_op = query_video_op_get_by_user_video(kw["user_id"],
                                                      kw["video_id"])

    if len(query_video_op) == 0:
        # create a new video_op object for current user and video
        query_video_op = service_video_op_create(kw["user_id"], kw["video_id"])

    video_op_result = util_serializer_mongo_results_to_array(query_video_op)
    video_op_id = video_op_result[0]["video_op_id"]

    # Only perform the operation when like is True and dislike is False
    if video_op_result[0]["like"] and not video_op_result[0]["dislike"]:
        query_video_op_update_like(video_op_id, False, get_time_now_utc())
        query_video_cnt_decr_by_one(kw["video_id"], "video_like")

        query_video_op = query_video_op_get_by_user_video(
            kw["user_id"], kw["video_id"])
        video_op_obj = util_serializer_mongo_results_to_array(
            query_video_op)[0]

        return_body = {
            "user_id": video_op_obj["user_id"],
            "video_id": video_op_obj["video_id"],
            "like": video_op_obj["like"],
            "like_date": str(video_op_obj["like_date"]),
            "dislike": video_op_obj["dislike"],
            "dislike_date": str(video_op_obj["dislike_date"])
        }
        return return_body
    else:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_LIKE_UPDATE_FAILURE)


def service_video_op_add_dislike(**kw):

    # keyword check and formatting
    if 'video_id' not in kw or 'user_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    kw['service'] = 'video_op'
    kw = util_pattern_format_param(**kw)

    if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    # check if the video_op object exists
    query_video_op = query_video_op_get_by_user_video(kw["user_id"],
                                                      kw["video_id"])

    if len(query_video_op) == 0:
        # create a new video_op object for current user and video
        query_video_op = service_video_op_create(kw["user_id"], kw["video_id"])

    video_op_result = util_serializer_mongo_results_to_array(query_video_op)
    video_op_id = video_op_result[0]["video_op_id"]

    # If already disliked, dislike operation cannot be duplicated
    if video_op_result[0]["dislike"]:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_DISLIKE_UPDATE_FAILURE)

    # If already liked, like operation should be set to False
    if video_op_result[0]["like"]:
        query_video_op_update_like(video_op_id, False, get_time_now_utc())
        query_video_cnt_decr_by_one(kw["video_id"], "video_like")

    # check if successfully add dislike
    query_video_op_update_dislike(video_op_id, True, get_time_now_utc())

    query_video_cnt_incr_by_one(kw["video_id"], "video_dislike")

    query_video_op = query_video_op_get_by_user_video(
        kw["user_id"], kw["video_id"])
    video_op_obj = util_serializer_mongo_results_to_array(query_video_op)[0]

    return_body = {
        "user_id": video_op_obj["user_id"],
        "video_id": video_op_obj["video_id"],
        "like": video_op_obj["like"],
        "like_date": str(video_op_obj["like_date"]),
        "dislike": video_op_obj["dislike"],
        "dislike_date": str(video_op_obj["dislike_date"])
    }
    return return_body


def service_video_op_cancel_dislike(**kw):

    # keyword check and formatting
    if 'video_id' not in kw or 'user_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    kw['service'] = 'video_op'
    kw = util_pattern_format_param(**kw)

    if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    # check if the video_op object exists
    query_video_op = query_video_op_get_by_user_video(kw["user_id"],
                                                      kw["video_id"])

    if len(query_video_op) == 0:
        # create a new video_op object for current user and video
        query_video_op = service_video_op_create(kw["user_id"], kw["video_id"])

    video_op_result = util_serializer_mongo_results_to_array(query_video_op)
    video_op_id = video_op_result[0]["video_op_id"]

    # Only perform the operation when like is False and dislike is True
    if not video_op_result[0]["like"] and video_op_result[0]["dislike"]:
        query_video_op_update_dislike(video_op_id, False, get_time_now_utc())
        query_video_cnt_decr_by_one(kw["video_id"], "video_dislike")

        query_video_op = query_video_op_get_by_user_video(kw["user_id"],
                                                          kw["video_id"])
        video_op_obj = util_serializer_mongo_results_to_array(
            query_video_op)[0]

        return_body = {
            "user_id": video_op_obj["user_id"],
            "video_id": video_op_obj["video_id"],
            "like": video_op_obj["like"],
            "like_date": str(video_op_obj["like_date"]),
            "dislike": video_op_obj["dislike"],
            "dislike_date": str(video_op_obj["dislike_date"])
        }
        return return_body

    else:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_DISLIKE_UPDATE_FAILURE)


def service_video_op_add_star(**kw):

    # keyword check and formatting
    if 'video_id' not in kw or 'user_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    kw['service'] = 'video_op'
    kw = util_pattern_format_param(**kw)

    if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    # check if the video_op object exists
    query_video_op = query_video_op_get_by_user_video(kw["user_id"],
                                                      kw["video_id"])

    if len(query_video_op) == 0:
        # create a new video_op object for current user and video
        query_video_op = service_video_op_create(kw["user_id"], kw["video_id"])

    video_op_result = util_serializer_mongo_results_to_array(query_video_op)
    video_op_id = video_op_result[0]["video_op_id"]

    # If already starred, star operation cannot be duplicated
    if video_op_result[0]["star"]:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_STAR_UPDATE_FAILURE)

    # check if successfully add star
    query_video_op_update_star(video_op_id, True, get_time_now_utc())

    query_video_cnt_incr_by_one(kw["video_id"], "video_star")

    query_video_op = query_video_op_get_by_user_video(
        kw["user_id"], kw["video_id"])
    video_op_obj = util_serializer_mongo_results_to_array(query_video_op)[0]

    return_body = {
        "user_id": video_op_obj["user_id"],
        "video_id": video_op_obj["video_id"],
        "star": video_op_obj["star"],
        "star_date": str(video_op_obj["star_date"])
    }
    return return_body


def service_video_op_cancel_star(**kw):

    # keyword check and formatting
    if 'video_id' not in kw or 'user_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    kw['service'] = 'video_op'
    kw = util_pattern_format_param(**kw)

    if not is_valid_id(kw["video_id"]) or not is_valid_id(kw["user_id"]):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    # check if the video_op object exists
    query_video_op = query_video_op_get_by_user_video(kw["user_id"],
                                                      kw["video_id"])

    if len(query_video_op) == 0:
        # create a new video_op object for current user and video
        query_video_op = service_video_op_create(kw["user_id"], kw["video_id"])

    video_op_result = util_serializer_mongo_results_to_array(query_video_op)
    video_op_id = video_op_result[0]["video_op_id"]

    # Only perform the operation when star is True
    if video_op_result[0]["star"]:
        query_video_op_update_star(video_op_id, False, get_time_now_utc())
        query_video_cnt_decr_by_one(kw["video_id"], "video_star")

        query_video_op = query_video_op_get_by_user_video(
            kw["user_id"], kw["video_id"])
        video_op_obj = util_serializer_mongo_results_to_array(
            query_video_op)[0]

        return_body = {
            "user_id": video_op_obj["user_id"],
            "video_id": video_op_obj["video_id"],
            "star": video_op_obj["star"],
            "star_date": str(video_op_obj["star_date"])
        }
        return return_body
    else:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_STAR_UPDATE_FAILURE)

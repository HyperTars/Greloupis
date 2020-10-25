from source.models.model_errors import *
from source.settings import *
from source.db.query_user import *
from source.db.query_video import *
from source.db.query_video_op import *
from source.utils.util_hash import *
from source.utils.util_serializer import *
from source.utils.util_validator import *
from source.utils.util_pattern import *
from source.db.mongo import get_db


def service_user_reg(conf, **kw):
    """
    Register user

    :param conf: config
    :param kw: keyword
    :keyword:
        :key user_name: (required) str
        :key user_email: (required) str
        :key user_ip: (optional) str
    :return user model:
    """
    # user_name: str, user_email: str, user_password: str, user_ip = "0.0.0.0"
    # service_user_reg(conf, user_name="t", user_email="k", user_password="lol")

    db = get_db(conf)
    kw['service'] = 'user'
    kw = util_pattern_format_param(**kw)
    if 'user_name' not in kw or 'user_email' not in kw or 'user_password' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    query_user_create(kw['user_name'], kw['user_email'], util_hash_encode(kw['user_password']))

    return query_user_get_by_name(kw['user_name'])[0].to_dict()


def service_user_check_password(conf, **kw):
    db = get_db(conf)
    kw['service'] = 'user'
    kw = util_pattern_format_param(**kw)

    if 'user_name' in kw and 'user_password' in kw:
        users = query_user_get_by_name(kw['user_name'])
    elif 'user_email' in kw and 'user_password' in kw:
        users = query_user_get_by_email(kw['user_email'])
    else:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    if len(users) == 0:
        raise ServiceError(ErrorCode.SERVICE_USER_NOT_FOUND)

    return util_hash_encode(kw['user_password']) == users[0].user_password


# def service_user_get_user(conf, **kw):
#     # service_user_get_user(config['default'], user_name="t", user_password="lol")
#
#     db = get_db(conf)
#
#     # TODO: validate user by session
#
#     # Validate user by password
#     if 'user_name' not in kw and 'user_email' not in kw:
#         return ErrorCode.SERVICE_MISSING_PARAM
#     if 'user_password' not in kw:
#         return ErrorCode.SERVICE_MISSING_PARAM
#
#     auth = service_user_check_password(**kw)
#
#     if type(auth) == ErrorCode or auth is False:
#         return ErrorCode.SERVICE_USER_NOT_FOUND
#
#     if 'user_name' in kw:
#         return query_user_get_by_name(kw['user_name'])[0].to_dict()
#     if 'user_email' in kw:
#         return query_user_get_by_email(kw['user_email'])[0].to_dict()
#
#     return ErrorCode.SERVICE_MISSING_PARAM
#
#
# def service_user_login(conf, **kw):
#     user = service_user_get_user(conf, **kw)
#
#     if type(user) == ErrorCode:
#         return ErrorCode.SERVICE_USER_AUTH_FAILURE
#
#     return user
#
#
# def service_user_logout():
#     return
#
#
# def service_user_update_info(conf, **kw):
#     db = get_db(conf)
#     return


def service_user_cancel(conf, user_id):
    db = get_db(conf)
    return query_user_delete_by_id(user_id)


def service_user_get_info(conf, user_id):
    db = get_db(conf)
    final_result = {}

    # user_id check
    if not is_valid_id(user_id):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    # table: user
    user_result = query_user_get_by_id(user_id)
    if len(user_result) == 1:
        user_result_dict_array = util_serializer_mongo_results_to_array(user_result)

        # convert datetime format to str
        for each_result in user_result_dict_array:
            for key, value in each_result.items():
                if isinstance(value, datetime.datetime):
                    each_result[key] = str(value)

        final_result["user"] = user_result_dict_array
    else:
        raise ServiceError(ErrorCode.SERVICE_USER_NOT_FOUND)

    # table: video (belong to this user)
    video_result = query_video_get_by_user_id(user_id)
    if len(video_result) > 0:
        video_result_dict_array = util_serializer_mongo_results_to_array(video_result)

        # convert datetime format to str
        for each_result in video_result_dict_array:
            for key, value in each_result.items():
                if isinstance(value, datetime.datetime):
                    each_result[key] = str(value)

        final_result["video"] = video_result_dict_array
    else:
        final_result["video"] = [{}]

    # table: video op (belong to this user)
    video_op_result = query_video_op_get_by_user_id(user_id)
    if len(video_op_result) > 0:
        video_op_result_dict_array = util_serializer_mongo_results_to_array(video_op_result)

        # convert datetime format to str
        for each_result in video_op_result_dict_array:
            for key, value in each_result.items():
                if isinstance(value, datetime.datetime):
                    each_result[key] = str(value)

        final_result["video_op"] = video_op_result_dict_array
    else:
        final_result["video_op"] = [{}]

    return final_result


def service_user_get_like(conf, user_id):
    db = get_db(conf)

    # user_id check
    if not is_valid_id(user_id):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    if len(query_user_get_by_id(user_id)) <= 0:
        raise ServiceError(ErrorCode.SERVICE_USER_NOT_FOUND)

    # perform db operations and get result
    search_mongo = query_video_op_get_by_user_id(user_id)
    if len(search_mongo) == 0:
        raise ServiceError(ErrorCode.SERVICE_USER_NO_VIDEO_OP)

    search_result = util_serializer_mongo_results_to_array(search_mongo)

    like_result = []
    for each in search_result:
        if each["like"]:
            like_result.append({
                "video_id": each["video_id"],
                "user_id": each["user_id"],
                "like_date": str(each["like_date"])
            })

    return like_result


def service_user_get_dislike(conf, user_id):
    db = get_db(conf)

    # user_id check
    if not is_valid_id(user_id):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    if len(query_user_get_by_id(user_id)) <= 0:
        raise ServiceError(ErrorCode.SERVICE_USER_NOT_FOUND)

    # perform db operations and get result
    search_mongo = query_video_op_get_by_user_id(user_id)
    if len(search_mongo) == 0:
        raise ServiceError(ErrorCode.SERVICE_USER_NO_VIDEO_OP)

    search_result = util_serializer_mongo_results_to_array(search_mongo)

    dislike_result = []
    for each in search_result:
        if each["dislike"]:
            dislike_result.append({
                "video_id": each["video_id"],
                "user_id": each["user_id"],
                "dislike_date": str(each["dislike_date"])
            })

    return dislike_result


def service_user_get_comment(conf, user_id):
    db = get_db(conf)

    # user_id check
    if not is_valid_id(user_id):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    if len(query_user_get_by_id(user_id)) <= 0:
        raise ServiceError(ErrorCode.SERVICE_USER_NOT_FOUND)

    # perform db operations and get result
    search_mongo = query_video_op_get_by_user_id(user_id)
    if len(search_mongo) == 0:
        raise ServiceError(ErrorCode.SERVICE_USER_NO_VIDEO_OP)

    search_result = util_serializer_mongo_results_to_array(search_mongo)

    comment_result = []
    for each in search_result:
        if each["comment"] != "":
            comment_result.append({
                "video_id": each["video_id"],
                "user_id": each["user_id"],
                "comment": each["comment"],
                "comment_date": str(each["comment_date"])
            })

    return comment_result


def service_user_get_star(conf, user_id):
    db = get_db(conf)

    # user_id check
    if not is_valid_id(user_id):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    if len(query_user_get_by_id(user_id)) <= 0:
        raise ServiceError(ErrorCode.SERVICE_USER_NOT_FOUND)

    # perform db operations and get result
    search_mongo = query_video_op_get_by_user_id(user_id)
    if len(search_mongo) == 0:
        raise ServiceError(ErrorCode.SERVICE_USER_NO_VIDEO_OP)

    search_result = util_serializer_mongo_results_to_array(search_mongo)

    star_result = []
    for each in search_result:
        if each["star"]:
            star_result.append({
                "video_id": each["video_id"],
                "user_id": each["user_id"],
                "star_date": str(each["star_date"])
            })

    return star_result

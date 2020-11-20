from utils.util_hash import util_hash_encode
from utils.util_serializer import util_serializer_mongo_results_to_array
from utils.util_validator import is_valid_id
from utils.util_pattern import util_pattern_format_param
from db.mongo import get_db
from db.query_user import query_user_create, query_user_get_by_name, \
    query_user_get_by_email, query_user_delete_by_id, \
    query_user_get_by_id, query_user_update_status, \
    query_user_add_login, query_user_update_name, \
    query_user_update_password, query_user_update_thumbnail, \
    query_user_update_details
from db.query_video import query_video_get_by_user_id
from db.query_video_op import query_video_op_get_by_user_id, \
    query_video_op_delete
from service.service_video import service_video_delete
from models.model_errors import ServiceError, ErrorCode


def service_user_auth_get(token, user_id):
    users = query_user_get_by_id(user_id)
    if len(users) == 0:
        raise ServiceError(ErrorCode.SERVICE_USER_NOT_FOUND)
    user = users[0].to_dict()
    if user['user_status'] == 'public' or token == user_id:
        return True
    return False


def service_user_auth_modify(token, user_id):
    return token == user_id


def service_user_reg(**kw):
    """
    Register user

    :param conf: config
    :param kw: keyword
    :keyword:
        :key user_name: (required) str
        :key user_email: (required) str
        :key user_password: (required) str
        :key user_ip: (optional) str
    :return user model:
    """
    # user_name: str, user_email: str, user_password: str, user_ip = "0.0.0.0"
    # service_user_reg(conf, user_name="t", user_email="k",
    # user_password="lol")
    get_db()
    kw['service'] = 'user'
    kw = util_pattern_format_param(**kw)
    if 'user_name' not in kw or 'user_email' not in kw \
            or 'user_password' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    query_user_create(kw['user_name'], kw['user_email'],
                      util_hash_encode(kw['user_password']))

    return query_user_get_by_name(kw['user_name'])[0].to_dict()


def service_user_login(**kw):
    get_db()
    kw['service'] = 'user'
    kw = util_pattern_format_param(**kw)
    if 'user_name' in kw and 'user_password' in kw:
        users = query_user_get_by_name(kw['user_name'])
        if len(users) == 0:
            raise ServiceError(ErrorCode.SERVICE_USER_NOT_FOUND)
        user = users[0]
        if util_hash_encode(kw['user_password']) != user.user_password:
            raise ServiceError(ErrorCode.SERVICE_USER_PASS_WRONG)
    elif 'user_email' in kw and 'user_password' in kw:
        users = query_user_get_by_email(kw['user_email'])
        if len(users) == 0:
            raise ServiceError(ErrorCode.SERVICE_USER_NOT_FOUND)
        user = users[0]
        if util_hash_encode(kw['user_password']) != user.user_password:
            raise ServiceError(ErrorCode.SERVICE_USER_PASS_WRONG)
    elif 'user' in kw and 'user_password' in kw:
        user_names = query_user_get_by_name(kw['user'])
        user_emails = query_user_get_by_email(kw['user'])
        if len(user_emails) == 0 and len(user_names) == 0:
            raise ServiceError(ErrorCode.SERVICE_USER_NOT_FOUND)
        elif len(user_emails) != 0:
            user = user_emails[0]
        elif len(user_names) != 0:
            user = user_names[0]
        if util_hash_encode(kw['user_password']) != user.user_password:
            raise ServiceError(ErrorCode.SERVICE_USER_PASS_WRONG)
    else:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)

    uid = user.to_dict()['user_id']
    if 'ip' in kw:
        query_user_add_login(uid, ip=kw['ip'])
    return query_user_get_by_id(uid)[0].to_dict()


def service_user_update_info(**kw):
    get_db()
    kw['service'] = 'user'
    kw = util_pattern_format_param(**kw)
    if 'user_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_USER_ID)
    if 'user_status' in kw:
        query_user_update_status(kw['user_id'], kw['user_status'])
    if 'user_name' in kw:
        query_user_update_name(kw['user_id'], kw['user_name'])
    if 'user_password' in kw:
        query_user_update_password(kw['user_id'], kw['user_password'])
    if 'user_thumbnail' in kw:
        query_user_update_thumbnail(kw['user_id'], kw['user_thumbnail'])
    query_user_update_details(**kw)
    return query_user_get_by_id(kw['user_id'])[0].to_dict()


def service_user_close(**kw):
    get_db()
    kw['service'] = 'user'
    kw = util_pattern_format_param(**kw)
    if 'user_id' not in kw:
        raise ServiceError(ErrorCode.SERVICE_MISSING_USER_ID)

    videos = query_video_get_by_user_id(kw['user_id'])
    ops = query_video_op_get_by_user_id(kw['user_id'])

    # delete by setting status
    if 'method' in kw and kw['method'] == 'status':
        res = query_user_update_status(kw['user_id'], 'closed')
        for video in videos:
            vid = video.to_dict()['video_id']
            service_video_delete(video_id=vid, method='status')

    # delete by removing from databse
    else:
        res = query_user_delete_by_id(kw['user_id'])
        for video in videos:
            vid = video.to_dict()['video_id']
            service_video_delete(video_id=vid)

    # delete all op created by this user immediately
    for op in ops:
        opid = op.to_dict()['video_op_id']
        query_video_op_delete(opid, silent=True)

    return res


def service_user_hide_private(user):
    hide = '[Private User]'
    user['user_detail']['user_city'] = hide
    user['user_detail']['user_country'] = hide
    user['user_detail']['user_first_name'] = hide
    user['user_detail']['user_last_name'] = hide
    user['user_detail']['user_phone'] = hide
    user['user_detail']['user_state'] = hide
    user['user_detail']['user_street1'] = hide
    user['user_detail']['user_street2'] = hide
    user['user_detail']['user_zip'] = hide
    user['user_email'] = hide
    user['user_following'] = []
    user['user_login'] = []
    return user


def service_user_get_user(user_id):
    get_db()

    # user_id check
    if not is_valid_id(user_id):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    users = query_user_get_by_id(user_id)
    if len(users) == 0:
        raise ServiceError(ErrorCode.SERVICE_USER_NOT_FOUND)

    user_array = util_serializer_mongo_results_to_array(users)
    return user_array[0]


def service_user_get_like(user_id):
    get_db()

    # user_id check
    if not is_valid_id(user_id):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    if len(query_user_get_by_id(user_id)) <= 0:
        raise ServiceError(ErrorCode.SERVICE_USER_NOT_FOUND)

    # perform db operations and get result
    search_mongo = query_video_op_get_by_user_id(user_id)
    if len(search_mongo) == 0:
        return []

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


def service_user_get_dislike(user_id):
    get_db()

    # user_id check
    if not is_valid_id(user_id):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    if len(query_user_get_by_id(user_id)) <= 0:
        raise ServiceError(ErrorCode.SERVICE_USER_NOT_FOUND)

    # perform db operations and get result
    search_mongo = query_video_op_get_by_user_id(user_id)
    if len(search_mongo) == 0:
        return []

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


def service_user_get_comment(user_id):
    get_db()

    # user_id check
    if not is_valid_id(user_id):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    if len(query_user_get_by_id(user_id)) <= 0:
        raise ServiceError(ErrorCode.SERVICE_USER_NOT_FOUND)

    # perform db operations and get result
    search_mongo = query_video_op_get_by_user_id(user_id)
    if len(search_mongo) == 0:
        return []

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


def service_user_get_star(user_id):
    get_db()

    # user_id check
    if not is_valid_id(user_id):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    if len(query_user_get_by_id(user_id)) <= 0:
        raise ServiceError(ErrorCode.SERVICE_USER_NOT_FOUND)

    # perform db operations and get result
    search_mongo = query_video_op_get_by_user_id(user_id)
    if len(search_mongo) == 0:
        return []

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


def service_user_get_process(user_id):
    get_db()

    # user_id check
    if not is_valid_id(user_id):
        raise ServiceError(ErrorCode.SERVICE_INVALID_ID_OBJ)

    if len(query_user_get_by_id(user_id)) <= 0:
        raise ServiceError(ErrorCode.SERVICE_USER_NOT_FOUND)

    # perform db operations and get result
    search_mongo = query_video_op_get_by_user_id(user_id)
    if len(search_mongo) == 0:
        return []

    search_result = util_serializer_mongo_results_to_array(search_mongo)

    process_result = []
    for each in search_result:
        if each["process"] != 0:
            process_result.append({
                "video_id": each["video_id"],
                "user_id": each["user_id"],
                "process": str(each["process"]),
                "process_date": str(each["process_date"])
            })

    return process_result

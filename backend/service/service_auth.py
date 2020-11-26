from db.query_user import query_user_get_by_id
from db.query_video import query_video_get_by_video_id
from models.model_errors import ErrorCode, ServiceError


def service_auth_user_get(token, user_id):
    users = query_user_get_by_id(user_id)
    if len(users) == 0:
        raise ServiceError(ErrorCode.SERVICE_USER_NOT_FOUND)
    user = users[0].to_dict()
    if user['user_status'] == 'public' or token == user_id:
        return True
    return False


def service_auth_user_modify(token, user_id):
    return token == user_id


def service_auth_video_get(token, video_id):
    videos = query_video_get_by_video_id(video_id)
    if len(videos) == 0:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_NOT_FOUND)
    video = videos[0].to_dict()
    user = video['user_id']
    status = video['video_status']
    raw = video['video_raw_status']
    if status != 'public' and user != token:
        return False
    if raw != 'streaming' and user != token:
        return False
    return True


def service_auth_video_modify(token, video_id):
    videos = query_video_get_by_video_id(video_id)
    if len(videos) == 0:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_NOT_FOUND)
    video = videos[0].to_dict()
    if video['user_id'] == token:
        return True
    return False


def service_auth_video_op_get(token, user_id, video_id):
    videos = query_video_get_by_video_id(video_id)
    if len(videos) == 0:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_NOT_FOUND)
    video = videos[0].to_dict()

    if video['video_status'] != 'public' and \
       video['user_id'] != token and \
       user_id != token:
        return False

    return True


def service_auth_video_op_post(token, user_id, video_id):
    videos = query_video_get_by_video_id(video_id)
    if len(videos) == 0:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_NOT_FOUND)
    video = videos[0].to_dict()
    if video['video_status'] != 'public' and \
       video['user_id'] != token:
        return False
    if token != user_id:
        return False
    return True


def service_auth_video_op_modify(token, user_id):
    return token == user_id


# Search Hide Caller
def service_auth_hide_video(user, results):
    ret = []
    if user is None:
        user = ""
    if len(results) == 0:
        return []
    for video in results:
        if video['video_status'] == 'deleted' or \
           video['video_raw_status'] != 'streaming':
            continue
        if video['video_status'] == 'public' or video['user_id'] == user:
            ret.append(video)
    return ret


def service_auth_hide_user(user, results):
    ret = []
    if user is None:
        user = ""
    for user in results:
        if user['user_status'] == 'closed':
            continue
        ret.append(user)
    return ret

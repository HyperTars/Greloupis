def service_video_auth_get(token, video_id):
    video = query_video_get_by_video_id(video_id)
    if len(videos) == 0:
        raise ServiceError(ErrorCode.SERVICE_VIDEO_NOT_FOUND)
    v = video[0].to_dict()
    user = v['user_id']
    status = v['video_status']
    if status != 'public' and user != token:
        return false
    return true



def service_video_auth_required():


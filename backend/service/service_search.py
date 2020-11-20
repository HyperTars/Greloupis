from settings import config
from db.query_user import query_user_search_by_aggregate, \
    query_user_search_by_pattern, query_user_search_by_contains, \
    query_user_get_by_id
from db.query_video import query_video_search_by_contains, \
    query_video_search_by_aggregate, query_video_search_by_pattern
from utils.util_pattern import util_pattern_build, \
    util_pattern_format_param, util_pattern_slice
from utils.util_serializer import util_serializer_mongo_results_to_array, \
    util_serializer_dict_to_json
from models.model_errors import ServiceError, ErrorCode


#########################
# Service Search Caller #
#########################
# TODO: add search all (including search video by comment content, uploader,
#  etc.)
# TODO: by comment: search VideoOp.comment -> video_id -> Video.video_id
# TODO: by uploader: search User.user_id -> user_id -> Video.user_id
# Search User Caller
def service_search_user(**kw):

    conf = config['base']
    kw['service'] = 'user'
    kw = util_pattern_format_param(**kw)

    # Search configs
    if 'slice' in kw and kw['slice'] is True:
        raise ServiceError(ErrorCode.SERVICE_PARAM_SLICE_NOT_SUPPORT)
    if 'ignore_case' not in kw:
        kw['ignore_case'] = conf.SEARCH_IGNORE_CASE
    if 'exact' not in kw:
        kw['exact'] = conf.SEARCH_EXACT

    # TODO: add typo allowance, etc.

    # Search
    # TODO: Support aggregation pipeline, etc.
    if kw['ignore_case'] is False or kw['exact'] is True \
            or 'pattern' in kw and kw['pattern'] is True:
        kw = util_pattern_build(**kw)
        res_search = service_search_user_by_pattern(**kw)
    elif 'aggregate' in kw and kw['aggregate'] is True:
        res_search = service_search_user_by_aggregation(**kw)
        return res_search
    else:
        res_search = service_search_user_by_contains(**kw)

    # Convert to json (if format="json")
    if 'json' in kw and kw['json'] is True \
            or 'dict' in kw and kw['dict'] is False \
            or 'format' in kw and kw['format'] == "json":
        res_array = util_serializer_mongo_results_to_array(
            res_search, format="json")
    else:
        res_array = util_serializer_mongo_results_to_array(res_search)
    return res_array


# Search Video Caller
def service_search_video(**kw):

    conf = config['base']
    kw['service'] = 'video'
    kw = util_pattern_format_param(**kw)

    # Search configs
    if 'slice' not in kw:
        kw['slice'] = conf.SEARCH_SLICE
    if 'ignore_case' not in kw:
        kw['ignore_case'] = conf.SEARCH_IGNORE_CASE
    if 'exact' not in kw:
        kw['exact'] = conf.SEARCH_EXACT
    # TODO: add typo allowance, etc.

    # Search
    # TODO: Support aggregation pipeline
    if kw['ignore_case'] is False or kw['exact'] is True or kw['slice']\
            is True:
        kw = util_pattern_slice(**kw)
        kw = util_pattern_build(**kw)
        res_search = service_search_video_by_pattern(**kw)
    elif 'pattern' in kw and kw['pattern'] is True:
        # Pattern search
        kw = util_pattern_build(**kw)
        res_search = service_search_video_by_pattern(**kw)
    elif 'aggregate' in kw and kw['aggregate'] is True:
        # Aggregate search
        res_search = service_search_video_by_aggregation(**kw)
        for res in res_search:
            res['video_id'] = str(res['_id'])
            res.pop('_id')

        for res in res_search:
            user = query_user_get_by_id(res['user_id'])[0]
            res['user_name'] = user.user_name

        return res_search
    else:
        # Contains keyword (single) search
        res_search = service_search_video_by_contains(**kw)

    res_array = util_serializer_mongo_results_to_array(res_search)

    for res in res_array:
        user = query_user_get_by_id(res['user_id'])[0]
        res['user_name'] = user.user_name
    # Convert to json (if format="json")
    if 'json' in kw and kw['json'] is True \
            or 'dict' in kw and kw['dict'] is False \
            or 'format' in kw and kw['format'] == "json":
        return util_serializer_dict_to_json(res_array)

    # default format="dict"
    return res_array


# Search Hide Caller
def service_search_hide_video(user, results):
    ret = []
    if user is None:
        user = ""
    if len(results) == 0:
        return []
    for video in results:
        if video['video_status'] == 'deleted':
            continue
        if video['video_status'] == 'public' or video['user_id'] == user:
            ret.append(video)
    return ret


def service_search_hide_user(user, results):
    ret = []
    if user is None:
        user = ""
    for user in results:
        if user['user_status'] == 'closed':
            continue
        ret.append(user)
    return ret


###########
# Helpers #
###########
# Search by contains
def service_search_user_by_contains(**kw):
    """
    choose one attribute to search one keyword, case sensitive
    :param user_name: (optional) single keyword of username to be searched
    :param user_email: (optional) single keyword of email to be searched
    :return: array of searching results
    """
    if 'user_id' in kw:
        return query_user_search_by_contains(user_id=kw['user_id'])
    elif 'user_name' in kw:
        return query_user_search_by_contains(user_name=kw['user_name'])
    elif 'user_email' in kw:
        return query_user_search_by_contains(user_email=kw['user_email'])
    elif 'user_first_name' in kw:
        return query_user_search_by_contains(
            user_first_name=kw['user_first_name'])
    elif 'user_last_name' in kw:
        return query_user_search_by_contains(
            user_last_name=kw['user_last_name'])
    elif 'user_phone' in kw:
        return query_user_search_by_contains(user_phone=kw['user_phone'])
    elif 'user_street1' in kw:
        return query_user_search_by_contains(user_street1=kw['user_street1'])
    elif 'user_street2' in kw:
        return query_user_search_by_contains(user_street2=kw['user_street2'])
    elif 'user_city' in kw:
        return query_user_search_by_contains(user_city=kw['user_city'])
    elif 'user_state' in kw:
        return query_user_search_by_contains(user_state=kw['user_state'])
    elif 'user_country' in kw:
        return query_user_search_by_contains(user_country=kw['user_country'])
    elif 'user_zip' in kw:
        return query_user_search_by_contains(user_zip=kw['user_zip'])
    elif 'user_status' in kw:
        return query_user_search_by_contains(user_status=kw['user_status'])

    raise ServiceError(ErrorCode.SERVICE_INVALID_SEARCH_PARAM)


def service_search_video_by_contains(**kw):
    """
    Currently support searching 'id', 'title', 'channel', 'category', 'tag'
    :param kw:
    :return:
    """
    if 'video_id' in kw:
        return query_video_search_by_contains(video_id=kw['video_id'])
    elif 'video_title' in kw:
        return query_video_search_by_contains(video_title=kw['video_title'])
    elif 'video_channel' in kw:
        return query_video_search_by_contains(
            video_channel=kw['video_channel'])
    elif 'video_category' in kw:
        return query_video_search_by_contains(
            video_category=kw['video_category'])
    elif 'video_tag' in kw:
        return query_video_search_by_contains(video_tag=kw['video_tag'])
    elif 'video_description' in kw:
        return query_video_search_by_contains(
            video_description=kw['video_description'])

    raise ServiceError(ErrorCode.SERVICE_INVALID_SEARCH_PARAM)


# Search by pattern
def service_search_user_by_pattern(**kw):
    if 'user_name' in kw:
        return query_user_search_by_pattern(pattern_name=kw['user_name'])
    elif 'user_email' in kw:
        return query_user_search_by_pattern(pattern_email=kw['user_email'])
    elif 'user_first_name' in kw:
        return query_user_search_by_pattern(
            pattern_first_name=kw['user_first_name'])
    elif 'user_last_name' in kw:
        return query_user_search_by_pattern(
            pattern_last_name=kw['user_last_name'])
    elif 'user_phone' in kw:
        return query_user_search_by_pattern(pattern_phone=kw['user_phone'])
    elif 'user_street1' in kw:
        return query_user_search_by_pattern(pattern_street1=kw['user_street1'])
    elif 'user_street2' in kw:
        return query_user_search_by_pattern(pattern_street2=kw['user_street2'])
    elif 'user_city' in kw:
        return query_user_search_by_pattern(pattern_city=kw['user_city'])
    elif 'user_state' in kw:
        return query_user_search_by_pattern(pattern_state=kw['user_state'])
    elif 'user_country' in kw:
        return query_user_search_by_pattern(pattern_country=kw['user_country'])
    elif 'user_zip' in kw:
        return query_user_search_by_pattern(pattern_zip=kw['user_zip'])
    elif 'user_status' in kw:
        return query_user_search_by_pattern(pattern_status=kw['user_status'])

    raise ServiceError(ErrorCode.SERVICE_PATTERN_SEARCH_NOT_SUPPORT)


def service_search_video_by_pattern(**kw):
    if 'video_title' in kw:
        return query_video_search_by_pattern(pattern_title=kw['video_title'])
    elif 'video_channel' in kw:
        return query_video_search_by_pattern(
            pattern_channel=kw['video_channel'])
    elif 'video_description' in kw:
        return query_video_search_by_pattern(
            pattern_description=kw['video_description'])

    raise ServiceError(ErrorCode.SERVICE_PATTERN_SEARCH_NOT_SUPPORT)


# Search by aggregate
def service_search_user_by_aggregation(search_dict=None, **kw):
    # Search by aggregate (can search multi attributes)
    if search_dict is None and len(kw) == 0:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)
    return query_user_search_by_aggregate(search_dict)


def service_search_video_by_aggregation(search_dict=None, **kw):
    # Search by aggregate (can search multi attributes)
    if search_dict is None and len(kw) == 0:
        raise ServiceError(ErrorCode.SERVICE_MISSING_PARAM)
    return query_video_search_by_aggregate(search_dict)

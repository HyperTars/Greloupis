import re

from source.configs import *
from source.db.mongo import get_db
from source.db.query_user import *
from source.db.query_video import *
from source.utils.util_pattern import *
from source.utils.util_serializer import *


#########################
# Service Search Caller #
#########################
# TODO: add search all (including search video by comment content, uploader, etc.)
# TODO: by comment: search VideoOp.comment -> video_id -> Video.video_id
# TODO: by uploader: search User.user_id -> user_id -> Video.user_id

# Search User Caller
def service_search_user(conf, **kw):
    db = get_db(conf)
    kw['search'] = 'user'
    kw = util_pattern_format_search_param(**kw)

    # Search configs
    if 'slice' in kw and kw['slice'] is True:
        return ErrorCode.SERVICE_PARAM_SLICE_NOT_SUPPORT
    if 'ignore_case' not in kw:
        kw['ignore_case'] = conf.SEARCH_IGNORE_CASE
    if 'exact' not in kw:
        kw['exact'] = conf.SEARCH_EXACT

    # TODO: add typo allowance, etc.

    # Search
    # TODO: Support aggregation pipeline, etc.
    if kw['ignore_case'] is False or kw['exact'] is True:
        kw = util_pattern_build(**kw)
        res_search = service_search_user_by_pattern(**kw)
    elif 'pattern' in kw and kw['pattern'] is True:
        res_search = service_search_user_by_pattern(**kw)
    elif 'aggregate' in kw and kw['aggregate'] is True:
        res_search = service_search_user_by_aggregation(**kw)
    else:
        res_search = service_search_user_by_contains(**kw)

    # Convert to dict
    res_array = util_serializer_mongo_results_to_array(res_search)

    # Remove password
    for res in res_array:
        if 'user_password' in res:
            res.pop('user_password')

    # Convert to json (if format="json")
    if 'json' in kw and kw['json'] is True \
            or 'dict' in kw and kw['dict'] is False \
            or 'format' in kw and kw['format'] == "json":
        return util_serializer_array_dict_to_json(res_array)

    return res_array


# Search Video Caller
def service_search_video(conf, **kw):
    db = get_db(conf)
    kw['search'] = 'video'
    kw = util_pattern_format_search_param(**kw)

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
    if kw['ignore_case'] is False or kw['exact'] is True or kw['slice'] is True:
        kw = util_pattern_slice(**kw)
        kw = util_pattern_build(**kw)
        res_search = service_search_video_by_pattern(**kw)
    elif 'pattern' in kw and kw['pattern'] is True:
        res_search = service_search_video_by_pattern(**kw)  # Pattern search
    elif 'aggregate' in kw and kw['aggregate'] is True:
        res_search = service_search_video_by_aggregation(**kw)  # Aggregate search
    else:
        res_search = service_search_video_by_contains(**kw)  # Contains keyword (single) search

    # Convert to dict
    res_array = util_serializer_mongo_results_to_array(res_search)

    # Convert to json (if format="json")
    if 'json' in kw and kw['json'] is True \
            or 'dict' in kw and kw['dict'] is False \
            or 'format' in kw and kw['format'] == "json":
        return util_serializer_array_dict_to_json(res_array)

    return res_array


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
        return query_user_search_by_contains(user_first_name=kw['user_first_name'])
    elif 'user_last_name' in kw:
        return query_user_search_by_contains(user_last_name=kw['user_last_name'])
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
    elif 'user_reg_date' in kw:
        return query_user_search_by_contains(user_reg_date=kw['user_reg_date'])

    return ErrorCode.MONGODB_INVALID_SEARCH_PARAM


def service_search_video_by_contains(**kw):
    """
    Currently support searching 'id', 'title', 'channel', 'category', 'tag' of videos
    :param kw:
    :return:
    """
    if 'video_id' in kw:
        return query_video_search_by_contains(video_id=kw['video_id'])
    elif 'video_title' in kw:
        return query_video_search_by_contains(video_title=kw['video_title'])
    elif 'video_channel' in kw:
        return query_video_search_by_contains(video_channel=kw['video_channel'])
    elif 'video_category' in kw:
        return query_video_search_by_contains(video_category=kw['video_category'])
    elif 'video_tag' in kw:
        return query_video_search_by_contains(video_tag=kw['video_tag'])
    elif 'video_description' in kw:
        return query_video_search_by_contains(video_description=kw['video_description'])

    return ErrorCode.SERVICE_PATTERN_SEARCH_NOT_SUPPORT


# Search by pattern
def service_search_user_by_pattern(**kw):
    if kw['ignore_case'] is False or kw['exact'] is True:
        if 'user_name' in kw:
            return query_user_search_by_pattern(pattern_name=kw['user_name'])
        elif 'user_email' in kw:
            return query_user_search_by_pattern(pattern_email=kw['user_email'])
        elif 'user_first_name' in kw:
            return query_user_search_by_pattern(pattern_first_name=kw['user_first_name'])
        elif 'user_last_name' in kw:
            return query_user_search_by_pattern(pattern_last_name=kw['user_last_name'])
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
        elif 'user_reg_date' in kw:
            return query_user_search_by_pattern(pattern_reg_date=kw['user_reg_date'])

    elif 'pattern' in kw and kw['pattern'] is True:
        if 'user_name' in kw:
            return query_user_search_by_pattern(pattern_name=re.compile(kw['user_name']))
        elif 'user_email' in kw:
            return query_user_search_by_pattern(pattern_email=re.compile(kw['user_email']))
        elif 'user_first_name' in kw:
            return query_user_search_by_pattern(pattern_first_name=re.compile(kw['user_first_name']))
        elif 'user_last_name' in kw:
            return query_user_search_by_pattern(pattern_last_name=re.compile(kw['user_last_name']))
        elif 'user_phone' in kw:
            return query_user_search_by_pattern(pattern_phone=re.compile(kw['user_phone']))
        elif 'user_street1' in kw:
            return query_user_search_by_pattern(pattern_street1=re.compile(kw['user_street1']))
        elif 'user_street2' in kw:
            return query_user_search_by_pattern(pattern_street2=re.compile(kw['user_street2']))
        elif 'user_city' in kw:
            return query_user_search_by_pattern(pattern_city=re.compile(kw['user_city']))
        elif 'user_state' in kw:
            return query_user_search_by_pattern(pattern_state=re.compile(kw['user_state']))
        elif 'user_country' in kw:
            return query_user_search_by_pattern(pattern_country=re.compile(kw['user_country']))
        elif 'user_zip' in kw:
            return query_user_search_by_pattern(pattern_zip=re.compile(kw['user_zip']))
        elif 'user_status' in kw:
            return query_user_search_by_pattern(pattern_status=re.compile(kw['user_status']))
        elif 'user_reg_date' in kw:
            return query_user_search_by_pattern(pattern_reg_date=re.compile(kw['user_reg_date']))

    return ErrorCode.MONGODB_INVALID_SEARCH_PARAM


def service_search_video_by_pattern(**kw):
    if kw['ignore_case'] is False or kw['exact'] is True or kw['slice'] is True:
        if 'video_title' in kw:
            return query_video_search_by_pattern(pattern_title=kw['video_title'])
        elif 'video_channel' in kw:
            return query_video_search_by_pattern(pattern_channel=kw['video_channel'])
        elif 'video_description' in kw:
            return query_video_search_by_pattern(pattern_description=kw['video_description'])

    elif 'pattern' in kw and kw['pattern'] is True:
        if 'video_title' in kw:
            return query_video_search_by_pattern(pattern_title=re.compile(kw['video_title']))
        elif 'video_channel' in kw:
            return query_video_search_by_pattern(pattern_channel=re.compile(kw['video_channel']))
        elif 'video_description' in kw:
            return query_video_search_by_pattern(pattern_description=re.compile(kw['video_description']))

    return ErrorCode.SERVICE_PATTERN_SEARCH_NOT_SUPPORT


# Search by aggregate
def service_search_user_by_aggregation(**kw):
    # Search by aggregate (can search multi attributes)
    """
    example:
    pipeline1 = [
        { "$match":
            {
                "user_name": {"$regex": "es"},
                "user_status": "active"
            }
        }
    ]
    pipeline2 = [
        { "$unwind": "$user_detail" },
        { "$match":
            {
                "user_detail.street1": {"$regex": "343"},
                "user_status": "public"
            }
        }
    ]
    """
    search_dict = {}

    return query_user_search_by_aggregate(search_dict)


def service_search_video_by_aggregation(**kw):
    # Search by aggregate (can search multi attributes)
    """
    example:
    pipeline1 = [
        { "$match":
            {
                "user_name": {"$regex": "es"}, 
                "user_status": "active" 
            }
        }
    ]
    pipeline2 = [
        { "$unwind": "$user_detail" },
        { "$match":
            { 
                "user_detail.street1": {"$regex": "343"}, 
                "user_status": "public" 
            }
        }
    ]
    """
    search_dict = {}
    return query_video_search_by_aggregate(search_dict)

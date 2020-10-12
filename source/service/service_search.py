import re

from source.config import *
from source.db.mongo import get_db
from source.db.query_user import *
from source.db.query_video import *
from source.utils.util_pattern import *
from source.utils.util_serializer import *


#########################
# Service Search Caller #
#########################

# Search User Caller
def service_search_user(conf=config['default'], **kw):
    db = get_db(conf)

    # Search configs
    if 'ignore_case' not in kw:
        kw['ignore_case'] = conf.SEARCH_IGNORE_CASE
    if 'exact' not in kw:
        kw['exact'] = conf.SEARCH_EXACT

    # TODO: add typo allowance, etc.

    # Search
    # res_search = service_search_video_by_keyword(**kw)
    res_search = service_search_user_by_pattern(**kw)
    # res_search = query_user_search_aggregate(**kw)

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
def service_search_video(conf=config['default'], **kw):
    db = get_db(conf)

    # Search configs
    if 'ignore_case' not in kw:
        kw['ignore_case'] = conf.SEARCH_IGNORE_CASE
    if 'exact' not in kw:
        kw['exact'] = conf.SEARCH_EXACT
    # TODO: add typo allowance, etc.

    # Search
    # TODO: Aggregation Pipeline
    if 'description' not in kw or 'video_description' not in kw:
        res_search = service_search_video_by_keyword(**kw)  # id, title, channel, category, tag
    elif 'title' in kw or 'video_title' in kw or 'description' in kw or 'video_description' in kw:
        res_search = service_search_video_by_pattern(**kw)  # title, description
    # res_search = service_search_video_by_aggregation(**kw) # Advanced search

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
def service_search_user_by_keyword(**kw):
    """
    choose one attribute to search one keyword, case sensitive
    :param name (optional): single keyword of username to be searched
    :param email (optional): single keyword of email to be searched
    :return: array of searching results
    """
    if 'name' in kw:
        return query_user_search_keyword(keyword_name=kw['name'])
    elif 'email' in kw:
        return query_user_search_keyword(keyword_email=kw['email'])

    return ErrorCode.MONGODB_INVALID_SEARCH_PARAM


def service_search_user_by_pattern(**kw):
    pattern = util_pattern_compile(**kw)

    if 'name' in kw:
        return query_user_search_pattern(pattern_name=pattern)

    elif 'email' in kw:
        return query_user_search_pattern(pattern_email=pattern)

    return ErrorCode.MONGODB_INVALID_SEARCH_PARAM


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

    return query_user_search_aggregate(search_dict)


def service_search_video_by_keyword(**kw):
    """
    Currently support searching 'id', 'title', 'channel', 'category', 'tag' of videos
    :param kw:
    :return:
    """
    if 'id' in kw:
        return query_video_search_by_contains(video_id=kw['id'])
    elif '_id' in kw:
        return query_video_search_by_contains(video_id=kw['_id'])
    elif 'video_id' in kw:
        return query_video_search_by_contains(video_id=kw['video_id'])
    elif 'title' in kw:
        return query_video_search_by_contains(video_title=kw['title'])
    elif 'video_title' in kw:
        return query_video_search_by_contains(video_title=kw['video_title'])
    elif 'channel' in kw:
        return query_video_search_by_contains(video_channel=kw['channel'])
    elif 'video_channel' in kw:
        return query_video_search_by_contains(video_channel=kw['video_channel'])
    elif 'category' in kw:
        return query_video_search_by_contains(video_category=kw['category'])
    elif 'video_category' in kw:
        return query_video_search_by_contains(video_category=kw['video_category'])
    elif 'tag' in kw:
        return query_video_search_by_contains(video_tag=kw['tag'])
    elif 'video_tag' in kw:
        return query_video_search_by_contains(video_tag=kw['video_tag'])

    return ErrorCode.MONGODB_INVALID_SEARCH_PARAM


def service_search_video_by_pattern(**kw):
    """
    Currently support searching 'title' and 'description'
    :param title or video_title: (optional) title of video
    :param description or video_description: (optional) description of videos
    :return array of searching results (Video Model):
    """
    pattern = util_pattern_compile(**kw)

    if 'title' in kw or 'video_title' in kw:
        return query_video_search_by_pattern(pattern_title=pattern)
    elif 'description' in kw or 'video_description' in kw:
        return query_video_search_by_pattern(pattern_description=pattern)

    return ErrorCode.MONGODB_INVALID_SEARCH_PARAM


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

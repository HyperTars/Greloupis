import re

from source.config import *
from source.db.mongo import get_db
from source.db.query_user import *
from source.db.query_video import *
from source.utils.util_pattern import *
from source.utils.util_serializer import *


# Service Search User
def service_search_user(conf=config['default'], **kw):
    db = get_db(conf)
    res_ret = []
    res_search = None

    # Search configs
    if 'ignore_case' not in kw:
        kw['ignore_case'] = conf.SEARCH_IGNORE_CASE
    if 'exact' not in kw:
        kw['exact'] = conf.SEARCH_EXACT
    format = conf.DATA_FORMAT
    if 'json' in kw and kw['json'] is True \
            or 'dict' in kw and kw['dict'] is False \
            or 'format' in kw and kw['format'] == "json":
        format = "json"
    # TODO: add typo allowance, etc.

    # Search
    # res_search = service_search_video_by_keyword(**kw)
    res_search = service_search_user_by_pattern(**kw)
    # res_search = query_user_search_aggregate(**kw)

    # Re-construct return data type
    res_ret = util_serializer_mongo_results_to_array(res_search, format=format)

    return res_ret


# Service Search Video
def service_search_video(conf=config['default'], **kw):
    db = get_db(conf)
    res_ret = []
    res_search = None

    # Search configs
    if 'ignore_case' not in kw:
        kw['ignore_case'] = conf.SEARCH_IGNORE_CASE
    if 'exact' not in kw:
        kw['exact'] = conf.SEARCH_EXACT
    format = conf.DATA_FORMAT
    if 'json' in kw and kw['json'] is True \
            or 'dict' in kw and kw['dict'] is False \
            or 'format' in kw and kw['format'] == "json":
        format = "json"
    # TODO: add typo allowance, etc.

    # Search
    # TODO: Aggregation Pipeline
    # res_search = service_search_video_by_keyword(**kw)
    res_search = service_search_video_by_pattern(**kw)
    # res_search = service_search_video_by_aggregation(**kw)

    # Re-construct return data type
    # Re-construct return data type
    res_ret = util_serializer_mongo_results_to_array(res_search, format=format)

    return res_ret


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
    """
    pipeline2 = [
        { "$unwind": "$user_detail" },
        { "$match":
            { 
                "user_detail.street1": {"$regex": "343"}, 
                "user_status": "public" 
            }
        }
    ]
    print(query_user_search_aggregate(pipeline2))

    return query_user_search_aggregate(pipeline2)


def service_search_video_by_keyword(**kw):
    if 'title' in kw:
        return query_video_search_keyword(kw['title'])


def service_search_video_by_pattern(**kw):
    pattern = util_pattern_compile(**kw)

    if 'title' in kw:
        return query_video_search_pattern(pattern_title=pattern)

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
    return query_video_search_aggregate()

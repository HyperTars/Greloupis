import re

from source.config import *
from source.db.mongo import get_db
from source.db.query_user import *
from source.db.query_video import *
from source.utils.util_pattern import *


def service_search_user(Config, **kw):
    db = get_db(Config)
    res_ret = []
    res_search = None

    # Search configs
    if 'ignore_case' not in kw:
        kw['ignore_case'] = Config.SEARCH_IGNORE_CASE
    if 'exact' not in kw:
        kw['exact'] = Config.SEARCH_EXACT

    # Search
    # res_search = service_search_video_by_keyword(**kw)
    res_search = service_search_user_by_pattern(**kw)
    # res_search = query_user_search_aggregate(**kw)

    # Re-construct return data type
    for res_s in res_search:
        if 'json' in kw and kw['json'] is True \
                or 'dict' in kw and kw['dict'] is False \
                or 'type' in kw and kw['type'] == "json":
            res_ret.append(res_s.to_json())
        else:
            res_ret.append(res_s.to_dict())

    return res_ret


def service_search_video(Config, **kw):
    db = get_db(Config)
    res_ret = []
    res_search = None

    # Search configs
    if 'ignore_case' not in kw:
        kw['ignore_case'] = Config.SEARCH_IGNORE_CASE
    if 'exact' not in kw:
        kw['exact'] = Config.SEARCH_EXACT

    # Search
    # TODO: Pattern & Case Ignore & Aggregation Pipeline
    if 'title' in kw:
        res_search = service_search_video_by_keyword(title=kw['title'])
    else:
        return ErrorCode.MONGODB_INVALID_SEARCH_PARAM

    # Re-construct return data type
    for res_s in res_search:
        if 'json' in kw and kw['json'] == True \
                or 'dict' in kw and kw['dict'] == False \
                or 'type' in kw and kw['type'] == "json":
            res_ret.append(res_s.to_json())
        else:
            res_ret.append(res_s.to_dict())

    return res_ret


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


def service_search_user_by_aggregation(pipeline):
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
    print(query_user_search_aggregate(pipeline2))
    """
    return query_user_search_aggregate(pipeline)


def service_search_video_by_keyword(**kw):
    if 'title' in kw:
        return query_video_search_keyword(kw['title'])


def service_search_video_by_pattern(**kw):
    # Search by pattern (can ignore case)
    pattern_string = ""
    ignore_case = True

    # Construct pattern string
    if 'title' in kw:
        pattern_string = kw['title']
    # TODO: add more attr search support
    else:
        return ErrorCode.MONGODB_INVALID_SEARCH_PARAM
    
    # Pattern flags
    if ('like' in kw and kw['like'] is False) or ('exact' in kw and kw['exact'] is True):
        pattern_string = '\\b' + pattern_string + '\\b'
    else:
        pattern_string = '.*' + pattern_string + '.*'
    # TODO: allow typo, allow slice

    # Compile pattern string
    pattern = re.compile(pattern_string)
    if 'ignore_case' in kw and kw['ignore_case'] == True:
        pattern = re.compile(pattern_string, re.IGNORECASE)

    return res_ret


def service_search_video_by_aggregation(pipeline):
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
    return query_video_search_aggregate(pipeline)

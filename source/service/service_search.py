from source.db.query_user import *
from source.db.query_video import *
from source.config import *
from source.db.mongo import get_db
import re
import flask_mongoengine

def search_user(**kw):
    db = get_db(DevConfig)
    res_ret = []
    res_search = None

    # Search configs
    ignore_case = DevConfig.IGNORE_CASE
    exact = False
    if 'ignore_case' in kw and kw['ignore_case'] == False:
        ignore_case = False
    if 'exact' in kw and kw['exact'] == True:
        exact = True

    # Seach
    if 'name' in kw:
        res_search = search_user_by_pattern(name=kw['name'], ignore_case=ignore_case, exact=exact)
    elif 'email' in kw:
        res_search = search_user_by_pattern(email=kw['email'], ignore_case=ignore_case, exact=exact)
    else:
        ErrorCode.MONGODB_INVALID_SEARCH_PARAM

    # Re-construct return data type
    for res_s in res_search:
        if 'json' in kw and kw['json'] == True \
            or 'dict' in kw and kw['dict'] == False \
            or 'type' in kw and kw['type'] == "json":
            res_ret.append(res_s.to_json())
        else:
            res_ret.append(res_s.to_dict())

    return res_ret


def search_video(**kw):
    db = get_db(DevConfig)
    res_ret = []
    res_search = None

    # Search configs
    ignore_case = DevConfig.IGNORE_CASE
    exact = False
    if 'ignore_case' in kw and kw['ignore_case'] == False:
        ignore_case = False
    if 'exact' in kw and kw['exact'] == True:
        exact = True

    # Search
    # TODO: Pattern & Case Ignore & Aggregation Pipeline
    if 'title' in kw:
        res_search = search_video_by_keyword(title=kw['title'])
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


def search_user_by_keyword(**kw):
    """
    choose one attribute to search one keyword, case sensitive
    :param name (optional): single keyword of username to be searched
    :param email (optional): single keyword of email to be searched
    :return: array of searching results
    """
    if 'name' in kw:
        return user_search_keyword(keyword_name=kw['name'])
    elif 'email' in kw:
        return user_search_keyword(keyword_email=kw['email'])
    
    return ErrorCode.MONGODB_INVALID_SEARCH_PARAM


def search_user_by_pattern(**kw):
    # Search by pattern (can ignore case)
    pattern_string = ""
    ignore_case = True

    # Construct pattern string
    if 'name' in kw:
        pattern_string = kw['name']
    elif 'email' in kw:
        pattern_string = kw['email']

    # Pattern flags
    if ('like' in kw and kw['like'] == False) or ('exact' in kw and kw['exact'] == True):
        pattern_string = '\\b' + pattern_string + '\\b'
    else:
        pattern_string = '.*' + pattern_string + '.*'
    # TODO: allow typo, allow slice

    # Compile pattern string
    pattern = re.compile(pattern_string)
    if 'ignore_case' in kw and kw['ignore_case'] == True:
        pattern = re.compile(pattern_string, re.IGNORECASE)
        
        
    if 'name' in kw:
        return user_search_pattern(pattern_name=pattern)
    elif 'email' in kw:
        return user_search_pattern(pattern_email=pattern)

    return ErrorCode.MONGODB_INVALID_SEARCH_PARAM


def search_user_by_aggregation(pipeline):
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
    print(user_search_aggregate(pipeline2))
    """
    return user_search_aggregate(pipeline)

def search_video_by_keyword(**kw):
    if 'title' in kw:
        return video_search_keyword(kw['title'])


def search_video_by_pattern():
    res_ret = []
    return res_ret

def search_video_by_aggregation(pipeline):
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
    return video_search_aggregate(pipeline)

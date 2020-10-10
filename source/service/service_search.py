from source.db.query_user import *
from source.db.query_video import *


def search_user_by_keyword(**kw):
    """
    choose one attribute to search one keyword, case sensitive
    :param name (optional): single keyword of username to be searched
    :param email (optional): single keyword of email to be searched
    :return: array of searching results
    """
    res_ret = []
    if 'name' in kw:
        res_search = user_search_keyword(keyword_name=kw['name'])
        for r in res_search:
            res_ret.append(r.to_dict())
        return res_ret
    elif 'email' in kw:
        res_search = user_search_keyword(keyword_email=kw['email'])
        for r in res_search:
            res_ret.append(r.to_dict())
        return res_ret
    return ErrorCode.MONGODB_INVALID_SEARCH_PARAM


def search_user_by_pattern():
    # Search by pattern (can ignore case)
    print(user_search_pattern(re.compile('.*E.*T.*', re.IGNORECASE))) # Ignore case


def search_user_by_aggregation():
    # Search by aggregate (can search multi attributes)
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


def search_video_by_keyword():
    res_ret = []
    return res_ret


def search_video_by_pattern():
    res_ret = []
    return res_ret

def search_video_by_aggregation():
    res_ret = []
    return res_ret

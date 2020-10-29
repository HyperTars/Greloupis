from source.models.model_user import UserDetail, UserLogin, User
from source.models.model_errors import ErrorCode, MongoError
from source.utils.util_time import get_time_now_utc
import bson
import datetime
import re

VALID_USER_STATUS = ["public", "private", "closed"]


##########
# CREATE #
##########
def query_user_create(user_name: str, user_email: str, user_password: str, user_ip="0.0.0.0"):
    """
    :param user_name: user's unique nickname
    :param user_email: user's unique email
    :param user_password: user's password
    :param user_ip: user's ip address (default 0.0.0.0)
    :return: user object if succeeded
    """
    if type(user_name) != str or type(user_email) != str or type(user_password) != str:
        raise MongoError(ErrorCode.MONGODB_STR_EXPECTED)

    if len(query_user_get_by_name(user_name)) > 0:
        raise MongoError(ErrorCode.MONGODB_USER_NAME_TAKEN)

    elif len(query_user_get_by_email(user_email)) > 0:
        raise MongoError(ErrorCode.MONGODB_USER_EMAIL_TAKEN)

    login = [UserLogin(user_login_ip=user_ip, user_login_time=get_time_now_utc())]

    # EmbeddedDocument must be included when creating
    # user_detail, user_reg_date
    user = User(user_name=user_name, user_email=user_email, user_password=user_password,
                user_detail=UserDetail(), user_status="private", user_thumbnail="",
                user_reg_date=get_time_now_utc(), user_login=login,
                user_following=[], user_follower=[])

    return user.save()


############
# RETRIEVE #
############
def query_user_get_by_name(user_name: str):
    """
    :param user_name: user name
    :return: an array of such User, len == 0 if no such user_name, len == 1 if found
    """
    if type(user_name) != str:
        raise MongoError(ErrorCode.MONGODB_STR_EXPECTED)

    return User.objects(user_name=user_name)


def query_user_get_by_email(user_email: str):
    """
    :param user_email: user email
    :return: an array of such User (len == 0 or 1), len == 0 if no such user_email, len == 1 if found
    """
    if type(user_email) != str:
        raise MongoError(ErrorCode.MONGODB_STR_EXPECTED)

    return User.objects(user_email=user_email)


def query_user_get_by_id(user_id: str):
    """
    :param user_id: user id
    :return: an array of such User (len == 0 or 1), len == 0 if no such user_id, len == 1 if found
    """
    if type(user_id) != str:
        raise MongoError(ErrorCode.MONGODB_STR_EXPECTED)

    return User.objects(_id=bson.ObjectId(user_id))


##########
# UPDATE #
##########
def query_user_update_status(user_id: str, user_status: str):
    """
    :param user_id: user's unique id
    :param user_status: user's new status
    :return: array of User Model
    """
    if type(user_id) != str or type(user_status) != str:
        raise MongoError(ErrorCode.MONGODB_STR_EXPECTED)

    if len(query_user_get_by_id(user_id)) == 0:
        raise MongoError(ErrorCode.MONGODB_USER_NOT_FOUND)

    if user_status not in VALID_USER_STATUS:
        raise MongoError(ErrorCode.MONGODB_USER_INVALID_STATUS)

    return User.objects(_id=bson.ObjectId(user_id)).update(user_status=user_status)


def query_user_add_follow(follower_id: str, following_id: str):
    """
    :param follower_id: follower user id
    :param following_id: uploader user_id
    :return: 1 if succeeded
    """
    if type(follower_id) != str or type(following_id) != str:
        raise MongoError(ErrorCode.MONGODB_STR_EXPECTED)

    follower = query_user_get_by_id(follower_id)
    following = query_user_get_by_id(following_id)

    if len(follower) == 0:
        raise MongoError(ErrorCode.MONGODB_FOLLOWER_NOT_FOUND)

    if len(following) == 0:
        raise MongoError(ErrorCode.MONGODB_FOLLOWED_NOT_FOUND)

    if following_id in follower[0].user_following and follower_id in following[0].user_follower:
        raise MongoError(ErrorCode.MONGODB_FOLLOW_REL_EXISTS)

    User.objects(_id=bson.ObjectId(follower_id)).update(add_to_set__user_following=following_id)
    User.objects(_id=bson.ObjectId(following_id)).update(add_to_set__user_follower=follower_id)

    return 1


def query_user_delete_follow(follower_id: str, following_id: str):
    """
    :param follower_id: follower user id
    :param following_id: uploader user_id
    :return: 1 if succeeded
    """

    if type(follower_id) != str or type(following_id) != str:
        raise MongoError(ErrorCode.MONGODB_STR_EXPECTED)

    follower = query_user_get_by_id(follower_id)
    following = query_user_get_by_id(following_id)

    if len(follower) == 0:
        raise MongoError(ErrorCode.MONGODB_FOLLOWER_NOT_FOUND)
    if len(following) == 0:
        raise MongoError(ErrorCode.MONGODB_FOLLOWED_NOT_FOUND)

    User.objects(_id=bson.ObjectId(follower_id)).update(pull__user_following=following_id)
    User.objects(_id=bson.ObjectId(following_id)).update(pull__user_follower=follower_id)

    return 1


def query_user_update_name(user_id: str, user_name: str):
    """
    :param user_id: user's id
    :param user_name: user's name
    :return: array of User Model
    """
    if type(user_id) != str or type(user_name) != str:
        raise MongoError(ErrorCode.MONGODB_STR_EXPECTED)

    users = query_user_get_by_id(user_id)
    if len(users) == 0:
        raise MongoError(ErrorCode.MONGODB_USER_NOT_FOUND)

    old_name = users[0].user_name
    if user_name == old_name:
        raise MongoError(ErrorCode.MONGODB_UPDATE_SAME_NAME)

    if len(query_user_get_by_name(user_name)) > 0:
        raise MongoError(ErrorCode.MONGODB_USER_NAME_TAKEN)

    return User.objects(_id=bson.ObjectId(user_id)).update(user_name=user_name)


def query_user_update_password(user_id: str, user_password: str):
    """
    :param user_id: user's id
    :param user_password: user's password
    :return: array of User Model
    """
    if type(user_id) != str or type(user_password) != str:
        raise MongoError(ErrorCode.MONGODB_STR_EXPECTED)

    users = query_user_get_by_id(user_id)
    if len(users) == 0:
        raise MongoError(ErrorCode.MONGODB_USER_NOT_FOUND)

    old_password = users[0].user_password
    if user_password == old_password:
        raise MongoError(ErrorCode.MONGODB_UPDATE_SAME_PASS)

    return User.objects(_id=bson.ObjectId(user_id)).update(user_password=user_password)


def query_user_update_thumbnail(user_id: str, user_thumbnail: str):
    """
    :param user_id: user's id
    :param user_thumbnail: thumbnail URI
    :return: array of user Model
    """
    if type(user_id) != str or type(user_thumbnail) != str:
        raise MongoError(ErrorCode.MONGODB_STR_EXPECTED)

    users = query_user_get_by_id(user_id)
    if len(users) == 0:
        raise MongoError(ErrorCode.MONGODB_USER_NOT_FOUND)

    User.objects(_id=bson.ObjectId(user_id)).update(user_thumbnail=user_thumbnail)


def query_user_update_details(user_id: str, **kw):
    """
    Update user details
    :param user_id: user unique id
    :param kw:
        :key "user_first_name": (```str```, optional) new user first name
        :key "user_last_name": (```str```, optional) new user last name
        :key "user_phone": (```str```, optional) new user phone
        :key "user_street1": (```str```, optional) new user street1
        :key "user_street2": (```str```, optional) new user street2
        :key "user_city": (```str```, optional) new user city
        :key "user_state": (```str```, optional) new user state
        :key "user_country": (```str```, optional) new user country
        :key "user_zip": (```str```, optional) new user zip
    \nAt least one key must be provided
    :return: 1 if succeeded
    """
    if type(user_id) != str:
        raise MongoError(ErrorCode.MONGODB_STR_EXPECTED)

    for arg in kw:
        if type(kw[arg]) != str:
            raise MongoError(ErrorCode.MONGODB_STR_EXPECTED)

    users = query_user_get_by_id(user_id)
    if len(users) == 0:
        raise MongoError(ErrorCode.MONGODB_USER_NOT_FOUND)

    _id = bson.ObjectId(user_id)

    if 'user_first_name' in kw:
        User.objects(_id=_id).update(set__user_detail__user_first_name=kw['user_first_name'])
    if 'user_last_name' in kw:
        User.objects(_id=_id).update(set__user_detail__user_last_name=kw['user_last_name'])
    if 'user_phone' in kw:
        User.objects(_id=_id).update(set__user_detail__user_phone=kw['user_phone'])
    if 'user_street1' in kw:
        User.objects(_id=_id).update(set__user_detail__user_street1=kw['user_street1'])
    if 'user_street2' in kw:
        User.objects(_id=_id).update(set__user_detail__user_street2=kw['user_street2'])
    if 'user_city' in kw:
        User.objects(_id=_id).update(set__user_detail__user_city=kw['user_city'])
    if 'user_state' in kw:
        User.objects(_id=_id).update(set__user_detail__user_state=kw['user_state'])
    if 'user_country' in kw:
        User.objects(_id=_id).update(set__user_detail__user_country=kw['user_country'])
    if 'user_zip' in kw:
        User.objects(_id=_id).update(set__user_detail__user_zip=kw['user_zip'])

    return 1


def query_user_add_login(user_id: str, ip="0.0.0.0", time=get_time_now_utc()):
    """
    :param user_id: user's unique id
    :param ip: user's login ip address
    :param time: user's login time (utc, optional), default: current system time (utc)
    :return: 1 if succeeded
    """
    if type(user_id) != str or type(ip) != str or type(time) != datetime.datetime:
        raise MongoError(ErrorCode.MONGODB_STR_EXPECTED)

    users = query_user_get_by_id(user_id)
    if len(users) == 0:
        raise MongoError(ErrorCode.MONGODB_USER_NOT_FOUND)

    # only keep 10 login info
    login_history = users[0].user_login
    oldest_login_time = login_history[0].user_login_time
    latest_login_time = login_history[-1].user_login_time
    if len(login_history) >= 10:
        # Delete oldest history
        User.objects(_id=bson.ObjectId(user_id)).update(pull__user_login__user_login_time=oldest_login_time)

    # TODO: update latest 10 login info method, some bugs for current version
    # add new login info
    # print(time)
    # print(latest_login_time)
    if time == latest_login_time:
        raise MongoError(ErrorCode.MONGODB_LOGIN_INFO_EXISTS)
    new_login = {'user_login_ip': ip, 'user_login_time': time}

    User.objects(_id=bson.ObjectId(user_id)).update(add_to_set__user_login=[new_login])

    return 1


##########
# DELETE #
##########
def query_user_delete_by_id(user_id: str, silent=False):
    """
    :param user_id: user's unique id
    :param silent: delete user regardless of existence
    :return: 1 if succeeded
    """
    if type(user_id) != str:
        raise MongoError(ErrorCode.MONGODB_STR_EXPECTED)

    users = query_user_get_by_id(user_id)
    if len(users) == 0 and silent is False:
        raise MongoError(ErrorCode.MONGODB_USER_NOT_FOUND)

    return User.objects(_id=bson.ObjectId(user_id)).delete()


def query_user_delete_by_name(user_name: str, silent=False):
    """
    :param user_name: user's name
    :param silent: delete user regardless of existence
    :return: 1 if succeeded
    """
    if type(user_name) != str:
        raise MongoError(ErrorCode.MONGODB_STR_EXPECTED)

    users = query_user_get_by_name(user_name)
    if len(users) == 0 and silent is False:
        raise MongoError(ErrorCode.MONGODB_USER_NOT_FOUND)

    return User.objects(user_name=user_name).delete()


##########
# SEARCH #
##########
# Search by i-contains
def query_user_search_by_contains(**kw):
    """
    Search user by i-contains (ignore case)
    :param kw: keyword arguments
        :key "user_name": (optional) single keyword of username to be searched
        :key "user_email": (optional) single keyword of email to be searched
        :key "user_first_name": (optional) single keyword of first name to be searched
        :key "user_last_name": (optional) single keyword of last name to be searched
        :key "user_phone": (optional) single keyword of phone to be searched
        :key "user_street1": (optional) single keyword of street1 to be searched
        :key "user_street2": (optional) single keyword of street2 to be searched
        :key "user_city": (optional) single keyword of city to be searched
        :key "user_state": (optional) single keyword of state to be searched
        :key "user_country": (optional) single keyword of country to be searched
        :key "user_zip": (optional) single keyword of zip to be searched
        :key "user_status": (optional) single keyword of status to be searched
        :key "user_reg_date": (optional) single keyword of reg date to be searched
    \nAt least one key must be provided
    :return: array of searching results (User Model)
    """
    if len(kw) == 0:
        raise MongoError(ErrorCode.MONGODB_EMPTY_PARAM)

    for arg in kw:
        if type(kw[arg]) != str:
            raise MongoError(ErrorCode.MONGODB_STR_EXPECTED)

    if 'user_id' in kw:
        return query_user_get_by_id(kw['user_id'])
    elif 'user_name' in kw:
        return User.objects.filter(user_name__icontains=kw['user_name'])
    elif 'user_email' in kw:
        return User.objects.filter(user_email__icontains=kw['user_email'])
    elif 'user_first_name' in kw:
        return User.objects.filter(user_detail__user_first_name__icontains=kw['user_first_name'])
    elif 'user_last_name' in kw:
        return User.objects.filter(user_detail__user_last_name__icontains=kw['user_last_name'])
    elif 'user_phone' in kw:
        return User.objects.filter(user_detail__user_phone__icontains=kw['user_phone'])
    elif 'user_street1' in kw:
        return User.objects.filter(user_detail__user_street1__icontains=kw['user_street1'])
    elif 'user_street2' in kw:
        return User.objects.filter(user_detail__user_street2__icontains=kw['user_street2'])
    elif 'user_city' in kw:
        return User.objects.filter(user_detail__user_city__icontains=kw['user_city'])
    elif 'user_state' in kw:
        return User.objects.filter(user_detail__user_state__icontains=kw['user_state'])
    elif 'user_country' in kw:
        return User.objects.filter(user_detail__user_country__icontains=kw['user_country'])
    elif 'user_zip' in kw:
        return User.objects.filter(user_detail__user_zip__icontains=kw['user_zip'])
    elif 'user_status' in kw:
        return User.objects.filter(user_status__icontains=kw['user_status'])

    raise MongoError(ErrorCode.MONGODB_INVALID_SEARCH_PARAM)


# Search by pattern
def query_user_search_by_pattern(**kw):
    """
    search user by pattern (re.Pattern)
    :param kw: keyword arguments
        :key "user_name": (optional) single keyword of username to be searched
        :key "user_email": (optional) single keyword of email to be searched
        :key "user_first_name": (optional) single keyword of first name to be searched
        :key "user_last_name": (optional) single keyword of last name to be searched
        :key "user_phone": (optional) single keyword of phone to be searched
        :key "user_street1": (optional) single keyword of street1 to be searched
        :key "user_street2": (optional) single keyword of street2 to be searched
        :key "user_city": (optional) single keyword of city to be searched
        :key "user_state": (optional) single keyword of state to be searched
        :key "user_country": (optional) single keyword of country to be searched
        :key "user_zip": (optional) single keyword of zip to be searched
        :key "user_status": (optional) single keyword of status to be searched
    \nAt least one key must be provided
    :return: array of searching results (User Model)
    """
    # Check input param
    if len(kw) == 0:
        raise MongoError(ErrorCode.MONGODB_EMPTY_PARAM)

    for arg in kw:
        if type(kw[arg]) != re.Pattern:
            raise MongoError(ErrorCode.MONGODB_RE_PATTERN_EXPECTED)

    if 'pattern_name' in kw:
        return User.objects(user_name=kw['pattern_name'])
    elif 'pattern_email' in kw:
        return User.objects(user_email=kw['pattern_email'])
    elif 'pattern_first_name' in kw:
        return User.objects(user_detail__user_first_name=kw['pattern_first_name'])
    elif 'pattern_last_name' in kw:
        return User.objects(user_detail__user_last_name=kw['pattern_last_name'])
    elif 'pattern_phone' in kw:
        return User.objects(user_detail__user_phone=kw['pattern_phone'])
    elif 'pattern_street1' in kw:
        return User.objects(user_detail__user_street1=kw['pattern_street1'])
    elif 'pattern_street2' in kw:
        return User.objects(user_detail__user_street2=kw['pattern_street2'])
    elif 'pattern_city' in kw:
        return User.objects(user_detail__user_city=kw['pattern_city'])
    elif 'pattern_state' in kw:
        return User.objects(user_detail__user_state=kw['pattern_state'])
    elif 'pattern_country' in kw:
        return User.objects(user_detail__user_country=kw['pattern_country'])
    elif 'pattern_zip' in kw:
        return User.objects(user_detail__user_zip=kw['pattern_zip'])
    elif 'pattern_status' in kw:
        return User.objects(user_status=kw['pattern_status'])

    raise MongoError(ErrorCode.MONGODB_INVALID_SEARCH_PARAM)


# Search by aggregate
def query_user_search_by_aggregate(aggr: list or dict):
    """
    :param aggr: dict of searching param
    :return: array of searching results in dict
    """
    if type(aggr) != list and type(aggr) != dict:
        raise MongoError(ErrorCode.MONGODB_LIST_EXPECTED)
    return list(User.objects.aggregate(aggr))

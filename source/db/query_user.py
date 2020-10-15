from source.models.model_user import User, LoginDetail, UserDetail, Thumbnail
from source.models.model_errors import ErrorCode
from source.utils.util_hash import *
import bson
import datetime
import re


##########
# CREATE #
##########
def query_user_create(user_name: str, user_email: str, user_password: str, user_ip="0.0.0.0"):
    """
    :param user_name: user's unique nickname
    :param user_email: user's unique email
    :param user_password: user's password
    :param user_ip: user's ip address (defaut 0.0.0.0)
    :return: user object if succeeded
    """
    if len(query_user_get_by_name(user_name)) > 0:
        return ErrorCode.MONGODB_USER_NAME_TAKEN

    elif len(query_user_get_by_email(user_email)) > 0:
        return ErrorCode.MONGODB_USER_EMAIL_TAKEN

    login = [LoginDetail(login_ip=user_ip, login_time=datetime.datetime.utcnow())]

    # EmbeddedDocument must be included when creating
    # user_detail, user_thumbnail, user_reg_date
    user = User(user_name=user_name, user_email=user_email, user_password=user_password,
                user_detail=UserDetail(), user_status="private", user_thumbnail=Thumbnail(),
                user_reg_date=datetime.datetime.utcnow(), user_recent_login=login,
                user_following=[], user_follower=[])

    return user.save()


############
# RETRIEVE #
############
def query_user_get_by_name(user_name: str):
    """
    :return: an array of such User, len == 0 if no such user_name, len == 1 if found
    """
    return User.objects(user_name=user_name)


def query_user_get_by_email(user_email: str):
    """
    :return: an array of such User (len == 0 or 1), len == 0 if no such user_email, len == 1 if found
    """
    return User.objects(user_email=user_email)


def query_user_get_by_id(user_id: str):
    """
    :return: an array of such User (len == 0 or 1), len == 0 if no such user_id, len == 1 if found
    """
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
    if len(query_user_get_by_id(user_id)) == 0:
        return ErrorCode.MONGODB_USER_NOT_FOUND

    valid_status = ["public", "private", "closed"]
    if user_status not in valid_status:
        return ErrorCode.MONGODB_INVALID_USER_STATUS

    return User.objects(_id=bson.ObjectId(user_id)).update(user_status=user_status)


def query_user_add_follow(follower_id: str, following_id: str):
    """
    :param follower_id: follower's user id
    :param following_id: uploader's user_id
    :return: 1 if succeeded
    """
    follower = query_user_get_by_id(follower_id)
    following = query_user_get_by_id(following_id)

    if len(follower) == 0:
        return ErrorCode.MONGODB_FOLLOWER_NOT_FOUND

    if len(following) == 0:
        return ErrorCode.MONGODB_FOLLOWED_NOT_FOUND

    if following_id in follower[0].user_following and follower_id in following[0].user_follower:
        return ErrorCode.MONGODB_FOLLOW_REL_EXISTS

    if following_id in follower[0].user_following or follower_id in following[0].user_follower:
        # print("following relationship broken, try to remove")
        query_user_delete_follow(follower_id, following_id)

    r1 = User.objects(_id=bson.ObjectId(follower_id)).update(add_to_set__user_following=following_id)
    r2 = User.objects(_id=bson.ObjectId(following_id)).update(add_to_set__user_follower=follower_id)
    if r1 != 1:
        return r1
    elif r2 != 1:
        return r2

    return 1


def query_user_delete_follow(follower_id: str, following_id: str):
    """
    :param follower_id: follower's user id
    :param following_id: uploader's user_id
    :return: 1 if succeeded
    """
    follower = query_user_get_by_id(follower_id)
    following = query_user_get_by_id(following_id)

    if len(follower) == 0:
        return ErrorCode.MONGODB_FOLLOWER_NOT_FOUND
    if len(following) == 0:
        return ErrorCode.MONGODB_FOLLOWED_NOT_FOUND

    r1 = User.objects(_id=bson.ObjectId(follower_id)).update(pull__user_following=following_id)
    r2 = User.objects(_id=bson.ObjectId(following_id)).update(pull__user_follower=follower_id)
    if r1 != 1:
        return r1
    elif r2 != 1:
        return r2

    return 1


def query_user_update_name(user_id: str, user_name: str):
    """
    :param user_id: user's id
    :param user_name: user's name
    :return: array of User Model
    """
    users = query_user_get_by_id(user_id)
    if len(users) == 0:
        return ErrorCode.MONGODB_USER_NOT_FOUND

    old_name = users[0].user_name
    if user_name == old_name:
        return ErrorCode.MONGODB_UPDATE_SAME_NAME

    if len(query_user_get_by_name(user_name)) > 0:
        return ErrorCode.MONGODB_USER_NAME_TAKEN

    return User.objects(_id=bson.ObjectId(user_id)).update(user_name=user_name)


def query_user_update_password(user_id: str, user_password: str):
    """
    :param user_id: user's id
    :param user_password: user's password
    :return: array of User Model
    """
    users = query_user_get_by_id(user_id)
    if len(users) == 0:
        return ErrorCode.MONGODB_USER_NOT_FOUND

    old_password = users[0].user_password
    if user_password == old_password:
        return ErrorCode.MONGODB_UPDATE_SAME_PASS

    return User.objects(_id=bson.ObjectId(user_id)).update(user_password=user_password)


def query_user_update_details(user_id: str, **kw):
    """
    :param user_id: user's unique id
    :param user_first_name (optional): new user's first name
    :param user_last_name (optional): new user's last_name
    :param user_phone (optional): new user's phone
    :param user_street1 (optional): new user's street1
    :param user_street2 (optional): new user's street2
    :param user_city (optional): new user's city
    :param user_state (optional): new user's state
    :param user_country (optional): new user's country
    :param user_zip (optional): new user's zip
    :return 1 if succeeded
    """
    users = query_user_get_by_id(user_id)
    if len(users) == 0:
        return ErrorCode.MONGODB_USER_NOT_FOUND

    id = bson.ObjectId(user_id)

    if 'user_first_name' in kw:
        User.objects(_id=id).update(set__user_detail__first_name=kw['user_first_name'])
    if 'user_last_name' in kw:
        User.objects(_id=id).update(set__user_detail__last_name=kw['user_last_name'])
    if 'user_phone' in kw:
        User.objects(_id=id).update(set__user_detail__phone=kw['user_phone'])
    if 'user_street1' in kw:
        User.objects(_id=id).update(set__user_detail__street1=kw['user_street1'])
    if 'user_street2' in kw:
        User.objects(_id=id).update(set__user_detail__street2=kw['user_street2'])
    if 'user_city' in kw:
        User.objects(_id=id).update(set__user_detail__city=kw['user_city'])
    if 'user_state' in kw:
        User.objects(_id=id).update(set__user_detail__state=kw['user_state'])
    if 'user_country' in kw:
        User.objects(_id=id).update(set__user_detail__country=kw['user_country'])
    if 'user_zip' in kw:
        User.objects(_id=id).update(set__user_detail__zip=kw['user_zip'])

    return 1


def query_user_update_thumbnail(user_id: str, **kw):
    """
    :param user_id: user's unique id
    :param user_thumbnail_uri: thumbnail uri
    :param user_thumbnail_type: must be in ['default', 'user', 'system']
    :return 1 if succeeded
    """
    users = query_user_get_by_id(user_id)
    id = bson.ObjectId(user_id)
    if len(users) == 0:
        return ErrorCode.MONGODB_USER_NOT_FOUND

    valid_type = ['default', 'user', 'system']
    if 'user_thumbnail_uri' in kw:
        User.objects(_id=id).update(set__user_thumbnail__thumbnail_uri=kw['user_thumbnail_uri'])
    if 'user_thumbnail_type' in kw:
        if kw['user_thumbnail_type'] not in valid_type:
            return ErrorCode.MONGODB_INVALID_THUMBNAIL
        User.objects(_id=id).update(set__user_thumbnail__thumbnail_type=kw['user_thumbnail_type'])

    return 1


def query_user_add_login(user_id: str, ip="0.0.0.0", time=datetime.datetime.utcnow()):
    """
    :param user_id: user's unique id
    :param ip: user's login ip address
    :param time: user's login time (utc, optional), default: current system time (utc)
    :return: 1 if succeeded
    """
    users = query_user_get_by_id(user_id)
    if len(users) == 0:
        return ErrorCode.MONGODB_USER_NOT_FOUND

    # only keep 10 login info
    login_history = users[0].user_recent_login
    oldest_login_time = login_history[0].login_time
    latest_login_time = login_history[-1].login_time
    if len(login_history) >= 10:
        # Delete oldest history
        User.objects(_id=bson.ObjectId(user_id)).update(pull__user_recent_login__login_time=oldest_login_time)

    # TODO: update latest 10 login info method, some bugs for current version
    # add new login info
    # print(time)
    # print(latest_login_time)
    if time == latest_login_time:
        return ErrorCode.MONGODB_LOGIN_INFO_EXISTS
    new_login = {'login_ip': ip, 'login_time': time}

    User.objects(_id=bson.ObjectId(user_id)).update(add_to_set__user_recent_login=[new_login])

    return 1


##########
# DELETE #
##########
def query_user_delete(user_id: str):
    """
    :param user_id: user's unique id
    :return: array of User Model
    """
    users = query_user_get_by_id(user_id)
    if len(users) == 0:
        return ErrorCode.MONGODB_USER_NOT_FOUND

    return User.objects(_id=bson.ObjectId(user_id)).delete()


##########
# SEARCH #
##########
# Search by i-contains
def query_user_search_by_contains(**kw):
    """
    Search user by i-contains (ignore case)
    :param user_name: (optional) single keyword of username to be searched
    :param user_email: (optional) single keyword of email to be searched
    :param user_first_name: (optional) single keyword of first_name to be searched
    :param user_last_name: (optional) single keyword of last_name to be searched
    :param user_phone: (optional) single keyword of phone to be searched
    :param user_street1: (optional) single keyword of street1 to be searched
    :param user_street2: (optional) single keyword of street2 to be searched
    :param user_city: (optional) single keyword of city to be searched
    :param user_state: (optional) single keyword of state to be searched
    :param user_country: (optional) single keyword of country to be searched
    :param user_zip: (optional) single keyword of zip to be searched
    :param user_status: (optional) single keyword of status to be searched
    :param user_reg_date: (optional) single keyword of reg_date to be searched
    :return: array of searching results (User Model)
    """

    for arg in kw:
        if type(kw[arg]) != str:
            return ErrorCode.MONGODB_PARAM_STR_EXPECTED

    if 'user_id' in kw:
        return query_user_get_by_id(kw['user_id'])
    elif 'user_name' in kw:
        return User.objects.filter(user_name__icontains=kw['user_name'])
    elif 'user_email' in kw:
        return User.objects.filter(user_email__icontains=kw['user_email'])
    elif 'user_first_name' in kw:
        return User.objects.filter(user_detail__first_name__icontains=kw['user_first_name'])
    elif 'user_last_name' in kw:
        return User.objects.filter(user_detail__last_name__icontains=kw['user_last_name'])
    elif 'user_phone' in kw:
        return User.objects.filter(user_detail__phone__icontains=kw['user_phone'])
    elif 'user_street1' in kw:
        return User.objects.filter(user_detail__street1__icontains=kw['user_street1'])
    elif 'user_street2' in kw:
        return User.objects.filter(user_detail__street2__icontains=kw['user_street2'])
    elif 'user_city' in kw:
        return User.objects.filter(user_detail__city__icontains=kw['user_city'])
    elif 'user_state' in kw:
        return User.objects.filter(user_detail__state__icontains=kw['user_state'])
    elif 'user_country' in kw:
        return User.objects.filter(user_detail__country__icontains=kw['user_country'])
    elif 'user_zip' in kw:
        return User.objects.filter(user_detail__zip__icontains=kw['user_zip'])
    elif 'user_status' in kw:
        return User.objects.filter(user_status__icontains=kw['user_status'])

    return ErrorCode.MONGODB_INVALID_SEARCH_PARAM


# Search by pattern
def query_user_search_by_pattern(**kw):
    """
    search user by pattern (re.Pattern)
    :param pattern_name (optional): search name pattern
    :param pattern_email (optional): search email pattern
    :param pattern_first_name (optional): search first_name pattern
    :param pattern_last_name (optional): search last_name pattern
    :param pattern_phone (optional): search phone pattern
    :param pattern_street1 (optional): search street1 pattern
    :param pattern_street2 (optional): search street2 pattern
    :param pattern_city (optional): search city pattern
    :param pattern_state (optional): search state pattern
    :param pattern_country (optional): search country pattern
    :param pattern_zip (optional): search zip pattern
    :param pattern_status (optional): search status pattern
    :param pattern_reg_date (optional): search reg_date pattern
    :return: array of searching results (User Model)
    """
    # Check input param
    if len(kw) == 0:
        return ErrorCode.MONGODB_EMPTY_PARAM

    for arg in kw:
        if type(kw[arg]) != re.Pattern:
            return ErrorCode.MONGODB_RE_PATTERN_EXPECTED

    if 'pattern_name' in kw:
        return User.objects(user_name=kw['pattern_name'])
    elif 'pattern_email' in kw:
        return User.objects(user_email=kw['pattern_email'])
    elif 'pattern_first_name' in kw:
        return User.objects(user_detail__first_name=kw['pattern_first_name'])
    elif 'pattern_last_name' in kw:
        return User.objects(user_detail__last_name=kw['pattern_last_name'])
    elif 'pattern_phone' in kw:
        return User.objects(user_detail__phone=kw['pattern_phone'])
    elif 'pattern_street1' in kw:
        return User.objects(user_detail__street1=kw['pattern_street1'])
    elif 'pattern_street2' in kw:
        return User.objects(user_detail__street2=kw['pattern_street2'])
    elif 'pattern_city' in kw:
        return User.objects(user_detail__city=kw['pattern_city'])
    elif 'pattern_state' in kw:
        return User.objects(user_detail__state=kw['pattern_state'])
    elif 'pattern_country' in kw:
        return User.objects(user_detail__country=kw['pattern_country'])
    elif 'pattern_zip' in kw:
        return User.objects(user_detail__zip=kw['pattern_zip'])
    elif 'pattern_status' in kw:
        return User.objects(user_status=kw['pattern_status'])
    elif 'pattern_reg_date' in kw:
        return User.objects(user_reg_date=kw['pattern_reg_date'])

    return ErrorCode.MONGODB_INVALID_SEARCH_PARAM


# Search by aggregate
def query_user_search_by_aggregate(aggr: dict):
    """
    :param aggr: dict of searching param
    :return: array of searching results in dict
    """
    return list(User.objects.aggregate(aggr))

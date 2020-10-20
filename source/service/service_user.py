from source.models.model_errors import *
from source.settings import *
from source.db.query_user import *
from source.utils.util_hash import *
from source.db.mongo import get_db


def service_user_reg(conf, **kw):
    """
    :param conf: config
    :param user_name: (required) str
    :param user_email: (required) str
    :param user_ip: (optional) str
    :return:
    """
    # user_name: str, user_email: str, user_password: str, user_ip = "0.0.0.0"
    # service_user_reg(conf, user_name="t", user_email="k", user_password="lol")

    db = get_db(conf)

    if 'user_name' not in kw or 'user_email' not in kw or 'user_password' not in kw:
        return ErrorCode.SERVICE_MISSING_PARAM

    users = query_user_create(kw['user_name'], kw['user_email'], util_hash_encode(kw['user_password']))

    # TODO: update to raise Exception
    if type(users) == ErrorCode:
        return ErrorCode.SERVICE_USER_CREATION_FAILURE

    user = query_user_get_by_name(kw['user_name'])[0]
    if type(user) == ErrorCode:
        return ErrorCode.SERVICE_USER_NOT_FOUND

    return user.to_dict()


def service_user_check_password(**kw):

    users = None
    if 'user_name' in kw:
        users = query_user_get_by_name(kw['user_name'])
    if 'user_email' in kw:
        users = query_user_get_by_email(kw['user_email'])

    if len(users) == 0:
        return ErrorCode.SERVICE_USER_NOT_FOUND

    return util_hash_encode(kw['user_password']) == users[0].user_password


def service_user_get_user(conf, **kw):
    # service_user_get_user(config['default'], user_name="t", user_password="lol")

    db = get_db(conf)

    # TODO: validate user by session

    # Validate user by password
    if 'user_name' not in kw and 'user_email' not in kw:
        return ErrorCode.SERVICE_MISSING_PARAM
    if 'user_password' not in kw:
        return ErrorCode.SERVICE_MISSING_PARAM

    auth = service_user_check_password(**kw)

    if type(auth) == ErrorCode or auth is False:
        return ErrorCode.SERVICE_USER_NOT_FOUND

    if 'user_name' in kw:
        return query_user_get_by_name(kw['user_name'])[0].to_dict()
    if 'user_email' in kw:
        return query_user_get_by_email(kw['user_email'])[0].to_dict()

    return ErrorCode.SERVICE_MISSING_PARAM


def service_user_login(conf, **kw):
    user = service_user_get_user(conf, **kw)

    if type(user) == ErrorCode:
        return ErrorCode.SERVICE_USER_AUTH_FAILURE

    return user


def service_user_logout():
    return


def service_user_cancel():
    return


def service_user_info(conf, **kw):
    # table: user
    # table: video (belong to this user)
    # table: video_op (belong to this user)

    db = get_db(conf)

    if "user_id" in kw:
        result = query_user_get_by_id(kw["user_id"])
    else:
        result = [{}]

    return result

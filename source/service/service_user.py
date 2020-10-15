from source.models.model_errors import *
from source.settings import *
from source.db.query_user import *
from source.utils.util_hash import *
from source.db.mongo import get_db
from source.service.service_auth import *


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

    users = query_user_create(kw['user_name'], kw['user_email'], hash_encode(kw['user_password']))

    # TODO: update to raise Exception
    if type(users) == ErrorCode:
        return ErrorCode.SERVICE_USER_CREATION_FAILURE

    user = query_user_get_by_name(kw['user_name'])[0]
    if type(user) == ErrorCode:
        return ErrorCode.SERVICE_USER_NOT_FOUND

    return user.to_dict()


def service_user_login(conf, **kw):
    user = service_auth_get_user(conf, **kw)

    if type(user) == ErrorCode:
        return ErrorCode.SERVICE_USER_AUTH_FAILURE

    return user


def service_user_logout():
    return


def service_user_cancel():
    return


def service_user_info():
    # table: user
    # table: video (belong to this user)
    # table: video_op (belong to this user)
    return

from source.db.query_user import *
from source.db.mongo import get_db
from source.settings import *
from source.utils.util_hash import *


# TODO: add session pool


def service_auth_check_password(**kw):

    users = None
    if 'user_name' in kw:
        users = query_user_get_by_name(kw['user_name'])
    if 'user_email' in kw:
        users = query_user_get_by_email(kw['user_email'])

    if len(users) == 0:
        return ErrorCode.SERVICE_USER_NOT_FOUND

    return hash_encode(kw['user_password']) == users[0].user_password


def service_auth_get_user(conf, **kw):
    # service_auth_get_user(config['default'], user_name="t", user_password="lol")

    db = get_db(conf)

    # TODO: validate user by session

    # Validate user by password
    if 'user_name' not in kw and 'user_email' not in kw:
        return ErrorCode.SERVICE_MISSING_PARAM
    if 'user_password' not in kw:
        return ErrorCode.SERVICE_MISSING_PARAM

    auth = service_auth_check_password(**kw)

    if type(auth) == ErrorCode or auth is False:
        return ErrorCode.SERVICE_USER_NOT_FOUND

    if 'user_name' in kw:
        return query_user_get_by_name(kw['user_name'])[0].to_dict()
    if 'user_email' in kw:
        return query_user_get_by_email(kw['user_email'])[0].to_dict()

    return ErrorCode.SERVICE_MISSING_PARAM

from source.models.model_errors import *


def service_user_reg(**kw):
    # user_name: str, user_email: str, user_password: str, user_ip = "0.0.0.0"
    if 'user_name' not in kw or 'user_email' not in kw or 'user_password' not in kw:
        return ErrorCode.SERVICE_MISSING_PARAM
    return


def service_user_login():
    return


def service_user_logout():
    return


def service_user_cancel():
    return


def service_user_info():
    # table: user
    # table: video (belong to this user)
    # table: video_op (belong to this user)
    return

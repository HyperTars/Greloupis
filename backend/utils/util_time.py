import datetime


def get_time_now_utc():
    return datetime.datetime.utcnow().replace(microsecond=0)

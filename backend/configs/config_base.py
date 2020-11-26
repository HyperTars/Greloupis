import os
# import sys


class BaseConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret string'

    # Searching Config
    SEARCH_IGNORE_CASE = True
    SEARCH_EXACT = False
    SEARCH_LIKE = True
    SEARCH_SLICE = False
    DATA_FORMAT = "dict"

    # Video Status
    VIDEO_STATUS = ['public', 'private', 'deleted']
    VIDEO_RAW_STATUS = ['pending', 'transcoding', 'streaming']
    VIDEO_CNT = ['view', 'views', 'video_view',
                 'comment', 'comments', 'video_comment',
                 'like', 'likes', 'video_like',
                 'dislike', 'dislikes', 'video_dislike',
                 'star', 'stars', 'video_star',
                 'share', 'shares', 'video_share']

    @staticmethod
    def init_app(app):
        pass

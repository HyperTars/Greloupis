import os


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

    # AWS
    AWS_AUTH_KEY = "bf9e5788a7f59072e26712bdfacdfd30c0941d836e9" \
        "340de9503ca579aa765716ae9521ae429d76876b818b00c34096582" \
        "ac4c7784eaf2c1febdafd667134101"
    AWS_CLOUD_FRONT = "https://d2t7530wn5sgoq.cloudfront.net/assets/MP4"
    AWS_STREAMING_FORMAT = ".mp4"
    AWS_STREAMING_LOW = "360"
    AWS_STREAMING_MID = "720"
    AWS_STREAMING_HIGH = "1080"

    @staticmethod
    def init_app(app):
        pass

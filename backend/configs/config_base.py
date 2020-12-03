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
    AWS_AUTH_KEY = os.environ.get('AWS_AUTH_KEY')
    AWS_CLOUD_FRONT = "https://d2t7530wn5sgoq.cloudfront.net/assets/"
    AWS_STREAMING_FOLDER = AWS_CLOUD_FRONT + "MP4/"
    AWS_STREAMING_FORMAT = ".mp4"
    AWS_STREAMING_LOW = "540"
    AWS_STREAMING_MID = "720"
    AWS_STREAMING_HIGH = "1080"

    AWS_THUMBNAIL_FOLDER = "https://vod-xuanbinmediabucket." \
        "s3-us-west-1.amazonaws.com/assets/Thumbnails/"
    AWS_THUMBNAIL_FORMAT = ".0000001.jpg"

    # Searching Config
    SEARCH_IGNORE_CASE = True
    SEARCH_EXACT = False
    SEARCH_LIKE = True
    SEARCH_SLICE = False
    DATA_FORMAT = "dict"

    # Mongo Tables
    MONGO_TABLE_USER = "user"
    MONGO_TABLE_VIDEO = "video"
    MONGO_TABLE_VIDEO_OP = "video_op"

    # CORS Settings
    CORS_ALLOW_HEADERS = 'Content-Type'
    FRONTEND = [
        'http://greloupis-backend.herokuapp.com',
        'http://greloupis-frontend.herokuapp.com',
        'https://greloupis-frontend.herokuapp.com',
        'https://greloupis.postman.co/',
        'http://localhost:8081',
        'http://localhost:8080',
        'http://localhost:8000',
        'http://localhost:5000',
        'http://localhost:3000',
        'http://localhost:443',
        'http://localhost:80',
        'http://localhost',
        'http://localhost/',
        'http://localhost/api',
        'http://127.0.0.1:8081',
        'http://127.0.0.1:8080',
        'http://127.0.0.1:8000',
        'http://127.0.0.1:5000',
        'http://127.0.0.1:3000',
        'http://127.0.0.1:443',
        'http://127.0.0.1:80',
        'http://127.0.0.1/api',
        'http://127.0.0.1',
        'http://127.0.0.1/',
        'http://0.0.0.0:8081',
        'http://0.0.0.0:8080',
        'http://0.0.0.0:8000',
        'http://0.0.0.0:5000',
        'http://0.0.0.0:3000',
        'http://0.0.0.0:443',
        'http://0.0.0.0:80',
        'http://0.0.0.0/api',
        'http://0.0.0.0/',
        'http://0.0.0.0'
    ]

    # jwt
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-key'
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_CSRF_CHECK_FORM = True
    JWT_ACCESS_TOKEN_EXPIRES = \
        os.environ.get('JWT_ACCESS_TOKEN_EXPIRES') or 10
    PROPAGATE_EXCEPTIONS = True
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', "refresh"]

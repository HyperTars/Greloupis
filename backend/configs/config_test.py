import os

from .config_base import BaseConfig


# Test settings class
class TestConfig(BaseConfig):
    """Config Core Class"""
    # Debug Mode
    DEBUG = True

    # Searching Config
    SEARCH_IGNORE_CASE = True
    SEARCH_EXACT = False
    SEARCH_LIKE = True
    SEARCH_SLICE = False
    DATA_FORMAT = "dict"

    # Mongo DB
    MONGO_ENDPOINT = "mongodb+srv://devops:DevOps@mongodbcluster.v4vtj" \
                     ".mongodb.net/online_video_platform_test?retryWrites" \
                     "=true&w=majority"
    MONGO_DATABASE = "online_video_platform_test"
    MONGODB_SETTINGS = {
        'db': MONGO_DATABASE,
        'host': MONGO_ENDPOINT
    }
    MONGO_TABLE_USER = "user"
    MONGO_TABLE_VIDEO = "video"
    MONGO_TABLE_VIDEO_OP = "video_op"

    # Config Flask
    FLASK_SERVER_NAME = 'localhost:8000'
    FLASK_DEBUG = True

    # Config Log
    LOG_LEVEL = "DEBUG"

    # Config redis
    # Change to real IP address ...
    REDIS_HOST = 'your host'
    REDIS_PORT = 'your port'
    REDIS_PASSWORD = 'your password'
    REDIS_POLL = 10

    # Frontend
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
    CORS_ALLOW_HEADERS = 'Content-Type'

    # jwt
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-key'
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_CSRF_CHECK_FORM = True
    JWT_ACCESS_TOKEN_EXPIRES = \
        os.environ.get('JWT_ACCESS_TOKEN_EXPIRES') or 10
    PROPAGATE_EXCEPTIONS = True
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', "refresh"]

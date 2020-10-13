from .config_base import *


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
    MONGO_ENDPOINT = "mongodb+srv://devops:DevOps@mongodbcluster.v4vtj.mongodb.net/online_video_platform?retryWrites=true&w=majority"
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

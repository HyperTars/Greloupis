from .config_base import BaseConfig


# Test settings class
class TestConfig(BaseConfig):
    """Config Core Class"""
    # Debug Mode
    DEBUG = True

    # Mongo DB
    # MONGO_ENDPOINT = "mongodb+srv://devops:DevOps@mongodbcluster.v4vtj" \
    #                  ".mongodb.net/online_video_platform_test?retryWrites" \
    #                  "=true&w=majority"
    # MONGO_DATABASE = "online_video_platform_test"
    MONGO_ENDPOINT = "mongodb+srv://greloupis:greloupis@cluster-greloupis" \
                     ".8gpx5.mongodb.net/greloupis-test?retryWrites=true&w" \
                     "=majority"
    MONGO_DATABASE = "greloupis-test"
    MONGODB_SETTINGS = {
        'db': MONGO_DATABASE,
        'host': MONGO_ENDPOINT,
        'connect': False
    }
    MONGO_TABLE_USER = "user"
    MONGO_TABLE_VIDEO = "video"
    MONGO_TABLE_VIDEO_OP = "video_op"

    # Config Flask
    FLASK_SERVER_NAME = 'localhost:5000'
    FLASK_DEBUG = True

    # Config Log
    LOG_LEVEL = "DEBUG"

    # Config redis
    # Change to real IP address ...
    REDIS_HOST = 'your host'
    REDIS_PORT = 'your port'
    REDIS_PASSWORD = 'your password'
    REDIS_POLL = 10

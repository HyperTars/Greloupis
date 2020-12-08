from .config_base import BaseConfig
import os


# Test settings class
class TestConfig(BaseConfig):
    """Config Core Class"""
    # Debug Mode
    DEBUG = True

    # Mongo DB
    MONGO_ENDPOINT = "mongodb+srv://" + os.environ.get('MONGO_TEST')
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

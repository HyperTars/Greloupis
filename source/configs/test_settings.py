# Test settings class
class TestConfig(object):
    """Config Core Class"""
    # Debug Mode
    DEBUG = True

    # DB URI
    MONGO_ENDPOINT = "mongodb+srv://devops:DevOps@mongodbcluster.v4vtj.mongodb.net/online_video_platform?retryWrites=true&w=majority"

    # Config Flask
    FLASK_SERVER_NAME = 'localhost:8000'
    FLASK_DEBUG = True

    # Config Log
    LOG_LEVEL = "DEBUG"
    LOG_LEVEL = "INFO"

    # Config redis
    # Change to real IP address ...
    REDIS_HOST = 'your host'
    REDIS_PORT = 'your port'
    REDIS_PASSWORD = 'your password'
    REDIS_POLL = 10

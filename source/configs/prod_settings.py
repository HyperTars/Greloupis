# Production settings class
class ProdConfig(object):
    """Deploy Config Class"""
    # Debug Mode
    DEBUG = False

    # DB URI
    MONGO_ENDPOINT = "mongodb+srv://devops:DevOps@mongodbcluster.v4vtj.mongodb.net/online_video_platform?retryWrites=true&w=majority"

    # Config Flask
    FLASK_SERVER_NAME = 'localhost:8888'
    FLASK_DEBUG = False

    # Config Log
    LOG_LEVEL = "INFO"

    # Config redis
    # Change to real IP address ...
    REDIS_HOST = 'your host'
    REDIS_PORT = 'your port'
    REDIS_PASSWORD = 'your password'
    REDIS_POLL = 10

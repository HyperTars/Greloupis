# Global general settings class
class Config(object):
    """Config Core Class"""
    # Debug Mode
    DEBUG = False

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

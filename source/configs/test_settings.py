# Global general settings class
class Config(object):
    """Config Core Class"""
    # Debug Mode
    DEBUG = True

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

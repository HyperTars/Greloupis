from .config_base import BaseConfig


# Development settings class
class DevConfig(BaseConfig):
    """Config Core Class"""
    # Debug Mode
    DEBUG = True

    # Mongo DB
    MONGO_ENDPOINT = "mongodb+srv://greloupis:greloupis@cluster-greloupis" \
                     ".8gpx5.mongodb.net/greloupis?retryWrites=true&w=majority"
    MONGO_DATABASE = "greloupis"
    MONGODB_SETTINGS = {
        'db': MONGO_DATABASE,
        'host': MONGO_ENDPOINT,
        'connect': False
    }

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

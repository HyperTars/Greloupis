import os
import sys
import multiprocessing

basedir = os.path.abspath(os.path.dirname(__file__))

class config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret string'
    @staticmethod
    def init_app(app):
        pass


# Development settings class
class DevConfig(object):
    """Config Core Class"""
    # Debug Mode
    DEBUG = True

    # Mongo DB
    MONGODB_SETTINGS = {
        'db': 'online_video_platform',
        'host': 'mongodb+srv://devops:DevOps@mongodbcluster.v4vtj.mongodb.net/online_video_platform?retryWrites=true&w=majority'
    }
    
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


# Test settings class
class TestConfig(object):
    """Config Core Class"""
    # Debug Mode
    DEBUG = True

    # DB URI
    MONGO_ENDPOINT = "mongodb+srv://devops:DevOps@mongodbcluster.v4vtj.mongodb.net/online_video_platform?retryWrites=true&w=majority"
    MONGO_DATABASE = "online_video_platform"
    
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


# Production settings class
class ProdConfig(object):
    """Deploy Config Class"""
    WORKERS = multiprocessing.cpu_count() * 2 + 1
    WORKER_CONNECTIONS = 10000
    BACKLOG = 64
    TIMEOUT = 30

    # Debug Mode
    DEBUG = False

    # DB URI
    MONGO_ENDPOINT = "mongodb+srv://devops:DevOps@mongodbcluster.v4vtj.mongodb.net/online_video_platform?retryWrites=true&w=majority"
    MONGO_DATABASE = "online_video_platform"
    
    # Config Flask
    FLASK_SERVER_NAME = 'localhost:8888'
    FLASK_DEBUG = False

    # Config Log
    LOG_LEVEL = "INFO"
    LOG_DIR_PATH = os.path.join(os.path.dirname(__file__), 'logs')
    LOG_FILE_MAX_BYTES = 1024 * 1024 * 100
    LOG_FILE_BACKUP_COUNT = 10
    PID_FILE = 'run.pid'

    # Config redis
    # Change to real IP address ...
    REDIS_HOST = 'your host'
    REDIS_PORT = 'your port'
    REDIS_PASSWORD = 'your password'
    REDIS_POLL = 10


config = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
    'default': DevConfig
}
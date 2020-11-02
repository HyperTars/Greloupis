from .config_base import BaseConfig
import multiprocessing
import os


# Production settings class
class ProdConfig(BaseConfig):
    """Deploy Config Class"""
    WORKERS = multiprocessing.cpu_count() * 2 + 1
    WORKER_CONNECTIONS = 10000
    BACKLOG = 64
    TIMEOUT = 30

    # Searching Config
    SEARCH_IGNORE_CASE = True
    SEARCH_EXACT = False
    SEARCH_LIKE = True
    SEARCH_SLICE = False
    DATA_FORMAT = "dict"

    # Debug Mode
    DEBUG = False

    # DB URI
    MONGO_ENDPOINT = "mongodb+srv://devops:DevOps@mongodbcluster.v4vtj" \
                     ".mongodb.net/online_video_platform?retryWrites=true&w" \
                     "=majority"
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

    # Frontend
    FRONTEND = [
        'http://localhost:3000',
        'http://127.0.0.1:3000',
        'http://0.0.0.0:3000'
    ]

    # jwt
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-key'
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_CSRF_CHECK_FORM = True
    JWT_ACCESS_TOKEN_EXPIRES = \
        os.environ.get('JWT_ACCESS_TOKEN_EXPIRES') or 10
    PROPAGATE_EXCEPTIONS = True
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', "refresh"]

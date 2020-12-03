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

    # Debug Mode
    DEBUG = False

    # DB URI
    MONGO_ENDPOINT = "mongodb+srv://greloupis:greloupis@cluster-greloupis" \
                     ".8gpx5.mongodb.net/greloupis?retryWrites=true&w" \
                     "=majority"
    MONGO_DATABASE = "greloupis"
    MONGODB_SETTINGS = {
        'db': MONGO_DATABASE,
        'host': MONGO_ENDPOINT,
        'connect': False
    }

    # Config Flask
    FLASK_SERVER_NAME = 'localhost:5000'
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

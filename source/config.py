# Global general settings class
class Config(object):
    """项目配置核心类"""
    # 调试模式
    DEBUG = True

    # Flask settings
    FLASK_SERVER_NAME = 'localhost:8888'
    FLASK_DEBUG = True

    # 配置日志
    # LOG_LEVEL = "DEBUG"
    LOG_LEVEL = "INFO"

    # 配置redis
    # 项目上线以后，这个地址就会被替换成真实IP地址，mysql也是
    REDIS_HOST = 'your host'
    REDIS_PORT = 'your port'
    REDIS_PASSWORD = 'your password'
    REDIS_POLL = 10

    # SQLAlchemy settings
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:xxxxx@localhost:3306/test?charset=utf8'
    # Dynamic tracing settings editing
    # SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 查询时会显示原始SQL语句
    # SQLALCHEMY_ECHO = True
    # 数据库连接池的大小
    # SQLALCHEMY_POOL_SIZE = 10
    # 指定数据库连接池的超时时间
    # SQLALCHEMY_POOL_TIMEOUT = 10
    # 控制在连接池达到最大值后可以创建的连接数。当这些额外的 连接回收到连接池后将会被断开和抛弃。
    # SQLALCHEMY_MAX_OVERFLOW = 2

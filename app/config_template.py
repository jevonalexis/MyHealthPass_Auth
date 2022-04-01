import os


class AppConfig:
    DEBUG = True
    SECRET_KEY = 'secret_key_here'
    FLASK_SECRET = SECRET_KEY
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = 'flask_session'
    PERMANENT_SESSION_LIFESPAN = 60 * 60 * 24 * 1  # 60s * 60m * 24h * 1d
    __DB_SQLITE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'MHP.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{__DB_SQLITE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    SQLALCHEMY_ECHO = False


REDIS_CONFIG = {
    'conn': {
        'host': "localhost",
        'password': "",
        'ssl': False,
        'port': 6379,
        'db': 3
    },
    'options': {
        'prefix': "mhp_",
        'ttl': 60 * 60 * 36
    }

}
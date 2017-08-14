import os

# WTF_CSRF_ENABLED = True
# SECRET_KEY = 'you-will-never-guess'

basedir = os.path.abspath(os.path.dirname(__file__))

# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/weekly_workouts'
# SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/weekly_workouts'
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

class Config(object):
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/weekly_workouts'
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class TestingConfig(Config):
    TESTING = True

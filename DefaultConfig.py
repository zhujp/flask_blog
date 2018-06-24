import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'OsYldjfYCicdYThinkTwiEc'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql+pymysql://root:123456@127.0.0.1:3306/flask_blog?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql+pymysql://root:123456@127.0.0.1:3306/flask_blog?charset=utf8'

config = {
    'development':DevelopmentConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig
}    
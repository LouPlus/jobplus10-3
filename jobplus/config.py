import os

class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hello shiyanlou'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/jobplus?charset=utf8'

class TestConfig(BaseConfig):
    pass

configs = {
    'dev': DevelopConfig,
    'test': TestConfig
}

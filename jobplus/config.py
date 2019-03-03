import os


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hello shiyanlou'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JOB_PER_PAGE = 15
    COMPANY_PER_PAGE = 15


class DevelopConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/jobplus?charset=utf8'


class TestConfig(BaseConfig):
    pass


configs = {
    'dev': DevelopConfig,
    'test': TestConfig
}

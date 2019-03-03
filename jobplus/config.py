import os


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hello shiyanlou'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    # 上传文件目录
    UPLOADS_DEFAULT_DEST = 'jobplus/static/'
    MAX_CONTENT_LENGTH = 1024 * 1024 * 8


class DevelopConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/jobplus?charset=utf8'


class TestConfig(BaseConfig):
    pass


configs = {
    'dev': DevelopConfig,
    'test': TestConfig
}

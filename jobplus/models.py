from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Base(db.Model):
    '''
    base class for models
    contains timestamp by default
    '''
    # 表示不要把这个类当成是 Model 类
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, 
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)


user_job = db.Table(
    'user_job',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')),
    db.Column('job_id', db.Integer, db.ForeignKey('job.id', ondelete='CASCADE'))
)


class User(Base, UserMixin):
    __tablename__ = 'user'

    ROLE_USER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True, nullable=False)
    avatar = db.Column(db.String(255), nullable=False, default='avatar.png')
    email = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column('password', db.String(255), nullable=False)
    phone = db.Column(db.String(20), unique=True)
    work_years = db.Column(db.SmallInteger, default=ROLE_USER)
    role = db.Column(db.Integer)
    resume_url = db.Column(db.String(64))

    # 关联简历表，结构化简历，以后做
    # resume = db.relation('Resume', uselist=False)
    collect_jobs = db.relation('Job', secondary=user_job)

    def __repr__(self):
        return '<User:{}>'.format(self.name)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)
    
    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.ROLE_ADMIN

    @property
    def is_company(self):
        return self.ROLE_COMPANY


class Company(Base):
    __tablename__ = 'company'


    id = db.Column(db.Integer,  db.ForeignKey('user.id'),primary_key=True)
    user = db.relationship('User', uselist=False, backref=db.backref('company',uselist=False))

    name = db.Column(db.String(64), nullable=False, index=True, unique=True, comment='公司名')
    slogan = db.Column(db.String(24), nullable=False, index=True, unique=True, comment='slogan')
    logo = db.Column(db.String(64), nullable=False)
    website = db.Column(db.String(64), nullable=False)
    contact = db.Column(db.String(24), nullable=False, comment='联系方式')
    location = db.Column(db.String(24), nullable=False, comment='公司地址')
    short_description = db.Column(db.String(10), comment='一句话描述')
    full_description = db.Column(db.String(255), comment='关于我们，公司详情描述')
    tags = db.Column(db.String(128), comment='公司标签，用多个逗号隔开')
    stack = db.Column(db.String(128), comment='公司技术栈，用多个逗号隔开')
    team_des = db.Column(db.String(255), comment='团队介绍')
    welfare = db.Column(db.String(255), comment='公司福利')
    trade = db.Column(db.String(32), comment='行业')
    funding = db.Column(db.String(32), comment='融资阶段')
    city = db.Column(db.String(32), comment='所在城市')

    

    def __repr__(self):
        return '<Company {}>'.format(self.name)


class Job(Base):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), comment='职位名称')
    salary_max = db.Column(db.Integer)
    salary_min = db.Column(db.Integer)
    location = db.Column(db.String(32), comment='工作地点')
    tags = db.Column(db.String(128), comment='职位标签')
    experience_requirement = db.Column(db.String(32), comment='工作经验要求')
    degree_requirement = db.Column(db.String(32), comment='学历要求')
    is_fulltime = db.Column(db.Boolean, default=True, comment='是否全职')
    is_open = db.Column(db.Boolean, default=True, comment='是否在招聘')
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'))
    company = db.relationship('Company', uselist=False)
    view_count = db.Column(db.Integer, default=0, comment='该岗位浏览数')

    description = db.Column(db.String(1024))


class Delivery(Base):
    __tablename__ = 'delivery'

    # 等待审核
    STATUS_WAITING = 1
    # 被拒绝
    STATUS_REJECT = 2
    # 被接受，等待面试通知
    STATUS_ACCEPT = 3

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id', ondelete='SET NULL'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    status = db.Column(db.SmallInteger, default=STATUS_WAITING, comment='投递状态')
    location = db.Column(db.String(255), comment='企业回应')

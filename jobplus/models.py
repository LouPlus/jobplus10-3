from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Base(db.Model):
    '''
    base class for models
    contains timestamp by default

    '''
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, 
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)


class User(Base):
    __tablename__ = 'user'

    ROLE_USER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(256),unique=True,nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    phone = db.Column(db.String(20),unique=True,nullable=False)
    role = db.Column(db.Integer)
    work_years = db.Column(db.SmallInteger, default=ROLE_USER)
    resume = db.Column(db.String(256))

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


class Job(Base):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True, nullable=False)
    salary_max = db.Column(db.Integer)
    salary_min = db.Column(db.Integer)
    location = db.Column(db.String(32))
    tags= db.Column(db.String(128))
    work_years = db.Column(db.Integer)
    degree = db.Column(db.String(32))
    description = db.Column(db.String(1024))


class Company(Base):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    short_description = db.Column(db.String(64))
    full_description = db.Column(db.String(256))
    logo_url = db.Column(db.String(256))
    website = db.Column(db.String(256))
    trade = db.Column(db.String(32))  
    funding = db.Column(db.String(32))
    city = db.Column(db.String(32))

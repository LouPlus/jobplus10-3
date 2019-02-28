from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user

from jobplus.forms import LoginForm, RegisterForm
from jobplus.models import User, db

front = Blueprint('front', __name__)


@front.route('/')
def index():
    return render_template('index.html')

@front.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)
        return redirect(url_for('.index'))
    return render_template('login.html',form=form)

@front.route('/userregister', methods=['GET', 'POST'])
def userregister():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录！','success')
        return redirect(url_for('.login'))
    return render_template('userregister.html',form=form)
    

@front.route('/companyregister', methods=['GET', 'POST'])
def companyregister():
    form = RegisterForm()
    form.name.lable = u'企业名称'
    if form.validate_on_submit():
        user= form.create_user()
        user.role = User.ROLE_COMPANY
        db.session.add(user)
        db.session.commit()
        flash('注册成功，请登录！','success')
        return redirect(url_for('.login'))
    return render_template('companyregister.html',form=form)
from flask import Blueprint, render_template, redirect, url_for, flash 
from flask_login import login_user, login_required, logout_user

from jobplus.forms import LoginForm, RegisterForm
from jobplus.models import db, User, Company

front = Blueprint('front', __name__)


@front.route('/')
def index():
    companies = Company.query.order_by(Company.id).limit(8).all()
    return render_template('index.html', companies=companies)


@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)
        next = 'user.profile'
        if user.is_admin:
            next = 'admin.admin_base.html'
        elif user.is_company:
            next = 'company.profile'
        return redirect(url_for(next))
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
    form.name.label.text = '企业名称'
    if form.validate_on_submit():
        user = form.create_user()
        user.role = User.ROLE_COMPANY
        db.session.add(user)
        db.session.commit()
        flash('注册成功，请登录！','success')
        return redirect(url_for('.login'))
    return render_template('companyregister.html',form=form)


@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录','success')
    return redirect(url_for('.index'))




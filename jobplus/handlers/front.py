from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user

from jobplus.forms import LoginForm
from jobplus.models import User

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

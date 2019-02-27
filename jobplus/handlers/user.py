from flask import Blueprint, render_template

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/profile')
def profile():
    # todo 提交显示表单逻辑
    return render_template('user.html')


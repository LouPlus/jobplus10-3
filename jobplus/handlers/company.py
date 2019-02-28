from flask import Blueprint, render_template

company = Blueprint('company', __name__, url_prefix='/company')


@company.route('/profile')
def profile():
    # todo 提交显示表单逻辑
    return render_template('company/profile.html')


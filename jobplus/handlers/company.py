from flask import Blueprint, render_template

company = Blueprint('company', __name__, url_prefix='/company')


@company.route('/profile')
def profile():
    # todo 提交显示表单逻辑
    return render_template('company/profile.html')

@company.route('/<int:company_id>')
def detail(company_id):
    return 'company detail: {}'.format(company_id)
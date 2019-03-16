from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from sqlalchemy import and_

from jobplus.forms import CompanyProfileForm
from jobplus.lib.source_data import company_filter_data
from jobplus.models import User, Company

company = Blueprint('company', __name__, url_prefix='/company')


@company.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if not current_user.is_company:
        flash('您不是企业用户，无法登陆', 'warning')
        return redirect(url_for('font.admin_base.html'))
    form = CompanyProfileForm(obj=current_user.company_info)
    form.name.data = current_user.name
    form.email.data = current_user.email
    if form.validate_on_submit():
        form.updated_profile(current_user)
        flash('企业信息更新成功', 'success')
        return redirect(url_for('front.admin_base.html'))
    return render_template('company/profile.html', form=form)


@company.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    args_dict = request.args.to_dict()

    rule_list = []
    for key in args_dict.keys():
        if args_dict[key]:
            if key == 'trade':
                rule_list.append(Company.trade.like('%'+args_dict['trade']+'%'))
            elif key == 'funding':
                rule_list.append(Company.funding == args_dict[key])
            elif key == 'size':
                rule_list.append(Company.size == args_dict[key])
            elif key == 'city':
                rule_list.append(Company.city == args_dict[key])

    rule = and_(*rule_list)

    pagination = Company.query.filter(rule).paginate(
        page=page,
        per_page=current_app.config['COMPANY_PER_PAGE'],
        error_out=False
    )
    return render_template('company/index.html',
                           pagination=pagination,
                           company_filter_data=company_filter_data,
                           args_dict=args_dict)


@company.route('/<int:company_id>')
def detail(company_id):
    return 'company detail: {}'.format(company_id)

from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, abort
from flask_login import login_required, current_user
from sqlalchemy import and_

from jobplus.forms import CompanyProfileForm
from jobplus.lib.source_data import company_filter_data
from jobplus.models import User, Company, Job, db, Delivery
from jobplus.forms import JobForm

company = Blueprint('company', __name__, url_prefix='/company')


@company.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if not current_user.is_company:
        flash('您不是企业用户，无法登陆', 'warning')
        return redirect(url_for('front.index'))
    form = CompanyProfileForm(obj=current_user.company_info)
    form.name.data = current_user.name
    form.email.data = current_user.email
    if form.validate_on_submit():
        form.updated_profile(current_user)
        flash('企业信息更新成功', 'success')
        return redirect(url_for('front.index'))
    return render_template('company/profile.html', form=form)


@company.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    args_dict = request.args.to_dict()
    # data = {'trade': '',
    #         'funding': '',
    #         'size': '',
    #         'city': '杭州'}

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

@company.route('/<int:company_id>/admin/')
@login_required
def admin_index(company_id):
    if  current_user.id != company_id:
        abort(404)
    page = request.args.get('page', 1, type=int)
    pagination = Job.query.filter_by(company_id=company_id).paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('company/admin_index.html',company_id=company_id, pagination=pagination)

@company.route('/<int:company_id>/admin/apply/')
@login_required
def admin_apply(company_id):
    if current_user.id != company_id:
        abort(404)
    status = request.args.get('status','all')
    page = request.args.get('page',default=1, type=int)
    q = Delivery.query.filter_by(company_id = company_id)

    if status == 'todolist':
        q=q.filter(Delivery.status==Delivery.STATUS_WAITING)
    elif status == 'reject':
        q=q.filter(Delivery.status==Delivery.STATUS_REJECT)
    elif status == 'accept':
        q=q.filter(Delivery.status==Delivery.STATUS_ACCEPT)

    pagination = q.paginate(
        page = page,
        per_page = current_app.config['ADMIN_PER_PAGE'],
        error_out = False
    )
    return render_template('company/admin_apply.html',pagination=pagination, company_id=company_id)

@company.route('/<int:company_id>/admin/apply/<int:apply_id>/reject/')
@login_required
def admin_apply_reject(company_id, apply_id):
    if current_user.id != company_id:
        abort(404)
    apply = Delivery.query.get_or_404(apply_id)
    apply.status = Delivery.STATUS_REJECT
    db.session.add(apply)
    db.session.commit()
    flash('已拒绝该投递','success')
    return redirect(url_for('company.admin_apply',company_id=company_id))

@company.route('/<int:company_id>/admin/apply/<int:apply_id>/accept/')
@login_required
def admin_apply_accept(company_id, apply_id):
    if current_user.id != company_id:
        abort(404)
    apply = Delivery.query.get_or_404(apply_id)
    apply.status = Delivery.STATUS_ACCEPT
    db.session.add(apply)
    db.session.commit()
    flash('已接受该投递,准备面试','success')
    return redirect(url_for('company.admin_apply',company_id=company_id))


@company.route('/<int:company_id>/admin/job/<int:job_id>/disable')
@login_required
def admin_disable_job(company_id, job_id):
    if  current_user.id != company_id:
        abort(404)
    job = Job.query.get_or_404(job_id)
    if job.company_id != current_user.id:
        abort(404)
    job.is_open = not job.is_open
    db.session.add(job)
    db.session.commit()
    if job.is_open:
        flash('职位已上线','success')    
    else:
        flash('职位已下线','success')    
    return redirect(url_for('company.admin_index',company_id=company_id))

@company.route('/<int:company_id>/admin/job/new',methods=['POST','GET'])
@login_required
def admin_add_job(company_id):
    if  current_user.id != company_id:
        abort(404) 
    form = JobForm()
    if form.validate_on_submit():
        form.create_job(current_user)
        flash('创建职位成功','success')
        return redirect(url_for('company.admin_index', company_id=current_user.id))
    return render_template('company/admin_new_job.html',form=form, company_id=company_id)
    
@company.route('/<int:company_id>/admin/job/<int:job_id>/edit',methods=['POST','GET'])
@login_required
def admin_edit_job(company_id,job_id):
    if  current_user.id != company_id:
        abort(404) 
    job = Job.query.get_or_404(job_id)
    if job.company_id != current_user.id:
        abort(404)         
    form = JobForm(obj=job)
    if form.validate_on_submit():
        form.update_job(job)
        flash('课程更新成功','success')
        return redirect(url_for('company.admin_index',company_id=company_id))
    return render_template('company/admin_edit_job.html',company_id=company_id, job=job, form= form)

@company.route('/<int:company_id>/admin/job/<int:job_id>/delete',methods=['POST','GET'])
@login_required
def admin_delete_job(company_id,job_id):
    if  current_user.id != company_id:
        abort(404) 
    job = Job.query.get_or_404(job_id)
    if job.company_id != current_user.id:
        abort(404)       
    db.session.delete(job)
    db.session.commit()
    flash('课程删除成功','success')
    return redirect(url_for('company.admin_index',company_id=company_id))



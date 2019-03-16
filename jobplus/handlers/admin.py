from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for, abort

from jobplus.forms import CompanyEditForm, UserEditForm, RegisterForm
from jobplus.lib.decorators import admin_required
from jobplus.models import User, db, Company, Job

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@admin_required
def index():
    return render_template('admin/admin_base.html')


@admin.route('/users')
@admin_required
def users():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/users.html', pagination=pagination)


@admin.route('/jobs')
@admin_required
def jobs():
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/jobs.html', pagination=pagination)


@admin.route('/users/create_user', methods=['GET', 'POST'])
@admin_required
def create_user():
    form = RegisterForm()
    if form.is_submitted():
        form.create_user()
        flash('创建求职者成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/create_user.html', form=form)


@admin.route('/users/create_company', methods=['GET', 'POST'])
@admin_required
def create_company():
    form = RegisterForm()
    form.name.label.text = '公司名称'
    if form.validate_on_submit():
        user = form.create_user()
        user.role = User.ROLE_COMPANY
        db.session.add(user)
        db.session.commit()
        flash('创建公司成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/create_company.html', form=form)


@admin.route('/users/<int:user_id>/disable', methods=['GET', 'POST'])
@admin_required
def disable_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_disable:
        user.is_disable = False
    else:
        user.is_disable = True
    db.session.add(user)
    db.session.commit()
    if user.is_disable:
        flash('已经成功禁用用户', 'success')
    else:
        flash('已经成功启用用户', 'success')

    return redirect(url_for('admin.users'))


@admin.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_company:
        # 由于企业注册的时候只写了user表，没有写company表,所以需要新写入一次
        if not user.company_info:
            company = Company()
            company.user_id = user.id
            company.name = user.name
            db.session.add(company)
            db.session.commit()

        form = CompanyEditForm(obj=user)
    else:
        form = UserEditForm(obj=user)

    if form.validate_on_submit():
        form.update(user)
        flash('更新成功', 'success')
        return redirect(url_for('admin.users'))

    if user.is_company:
        form.site.data = user.company_info.website
        form.description.data = user.company_info.short_description
    return render_template('admin/edit_user.html', form=form, user=user)

@admin.route('/jobs/<int:job_id>/disable')
@admin_required
def disable_job(job_id):
    job = Job.query.get_or_404(job_id)
    job.is_open = not job.is_open
    db.session.add(job)
    db.session.commit()
    if job.is_open:
        flash('已上线职位','success')
    else:
        flash('已下线职位','success')
    return redirect(url_for('.jobs'))

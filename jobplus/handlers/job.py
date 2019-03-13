from flask import Blueprint, render_template, url_for, request, current_app, redirect, flash
from flask_login import login_required, current_user
from jobplus.models import Job, Delivery, db

job = Blueprint('job', __name__, url_prefix='/job')


@job.route('/')
def index():
    page = request.args.get('page', default=1, type=int)

    pagination = Job.query.filter_by(is_open=True).paginate(
        page=page,
        per_page=current_app.config['JOB_PER_PAGE'],
        error_out=False
    )
    return render_template('job/job.html',pagination=pagination)

@job.route('/<int:job_id>')
def detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job/detail.html', job=job)

@job.route('/<int:job_id>/apply')
@login_required
def apply(job_id):
    job=Job.query.get_or_404(job_id)
    if job.is_current_user_applied: 
        flash('当前职位已经投递过','warning')
    else:
        delivery = Delivery(
            job_id=job_id,
            user_id=current_user.id,
            status=Delivery.STATUS_WAITING,
            location=job.location
        )
        db.session.add(delivery)
        db.session.commit()
        flash('投递成功','success')
    return redirect(url_for('.detail', job_id=job_id))

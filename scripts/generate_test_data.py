from jobplus.models import db, Job
import json


def add_jobs(file):
    with open(file,'r') as f:
        jobs = json.load(f)
        for job in jobs:
            jobobj = Job(
                name=job['name'],
                location=job['location'],
                salary_max=job['salary_max'],
                salary_min=job['salary_min'],
                tags=job['tags'],
                experience_requirement=job['experience_requirement'],
                degree_requirement=job['degree_requirement']
            )
            db.session.add(jobobj)


def run():
    add_jobs('datas/jobs.json')

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()


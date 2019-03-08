from jobplus.models import db, Job, Company
from faker import Faker
from random import randint,choice
import json

fake = Faker()

citys = ['成都','上海','北京','广州']

tag_list = ['高薪','不加班','python','福利']

degrees = ['本科','专科', '硕士' ,'博士']

natures = ['全职',  '兼职']

def add_jobs(file):
    companys = Company.query.all()
    for c in companys:
        fake_job_num = randint(2,4)
        for i in range(fake_job_num):
            jobobj = Job(
                name=c.name+ '|job:'+str(i),
                salary_max=randint(10,20),
                salary_min=randint(5,9),
                location=choice(citys),
                tags=','.join([choice(tag_list), choice(tag_list)]),
                experience_requirement='{}-{}年'.format(randint(1,3), randint(4,10)),
                degree_requirement=choice(degrees),
                job_nature = choice(natures),
                company = c,
                description = fake.sentence()
            )
            db.session.add(jobobj)


def run():
    add_jobs('datas/jobs.json')

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()


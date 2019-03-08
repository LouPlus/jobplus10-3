import requests
import re
import time
from flask import Flask
from faker import Faker
from jobplus.models import Job, db, Company
from jobplus.config import configs



fake = Faker()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    db.init_app(app)

    return app

def get_job_data(page):
    headers = {
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0',
        'Referer': 'https://www.lagou.com/jobs/list_?px=new&city=%E5%85%A8%E5%9B%BD',
        'Cookie': 'JSESSIONID=ABAAABAAADEAAFI2A6380247760563EE6ED3BE9E9471591; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1552010331; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1552011370; _ga=GA1.2.1381585888.1552010331; user_trace_token=20190308095850-b79dbb24-4145-11e9-a92f-525400f775ce; LGSID=20190308095850-b79dbc42-4145-11e9-a92f-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGRID=20190308101609-230456e7-4148-11e9-8b96-5254005c3644; LGUID=20190308095850-b79dbdd5-4145-11e9-a92f-525400f775ce; index_location_city=%E6%88%90%E9%83%BD; TG-TRACK-CODE=index_checkmore; SEARCH_ID=7b92cb46c20c4ebaab37c6c7ac740424; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221695b12efdb24c-0756c9251f70bb8-72206752-1824000-1695b12efdcb8%22%2C%22%24device_id%22%3A%221695b12efdb24c-0756c9251f70bb8-72206752-1824000-1695b12efdcb8%22%7D; sajssdk_2015_cross_new_user=1; LG_LOGIN_USER_ID=197c963b4d2cdf2453dcd698ec4f90d09655efef99499613; _putrc=DDF9FC3A22B5B6FF; login=true; unick=%E5%BC%A0%E6%B5%A9%E7%94%B0; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; gate_login_token=2b6af23c46cb56f6f03f6d096780bcb4983519fd10857d9f; _gat=1'
    }
    payload={'first':'false','pn':page, 'kd':''}
    url = 'https://www.lagou.com/jobs/positionAjax.json?px=new&needAddtionalResult=false'
    res = requests.post(url, data=payload,headers=headers, timeout=10)
    if res.status_code==200:
        try:
            print(res.json())
            #data= []
            data=res.json()['content']['positionResult']['result']
            return data
        except:
            print("can't get job data")

def insert_job(job):
    with app.app_context():
        result = Company.query.filter(lagou_company_id=job['companyId'])

        new_job = Job(name=job['positionName'],
                      salary_max=int(re.match(r'.*-(\d+)[k,K]', job['salary'])),
                      salary_min=int(re.match(r'(\d+)[k,K]-.*', job['salary'])),
                      location = job['city'],
                      tags = ','.join(job['positionLables']),
                      experience_requirement = job['workYear'],
                      degree_requirement=job['education'],
                      jobNature=job['jobNature'],
                      company = result,
                      description = fake.sentence()
        )
        db.session.add(new_job)
        db.session.commit()




if __name__ == '__main__':
    app = create_app('test')
    job_count=50
    page = 1
    while job_count>0:
        jobs = get_job_data(page)
        page+=1
        filtered_jobs=[]
        for job in jobs:
            #只爬取在数据库中存在的公司提供的职位
            print(job)
            result = Company.query.filter(lagou_company_id=job['companyId'])
            if not result:
                filtered_jobs.append(job)

        for job in filtered_jobs:
            print(job)
            insert_job(job)
            job_count-=1

        time.sleep(10)
        
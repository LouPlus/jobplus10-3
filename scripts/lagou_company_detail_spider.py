import re
import json
import time

from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from jobplus.config import configs
from jobplus.models import db, Company

options = Options()
options.headless = True
options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    db.init_app(app)

    return app


def get_company_detal(company_id):
    company_url = 'https://www.lagou.com/gongsi/{company_id}.html'.format(company_id=company_id)
    driver.get(company_url)
    html = driver.page_source
    page = re.findall(r'<script id="companyInfoData" type="text/html">(.*?)</script>', html)[0]
    data = json.loads(page)
    company_profile = data['introduction']['companyProfile']
    location = data['addressList'][0]['detailAddress']
    return company_profile, location


if __name__ == '__main__':
    app = create_app('test')
    with app.app_context():
        companies = Company.query.filter(Company.id > 29).all()
        for company in companies:
            if company.lagou_company_id:
                full_description, location = get_company_detal(company.lagou_company_id)
                company = Company.query.filter(Company.lagou_company_id == company.lagou_company_id).first()
                company.full_description = full_description
                company.location = location
                db.session.add(company)
                db.session.commit()
                print(company.id, company.name, company.lagou_company_id, company.full_description, company.location)
                time.sleep(1)

import time
import requests
import re
from flask import Flask
from jobplus.config import configs
from jobplus.lib.tool import random_string, random_email
from jobplus.models import Company, db, User


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    db.init_app(app)

    return app


def get_company_data(page):
    # 需要自行登录一次拉钩后找到Cookie, 替换下面headers中的cookie
    headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0',
               'Referer': 'https://www.lagou.com/gongsi/',
               'Origin': 'https://www.lagou.com',
               
               'Cookie': 'JSESSIONID=ABAAABAAAFCAAEGADA24BD2E9A3A2350788DF553B3F8B19; _ga=GA1.2.1445026406.1552479981; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1552479982; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1552484404; user_trace_token=20190313202620-351b9c50-458b-11e9-86eb-525400f775ce; LGRID=20190313214002-80e5ad82-4595-11e9-94e6-5254005c3644; LGUID=20190313202620-351b9f90-458b-11e9-86eb-525400f775ce; _gid=GA1.2.1234951713.1552479982; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_company; _gat=1; LGSID=20190313214002-80e5aa04-4595-11e9-94e6-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F'}
    payload = {'first': 'false', 'pn': page, 'sortField': 0, 'havemark': 0}

    url = 'https://www.lagou.com/gongsi/0-0-0-0.json'
    res = requests.post(url, data=payload, headers=headers, timeout=10)
    if res.status_code == 200:
        try:
            data = res.json()['result']
            return data
        except:
            print('无法获得正确的数据')


def download_img(img_url):
    # 获取文件后缀
    suffix = '.' + img_url.split('?')[0].split('.')[-1]
    # 生成随机的文件名
    filename = random_string() + suffix
    file_dir = './jobplus/static/clogo/{filename}'.format(filename=filename)
    r = requests.get(img_url)
    with open(file_dir, 'wb') as f:
        f.write(r.content)
        print('下载图片成功')
        return filename


def insert_company(company):
    logo_base_url = 'https://www.lgstatic.com/'
    # 获取到企业的logo地址，下载后放到项目文件中
    logo_url = logo_base_url + company['companyLogo']
    file_name = download_img(logo_url)
    with app.app_context():
        company_user = User()
        company_user.name = company['companyFullName']
        company_user.email = random_email()
        company_user.password = '123456'
        company_user.role = User.ROLE_COMPANY
        db.session.add(company_user)
        db.session.commit()
        print(company_user.id)

        new_company = Company(lagou_company_id=company['companyId'],
                              name=company['companyFullName'],
                              logo=file_name if file_name else 'avatar.png',
                              short_description=company['companyFeatures'],
                              short_name=company['companyShortName'],
                              welfare=company['otherLabel'],
                              trade=company['industryField'],
                              funding=company['financeStage'],
                              size=company['companySize'],
                              city=company['city'],
                              user_id=company_user.id)
        db.session.add(new_company)
        db.session.commit()


if __name__ == '__main__':
    app = create_app('test')
    for page in range(10):
        company_datas = get_company_data(page)
        for company in company_datas[:100]:
            print(company)
            insert_company(company)
        time.sleep(1)





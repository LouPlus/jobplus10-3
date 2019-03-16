import time
import requests
import re
from flask import Flask
from jobplus.config import configs
from jobplus.lib.tool import random_string, random_email
from jobplus.models import Company, db, User


# 需要自行登录一次拉钩后找到Cookie, 替换下面headers中的cookie
headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0',
           'Referer': 'https://www.lagou.com/gongsi/',
           'Origin': 'https://www.lagou.com',
           'Cookie': 'WEBTJ-ID=20190226232625-1692a6a05262a1-0a7f40c2a499b9-36657105-1764000-1692a6a0529a01; _ga=GA1.2.1964949034.1551194785; user_trace_token=20190226232625-e10e55f8-39da-11e9-9202-525400f775ce; LGUID=20190226232625-e10e5adb-39da-11e9-9202-525400f775ce; JSESSIONID=ABAAABAAAFCAAEGB0C0046FE1E0C4EA160BA5DF25998CE2; mds_login_authToken="OB02Q1k8/Wo5XrrpGT7q9gFKmcIN9R4vfkIIVPIw8/kW/Ft7K3kI/Cihf8oUjUj1GVGQntvIw2UmpH+Hocgprxeo0dMDpWPUqEwHzs/JaV+WttgiyCOU+ZXxqdP6Y3VHAGW1rDMbUFRvb4vMZlwxNsETqMMZx6WoRuJaJM6MML14rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; _putrc=59BF92213C546537; login=true; unick=%E8%92%8B%E9%87%91%E6%9D%B0; X_MIDDLE_TOKEN=577e28c48c14b736cab93a7a8264fb5d; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1551194785,1551947676; index_location_city=%E6%9D%AD%E5%B7%9E; LGSID=20190316100141-71034bae-478f-11e9-b1ee-525400f775ce; SEARCH_ID=303a8536d30949a59105648f178114a6; _gat=1; LG_LOGIN_USER_ID=48b6d3d7c4f64f04c54ff40bcf3dc91bdce8b75643c3a3aa; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; gate_login_token=04f20110afe255f25e1b03a7ab17eaed45dfe919fd2bace6; TG-TRACK-CODE=index_bannerad; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1552705488; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221692a6a2c6e43c-096227507d63a4-36657105-1764000-1692a6a2c6f6dc%22%2C%22%24device_id%22%3A%221692a6a2c6e43c-096227507d63a4-36657105-1764000-1692a6a2c6f6dc%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24os%22%3A%22MacOS%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2272.0.3626.121%22%7D%7D; LGRID=20190316110449-42d6cf9f-4798-11e9-97d7-5254005c3644'
            }


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    db.init_app(app)

    return app


def get_company_data(page):
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




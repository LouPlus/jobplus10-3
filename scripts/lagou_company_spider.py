import time
import requests
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
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
               'Referer': 'https://www.lagou.com/gongsi/',
               'Origin': 'https://www.lagou.com',
               'Cookie': 'WEBTJ-ID=20190226232625-1692a6a05262a1-0a7f40c2a499b9-36657105-1764000-1692a6a0529a01; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1551194785; _ga=GA1.2.1964949034.1551194785; user_trace_token=20190226232625-e10e55f8-39da-11e9-9202-525400f775ce; LGUID=20190226232625-e10e5adb-39da-11e9-9202-525400f775ce; JSESSIONID=ABAAABAAAFCAAEGB0C0046FE1E0C4EA160BA5DF25998CE2; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; index_location_city=%E5%85%A8%E5%9B%BD; ab_test_random_num=0; mds_login_authToken="OB02Q1k8/Wo5XrrpGT7q9gFKmcIN9R4vfkIIVPIw8/kW/Ft7K3kI/Cihf8oUjUj1GVGQntvIw2UmpH+Hocgprxeo0dMDpWPUqEwHzs/JaV+WttgiyCOU+ZXxqdP6Y3VHAGW1rDMbUFRvb4vMZlwxNsETqMMZx6WoRuJaJM6MML14rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221692a6a2c6e43c-096227507d63a4-36657105-1764000-1692a6a2c6f6dc%22%2C%22%24device_id%22%3A%221692a6a2c6e43c-096227507d63a4-36657105-1764000-1692a6a2c6f6dc%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; TG-TRACK-CODE=index_checkmore; LG_LOGIN_USER_ID=8a978870815a635cbd8bc4ecd227da66abd81408fc23f2c1; _putrc=59BF92213C546537; login=true; unick=%E8%92%8B%E9%87%91%E6%9D%B0; gate_login_token=a4c99b500c20f78d936941e7e3482c97c6338d8b780303ad; X_MIDDLE_TOKEN=577e28c48c14b736cab93a7a8264fb5d; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1551716328; LGSID=20190305001847-3088a5d7-3e99-11e9-8fb8-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Futrack%2FtrackMid.html%3Ff%3Dhttps%253A%252F%252Fwww.lagou.com%252Fgongsi%252F%26t%3D1551716327%26_ti%3D1; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F; LGRID=20190305001848-30ee2395-3e99-11e9-8a33-5254005c3644'}
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
    suffix = '.' + img_url.split('.')[-1]
    # 生成随机的文件名
    filename = random_string() + suffix
    file_dir = '../jobplus/static/clogo/{filename}'.format(filename=filename)
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
        company_datas = get_company_data(10)
        for company in company_datas[:100]:
            print(company)
            insert_company(company)
        time.sleep(1)




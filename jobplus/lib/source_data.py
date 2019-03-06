from collections import namedtuple


CompanyFilter = namedtuple('CompanyFilter', ['city', 'funding', 'trade', 'size'])

company_filter_data = CompanyFilter(city=['不限', '北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '南京', '西安', '厦门', '长沙', '苏州'],
                                    funding=['不限', '天使轮', 'A轮', 'B轮', 'C轮', 'D轮及以上', '上市公司', '不需要融资'],
                                    trade=['不限', '移动互联网', '电子商务', '金融', '企业服务', '教育', '文化娱乐', '游戏', 'O2O', '硬件'],
                                    size=['不限', '少于15人', '15-50人', '50-150人', '150-500人', '500-2000人', '2000人以上'])


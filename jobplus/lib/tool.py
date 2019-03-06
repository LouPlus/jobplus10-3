import random


def random_string(length=32):
    base_str = '1234567890qwertyuiopasdfghjklmnbvcxz'
    return ''.join([random.choice(base_str) for i in range(length)])


def random_email():
    email_type = ["@qq.com", "@163.com", "@gmail.com"]
    domain = random.choice(email_type)
    rang = random.randint(4, 10)
    base_str = "0123456789qbcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPWRSTUVWXYZ"
    random_str = "".join(random.choice(base_str) for i in range(rang))
    email = random_str + domain
    return email


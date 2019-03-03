import random


def random_string(length=32):
   base_str = '1234567890qwertyuiopasdfghjklmnbvcxz'
   return ''.join([random.choice(base_str) for i in range(length)])




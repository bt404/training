# -*- coding: utf-8 -*-
# author: gjz.knd2
# 该模块主要生成测试用日志文件
# 主要学习了random，os，datetime，time等4个模块
# random.choice/randint/sample/shuffle/uniform
# os.path.exists/mkdir等文件/目录的相关操作，文件读写
# datetime和time以及二者之间的转换，在notes中有记录

import random
import os
import datetime
import time
import sys


MONTH = 2592000
LEVEL = ('1', '2', '3', '4')
METHODS = ("GET", "POST")
STATUS = ('200', '300', '400', '500')
CLIENTS = {
    "8.8.8.1": "Bob",
    "10.2.1.5": "Hallen",
    "8.1.1.4": "John",
    "8.1.1.8": "May",
    "80.1.1.8": "Ben",
    "78.3.1.4": "Will",
    "68.1.30.4": "Red",
    "8.3.1.4": "Robot",
    "8.1.30.4": "Tom",
    "8.14.1.4": "Jerry"
}
VIEWS = ("question", "topic", "blog", "comment", "space")
PAGE_NUM = 25   # 设置每个view下的page数量为25
PAGES = []

def producer(num=2000):
    if not os.path.exists('data'):
        os.mkdir('data')
    with open('data/access.log', 'w+') as log:
        for i in xrange(num):
            time = generate_time()
            url = generate_url()
            client = generate_client()
            method = generate_method()
            status = generate_status()
            level = generate_level()
            resp_time = response_time()
            line = concat(level, time, status, method, url, client, resp_time)
            log.write(line)


def generate_time():
    now = int(time.time())
    timestamp = random.randint(now-MONTH, now)
    result = datetime.datetime.utcfromtimestamp(timestamp)
    return result.isoformat()


def generate_url():
    if len(PAGES) < PAGE_NUM:
        page = random.randint(100, 999)
        PAGES.append(page)
    else:
        page = random.choice(PAGES)
    view = random.choice(VIEWS)
    return '/'.join(['', view, str(page)])


def generate_client():
    return random.choice(CLIENTS.keys())


def generate_status():
    return random.choice(STATUS)


def generate_method():
    return random.choice(METHODS)


def generate_level():
    return random.choice(LEVEL)


def response_time():
    resp_time = "{0}ms".format(str(random.randint(1, 600)))
    return resp_time


def concat(level, time, status, method, url, client, resp_time):
    header = "[{0} {1}]".format(level, time)    # 尽量用格式化字符串
    return ' '.join([header, CLIENTS[client], status, method, url, client, resp_time])+'\n'


if __name__ == "__main__":
    num = 2000
    if len(sys.argv)-1:
        try:
            num = int(sys.argv[1])
        except:
            sys.exit("Invalid arg")
    producer(num)

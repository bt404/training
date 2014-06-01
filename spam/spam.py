# -*- coding: utf-8 -*-
# 实现一个防垃圾信息的简易功能
# 1. 生成格式化的日志文件（已经有producer.py实现，日志文件在data/access.log）
# 2. 找到半小时内访问topic超过两次且至少有两个不同page的用户列表
# 3. 找到一个路径列表，其中每个路径每天至少被两个用户访问


from model import Record
from datetime import datetime, timedelta
import time
import os
import re


PATTERN = r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})]\s([A-Za-z]+)\s.+(/[a-z]+/\d{3})\s(\d+\.\d+\.\d+\.\d+)'


def line_parser(line):
    pattern = re.compile(PATTERN)
    #time, name, view, ip = pattern.findall(line)[0]
    return pattern.findall(line)[0]


def save_info(file_name):
    if not os.path.exists(file_name):
        return 'file not exists'
    Record.dropCollection()
    with open(file_name) as file:
        for line in file.readlines():
            result = Record.create()
            time, name, view, ip = line_parser(line)
            result["ip"] = ip
            result["name"] = name
            result["view"] = view
            resp_time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
            result["time"] = resp_time
            result.save()


def filter_info(days):
    now = datetime.now()
    cond_time = now-timedelta(days)
    cond = {}
    cond["$and"] = [{"time": {"$gt": cond_time}}, {"time": {"$lt": now}}]
    result = Record.aggregate([
        {"$match": cond},
        # ip和view为组合key分组
        {"$group": {"_id": {"ip": "$ip", "view": "$view"}, "num": {"$sum": 1}}},
        {"$sort": {"num": -1}}
    ])["result"]
    return result


def get_users(days):
    result = filter_info(days)
    ret = []
    users = {}      # 缓存ip和view的对应关系
    for record in result:
        temp = record["_id"]
        ip = temp["ip"]
        view = temp["view"]
        ip_stored = users.get(ip)
        if ip_stored and not users[ip] == view:
            ret.append(ip)      # 当一个ip对应两个或以上view时将ip填入ret
        else:
            users[ip] = view
    ret = list(set(ret))        # 删除重复用户
    print ret


def get_views(days):
    result = filter_info(days)
    users = []
    for key, value in result:
        user = {}


save_info('data/access.log')
get_users(days=1)

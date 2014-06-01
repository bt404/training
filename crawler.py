# -*- coding: utf8 -*-
# crawler written 2 years ago

import os
import re
import threading
import urllib2
from bs4 import BeautifulSoup
from Queue import Queue


# 用来保存一个网页内的所有href
class GetUrls:
    def __init__(self):
        self.url = []
    def getURL(self, html):
        data = BeautifulSoup(html)
        urls = data.find_all('a', href=True)   # 查找href不为空的所有a标签
        for x in urls:
            self.url.append(x['href'])      # 获取a标签的href属性，即url

# 爬虫类，用来从队列中取出一个url并保存网页内容，更新队列。是一个线程类。
class Crawler(threading.Thread):
    def __init__(self, name, queues):
        threading.Thread.__init__(self)
        self.num = 0
        try:
            os.makedirs('/home/knd2/webpages/'+self.name)   # 该线程抓取的网页存储文件夹
        except OSError:
            pass
        self.way = '/home/knd2/webpages/'+self.name+'/'
        self.queues = queues
    def run(self):
        while True:
            if queues == []:
                break
            queue = self.queues[0]
            try:
                url = queue.get(timeout=10)       # 因为第一级队列只有一个url，所以如果不设置超时，那么第2个及以后的线程将永远阻塞。
            except:
                continue
            try:
                html = urllib2.urlopen(url).read().decode('gbk').encode('utf8')
            except:
                continue
            parser = GetUrls()
            parser.getURL(html)
            for item in parser.url:
                if item[:4]!='http':            # 如果href给出的是服务器上的相对地址，那么补全完整url。
                    item = 'http://www.dytt8.net'+item
                if len(self.queues)>1:          # 当仍要进行下一级抓取的时候，才继续添加url。
                    self.queues[1].put(item)
            way = self.way+str(self.num)+'.html'  # 下面5行为存储网页数据。
            self.num += 1
            file = open(way,'w+')
            file.write(html)
            file.close()
            print self.name+':has crawled '+str(self.num-1)+'.html'
            try:
                if queue.empty():
                    # 考虑到同步问题，可能存在一个线程将queues置空后，其它线程仍执行remove从而产生异常。
                    self.queues.remove(queue)   
            except:
                break

if __name__ == '__main__':
    threads = []
    url = 'http://www.dytt8.net'
    queues = []
    for j in range(0, 2):       # 爬n级则设置n个队列，它们存储在queues列表中。
        queues.append(Queue())
    queues[0].put(url)
    for i in range(0, 3):
        threads.append(Crawler(str(i), queues))      # 创建3个线程执行操作
        threads[i].start()


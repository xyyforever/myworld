#!/user/bin/env python
#!-*-coding:utf-8 -*-


#!/user/bin/env python
#!-*-coding:utf-8 -*-

import pymysql
import requests

from threading import Thread

from queue import Queue

from lxml import etree
import json
import time

url = 'https://www.qiushibaike.com/8hr/page/%d/'

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}

parseQueue = Queue(3)

# 解析线程退出的标志
exitFlag = False

class CrawlThread(Thread):

    def __init__(self, queue,id):
        super().__init__()
        self.crawlQueue = queue
        self.id = id
    def run(self):
        super().run()
        print('爬虫线程-----%d------启动'%(self.id))

        self.getHtml()

        print('爬虫线程-----%d------终止'%(self.id))

    def getHtml(self):

        while True:
            # 退出条件
            if self.crawlQueue.empty():
                break

            #队列中取出索引，
            try:
                p = self.crawlQueue.get(block=False)

                url_qiubai = url%(p)

                response = requests.get(url=url_qiubai,headers = headers,verify = False)
                response.encoding = 'utf-8'
                html = response.text

                # 保存起来
                #保存到队列
                parseQueue.put((html,p))
                print('------------------------parseQueue',p)
                print('爬虫线程-------%d-------,获取了-------%d------页数据'%(self.id,p))

                #告诉爬虫队列，任务完成
                self.crawlQueue.task_done()
            except Exception as e:
                pass

datas = []
class ParseThread(Thread):

    def __init__(self, connect,cursor,id):
        super().__init__()
        self.connect = connect
        self.cursor = cursor
        self.id = id
    def run(self):
        super().run()
        print('解析线程-----%d------启动'%(self.id))

        self.parse()

        print('解析线程-----%d------终止'%(self.id))

    def parse(self):
        global exitFlag
        while True:
            # print('---------------------------',exitFlag)
            if exitFlag:
                break

#             从解析队列中获取数据
            try:
                html,p = parseQueue.get(block=False)

                tree = etree.HTML(html)

                divs = tree.xpath('//div[contains(@id,"qiushi_tag_")]')

                for div in divs:
                    nickname = div.xpath('.//h2/text()')[0].strip()
                    try:
                        headpic = div.xpath('.//div[@class="author clearfix"]/a/img/@src')[0]
                    except Exception as e:
                        print(e)
                        headpic = ''
                    try:
                        content = div.xpath('.//div[@class="content"]/span/text()')[0].strip()
                    except Exception as e:
                        print(e)
                        content = ''
                    contenthref = div.xpath('.//a[@class="contentHerf"]/@href')[0].strip()
                    if div.xpath('.//div[@class="thumb"]'):
                        img = div.xpath('.//div[@class="thumb"]/a/img/@src')[0].strip()
                    else:
                        img = ''
                    vote = div.xpath('.//span[@class="stats-vote"]/i/text()')[0].strip()
                    comment = div.xpath('.//span[@class="stats-comments"]//i/text()')[0].strip()
                    # str = '%s,%s,%s,%s,%s,%s,%s\n' % (nickname, headpic, content, vote, comment, contenthref, img)
                    # datas.append({'nickname': nickname, 'headpic': headpic, 'content': content,'vote': vote,'comment': comment,'contenthref': contenthref,'img': img,})
                    # json.dump(datas, fp=self.fp, ensure_ascii=False)
                    sql = "insert into smile(nickname, headpic, content, vote, comment, contenthref, img) values('%s','%s','%s','%s','%s','%s','%s')" % (nickname, headpic, content, vote, comment, contenthref, img)
                    # try:
                    self.cursor.execute(sql)
                    self.connect.commit()
                    print('数据插入成功')
                    # except Exception as e:
                    #     print('数据插入错误')
                    #     print(e)

                print('解析线程：------%d-----完成了-----%d------页的解析任务,该页数量：%d'%(self.id,p,len(divs)))
                parseQueue.task_done()
                print('--------------------------------------++++++++++++++++++++++++++++++++++++')
            except Exception as e:
                print(e)
                pass

if __name__ == '__main__':
    crawlQueue = Queue(7)
    for i in range(1,8):
        crawlQueue.put(i)
    for i in range(2):
        crawlThread = CrawlThread(crawlQueue,i)
        crawlThread.start()


    connect = pymysql.connect(
        host='localhost',
        db='myword',
        port=3306,
        user='root',
        passwd='123456',
        charset='utf8'
    )
    cursor =connect.cursor()

    # # 数据保存到json
    # fp = open('./smile.json', mode='a', encoding='utf-8')
    for i in range(1):
        parseThread = ParseThread(connect,cursor,i)
        parseThread.start()


    # 对队列，加锁
    crawlQueue.join()
    parseQueue.join()

    exitFlag = True
    print('+++++++++++++++++++++++++++++++++++++++++++',exitFlag)

    connect.close()
    cursor.close()
    # fp.close()






















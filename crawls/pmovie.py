#!/user/bin/env python
#!-*-coding:utf-8 -*-


import requests
from lxml import etree
import pymysql
import time

def parse(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}

    response = requests.get(url=url, headers=headers)
    response.encoding = 'utf-8'
    text = response.text

    tree = etree.HTML(text)

    divs = tree.xpath('//div[@class="grid-2x grid-3x-md grid-6x-sm"]')

    for div in divs:
        movie_pic = div.xpath('.//img/@src')[0]
        movie_name = div.xpath('.//img/@alt')[0]
        score1 = div.xpath('.//i[@class="score"]/b/text()')
        score2 = div.xpath('.//i[@class="score"]/text()')
        if score2:
            movie_score = score1[0] + score2[0]
        else:
            movie_score = ''
        desc = div.xpath('.//p/text()')
        if desc:
            movie_des = desc[0]
        else:
            movie_des = ''

        jump_href = div.xpath('.//a[@class="pic-pack-outer"]/@href')[0]
        # 将得到的数据传送给MySQL
        mysql(movie_pic,movie_name,movie_score,movie_des,jump_href)



# 定义一个类，将连接MySQL的操作写入其中
class down_mysql:
    def __init__(self, movie_pic,movie_name,movie_score,movie_des,jump_href):
        self.movie_pic = movie_pic
        self.movie_name = movie_name
        self.movie_score = movie_score
        self.movie_des = movie_des
        self.jump_href = jump_href
        self.connect = pymysql.connect(
            host='localhost',
            db='myword',
            port=3306,
            user='root',
            passwd='123456',
            charset='utf8'
        )
        self.cursor = self.connect.cursor()

    # 保存数据到MySQL中
    def save_mysql(self):
        sql = "insert into movie_list(movie_pic,movie_name,movie_score,movie_des,jump_href) values('%s','%s','%s','%s','%s')" % (self.movie_pic,self.movie_name,self.movie_score,self.movie_des,self.jump_href)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            print('数据插入成功')
        except Exception as e:
            print('数据插入错误')
            print(e)


# 新建对象，然后将数据传入类中
def mysql(movie_pic,movie_name,movie_score,movie_des,jump_href):
    down = down_mysql(movie_pic,movie_name,movie_score,movie_des,jump_href)
    down.save_mysql()


if __name__ == '__main__':
    # 给定一个初始的url
    for x in range(1,13):
        onum = str(x)
        url = 'http://www.1905.com/vod/list/n_1_t_5/o1p'+onum+'.html'
        # 解析该url
        #解开注释就可以运行扒取
        # parse(url)
        #延迟2s
        time.sleep(3)















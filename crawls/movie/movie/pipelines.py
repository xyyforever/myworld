# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql


class MoviePipeline(object):

    #打开数据库
    def __init__(self):
        self.conn = pymysql.connect(host = '127.0.0.1',port = 3306,user = 'root',passwd = '123456',db = 'myword',charset = 'utf8')
        self.cursor = self.conn.cursor()

     #数据插入数据库
    def process_item(self, item, spider):
        movie_name = item['movie_name']
        movie_pic = item['movie_pic']
        movie_intract = item['movie_intract']
        movie_download_url = item['movie_download_url']

        sql = "insert into film_down(movie_name,movie_pic,movie_intract,movie_download_url) values('%s','%s','%s','%s')"%(movie_name,movie_pic,movie_intract,movie_download_url)

        flag = self.cursor.execute(sql)

        print(flag)
        #提交数据库
        self.conn.commit()
        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()

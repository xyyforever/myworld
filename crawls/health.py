#!/user/bin/env python
#!-*-coding:utf-8 -*-


from selenium import webdriver
import pymysql
import time

chrome = webdriver.Chrome()

# chrome.get('http://www.360changshi.com/jk/')

time.sleep(2)

#常识类型

types = chrome.find_elements_by_xpath("//div[@class='lei']")
#图片地址
xpath_urls = '//div[@class="pic"]/a/img'
pic_srcs = chrome.find_elements_by_xpath(xpath_urls)

ptimes = chrome.find_elements_by_xpath("//div[@class='meta']")
#图片链接地址
xpath_urls1 = '//div[@class="pic"]/a'
pic_hrefs = chrome.find_elements_by_xpath(xpath_urls1)

#标题
titles = chrome.find_elements_by_xpath("//div[@class='title']")

#内容
contents = chrome.find_elements_by_xpath("//div[@class='item']/p")

#标签
tabss = chrome.find_elements_by_xpath("//span[@class='span1']")

#打开并配置数据库
conn = pymysql.connect(
    host='localhost',
    db='myword',
    port=3306,
    user='root',
    passwd='123456',
    charset='utf8'
)
cursor = conn.cursor()
#
for type,pic_src,pic_href,title,content,tabs,ptime in zip(types,pic_srcs,pic_hrefs,titles,contents,tabss,ptimes):
    #拿字段
    hlytype = type.text
    pic_src = pic_src.get_attribute("src")
    pic_href = pic_href.get_attribute("href")
    title = title.text
    content = content.text
    tabs = tabs.text
    ptime = ptime.text
    # print(hlytype,pic_src,pic_href,title,content,tabs)
#
    #将数据写入数据库
    sql = "insert into health(hlytype,pic_src,pic_href,title,content,tabs,ptime) values('%s','%s','%s','%s','%s','%s','%s')" % (hlytype,pic_src,pic_href,title,content,tabs,ptime)
    try:
        flag = cursor.execute(sql)
        # 提交数据库
        conn.commit()
        print('数据保存成功')
    except Exception as e:
        print(e)
        print('数据保存失败')













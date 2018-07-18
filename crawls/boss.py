#!/user/bin/env python
#!-*-coding:utf-8 -*-
#!@Author : xyy

from selenium import webdriver
import pymysql
import time

chrome = webdriver.Chrome()
#全国
# chrome.get('https://www.zhipin.com/job_detail/?query=python&scity=100010000&industry=&position=')

#上海
# chrome.get('https://www.zhipin.com/job_detail/?query=python&scity=101020100&industry=&position=')


time.sleep(2)


while True:
    #职位名称
    Zjob_title = chrome.find_elements_by_xpath("//div[@class='job-title']")
    #职位要求
    xpath_urls = '//div[@class="info-primary"]/h3/a'
    urls_pre = chrome.find_elements_by_xpath(xpath_urls)
    Zjob_require = urls_pre
    # #薪资范围
    Zsalary = chrome.find_elements_by_xpath("//span[@class='red']")
    Zworkinfo1 = chrome.find_elements_by_xpath("//div[@class='info-primary']/p")
    #公司名称
    Zcompname = chrome.find_elements_by_xpath("//div[@class='company-text']/h3/a")
    #公司详情链接
    xpath_urls_1 = "//div[@class='company-text']/h3/a"
    urls_pre_a = chrome.find_elements_by_xpath(xpath_urls_1)
    Zcompdetail_href = urls_pre_a
    # 公司信息
    Zworkinfo2 = chrome.find_elements_by_xpath("//div[@class='company-text']/p")

    #招聘人头像
    xpath_urls_2 = "//div[@class='info-publis']/h3/img"
    urls_pre_b = chrome.find_elements_by_xpath(xpath_urls_2)
    Zhead_pic = urls_pre_b
    #招聘人信息
    Zworkinfo3 = chrome.find_elements_by_xpath("//div[@class='info-publis']/h3")

    #发布招聘时间
    Zpublic_time = chrome.find_elements_by_xpath("//div[@class='info-publis']/p")

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

    for job_title,job_require,salary,workinfo1,compname,compdetail_href,workinfo2,head_pic,workinfo3,public_time in zip(Zjob_title,Zjob_require,Zsalary,Zworkinfo1,Zcompname,Zcompdetail_href,Zworkinfo2,Zhead_pic,Zworkinfo3,Zpublic_time):
        # 职位名称
        job_title = job_title.text
        # 职位要求
        job_require = job_require.get_attribute("href")
        # #薪资范围
        salary = salary.text
        workinfo11 = workinfo1.text

        if workinfo11.find('应届生') != -1:
            # 工作经验
            work_exp = '应届生'
            # 工作地点
            work_city = workinfo11.split('应届生')[0]
            # 学历
            education = workinfo11.split('应届生')[1]
        elif workinfo11.find('1年以内') != -1:
            work_exp = '1年以内'
            work_city = workinfo11.split('1年以内')[0]
            education = workinfo11.split('1年以内')[1]
        elif workinfo11.find('1-3年') != -1:
            work_exp = '1-3年'
            work_city = workinfo11.split('1-3年')[0]
            education = workinfo11.split('1-3年')[1]
        elif workinfo11.find('3-5年') != -1:
            work_exp = '3-5年'
            work_city = workinfo11.split('3-5年')[0]
            education = workinfo11.split('3-5年')[1]
        elif workinfo11.find('5-10年') != -1:
            work_exp = '5-10年'
            work_city = workinfo11.split('5-10年')[0]
            education = workinfo11.split('5-10年')[1]
        elif workinfo11.find('10年以上') != -1:
            work_exp = '10年以上'
            work_city = workinfo11.split('10年以上')[0]
            education = workinfo11.split('10年以上')[1]
        else:
            work_exp = '不限'
            if workinfo11[-1] != '限':
                education = workinfo11.split('不限')[1]
            else:
                education = '不限'
            work_city = workinfo11.split('不限')[0]

        # 公司名称
        compname = compname.text
        # 公司详情链接
        compdetail_href = compdetail_href.get_attribute("href")
        # 公司信息
        workinfo2 = workinfo2.text
        # 招聘人头像
        head_pic = head_pic.get_attribute("src")
        # 招聘人信息
        workinfo3 = workinfo3.text
        # 发布招聘时间
        public_time = public_time.text
        # print(job_title, job_require, salary, work_city, work_exp, education, compname, compdetail_href, workinfo2,head_pic, workinfo3, public_time)
        #将数据写入数据库
        sql = "insert into python_shanghai(job_title, job_require, salary, work_city, work_exp, education, compname, compdetail_href, workinfo2,head_pic, workinfo3, public_time) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (job_title, job_require, salary, work_city, work_exp, education, compname, compdetail_href, workinfo2,head_pic, workinfo3, public_time)
        try:
            flag = cursor.execute(sql)
            # 提交数据库
            conn.commit()
            print('数据保存成功')
        except Exception as e:
            print(e)
            print('数据保存失败')

    index = chrome.page_source.find('next disabled')
    if index != -1:
        break

    #点击下一页
    chrome.find_element_by_class_name('next').click()
    time.sleep(5)















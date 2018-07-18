import requests
from bs4 import BeautifulSoup
import pymysql
import time


# 解析链接
def parse(url):
    html = requests.get(url)
    html.encoding = 'utf-8'
    html = html.text
    soup = BeautifulSoup(html, 'lxml')
    # 找到li标签，该标签内有两个class属性，分别为book,clearfix
    data = soup.select('div.songlist-list > ul > li')
    # 解析该data
    for i in data:
        music_id = i.find('a', class_='songlist-play-hook').attrs['data-listid']
        music_pic = i.find('img').attrs['src']
        listen_num = i.select('div.num > span')[0].get_text()
        song_title = i.select('p.text-title > a')[0].get_text()
        song_user = i.select('p.text-user > a')[0].get_text()
        # 将得到的数据传送给MySQL
        mysql(music_id,music_pic,listen_num,song_title,song_user)



# 定义一个类，将连接MySQL的操作写入其中
class down_mysql:
    def __init__(self, music_id,music_pic,listen_num,song_title,song_user):
        self.music_id = music_id
        self.music_pic = music_pic
        self.listen_num = listen_num
        self.song_title = song_title
        self.song_user = song_user
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
        sql = "insert into music_list(music_id,music_pic,listen_num,song_title,song_user) values('%s','%s','%s','%s','%s')" % (self.music_id, self.music_pic, self.listen_num, self.song_title, self.song_user)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            print('数据插入成功')
        except Exception as e:
            print('数据插入错误')
            print(e)


# 新建对象，然后将数据传入类中
def mysql(music_id,music_pic,listen_num,song_title,song_user):
    down = down_mysql(music_id,music_pic,listen_num,song_title,song_user)
    down.save_mysql()


if __name__ == '__main__':
    # 给定一个初始的url
    for x in range(10):
        onum = str(x * 20)
        url = 'http://music.taihe.com/songlist/tag/%E5%85%A8%E9%83%A8?orderType=1&offset='+onum+'&third_type='
        # 解析该url
        #解开注释就可以运行扒取
        # parse(url)
        #延迟2s
        time.sleep(3)
#跳转
# http://play.taihe.com/?__m=mboxCtrl.playSongMenu&__a=523046683&__o=/songlist/tag/全部||songMenu&fr=-1||-1#
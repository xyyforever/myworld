from django.db import models

# Create your models here.

class MyUser(models.Model):
    name = models.CharField(max_length=20)

#音乐列表
class MusicList(models.Model):
    music_id = models.CharField(max_length=10)
    music_pic = models.CharField(max_length=200)
    listen_num = models.CharField(max_length=60)
    song_title = models.CharField(max_length=100)
    song_user = models.CharField(max_length=100)
    class Meta:
        db_table = 'music_list'

#电影列表
class MovieList(models.Model):
    movie_pic = models.CharField(max_length=200)
    movie_name = models.CharField(max_length=60)
    movie_score = models.CharField(max_length=60,default='Null')
    movie_des = models.CharField(max_length=100,default='Null')
    jump_href = models.CharField(max_length=200,default='Null')
    class Meta:
        db_table = 'movie_list'

#电影下载
class FilmDown(models.Model):
    movie_name = models.CharField(max_length=60)
    movie_pic = models.CharField(max_length=200)
    movie_intract = models.CharField(max_length=300)
    movie_download_url = models.CharField(max_length=1000)
    class Meta:
        db_table = 'film_down'

#boss直聘python全国
#job_title, job_require, salary, work_city, work_exp, education, compname, compdetail_href, workinfo2,head_pic, workinfo3, public_time
class PythonPos(models.Model):
    job_title = models.CharField(max_length=30)
    job_require = models.CharField(max_length=200)
    salary = models.CharField(max_length=20)
    work_city = models.CharField(max_length=20)
    work_exp = models.CharField(max_length=20)
    education = models.CharField(max_length=20)
    compname = models.CharField(max_length=30)
    compdetail_href = models.CharField(max_length=200)
    workinfo2 = models.CharField(max_length=60)
    head_pic = models.CharField(max_length=200)
    workinfo3 = models.CharField(max_length=60)
    public_time = models.CharField(max_length=20)
    class Meta:
        db_table = 'python_pos'

#boss直聘python上海
class PythonShanghai(models.Model):
    job_title = models.CharField(max_length=30)
    job_require = models.CharField(max_length=200)
    salary = models.CharField(max_length=20)
    work_city = models.CharField(max_length=20)
    work_exp = models.CharField(max_length=20)
    education = models.CharField(max_length=20)
    compname = models.CharField(max_length=30)
    compdetail_href = models.CharField(max_length=200)
    workinfo2 = models.CharField(max_length=60)
    head_pic = models.CharField(max_length=200)
    workinfo3 = models.CharField(max_length=60)
    public_time = models.CharField(max_length=20)
    class Meta:
        db_table = 'python_shanghai'

#健康常识数据
class Healthy(models.Model):
    hlytype = models.CharField(max_length=30)
    ptime = models.CharField(max_length=20,default='今天')
    pic_src = models.CharField(max_length=200)
    pic_href = models.CharField(max_length=200)
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=500)
    tabs = models.CharField(max_length=30)
    class Meta:
        db_table = 'health'

# nickname,content,vote,comment,contenthref,img
#段子
class Smile(models.Model):
    nickname = models.CharField(max_length=30)
    content = models.CharField(max_length=1000)
    vote = models.CharField(max_length=20)
    comment = models.CharField(max_length=20)
    contenthref = models.CharField(max_length=50)
    img = models.CharField(max_length=200,default='Null')
    headpic = models.CharField(max_length=200)
    class Meta:
        db_table = 'smile'

#用户信息
class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=32)
    icon = models.CharField(max_length=64,default='default.png')
    user_token = models.CharField(max_length=32)
    class Meta:
        db_table='world_userinfo'












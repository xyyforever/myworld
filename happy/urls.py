"""myworld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url,re_path

from happy import views
from happy import views1

urlpatterns = [
    #注册登录和注销
    url(r'jumplogin/',views1.jumplogin),
    url(r'jumpregist/',views1.jumpregist),
    url(r'regist/',views1.regist),
    url(r'login/',views1.login),
    url(r'logout/',views1.logout),
    #编辑上传图片
    #编辑
    url('edit/',views1.edit),
    #上传头像
    url('uploadpic/',views1.uploadpic),
    #首页
    url(r'^$',views.myindex),
    #热门音乐
    url(r'hot_music/(\d*)',views.hot_music),
    #音乐下载load_music
    url('load_music/',views.load_music),
    #下载的列表展示to_load
    url(r'to_load/',views.to_load),
    #热门电影
    url(r'hot_movie/(\d*)',views.hot_movie),
    #电影下载load_movie
    url(r'load_movielist/(\d*)',views.load_movielist),
    #python职位，全国
    url(r'python_pos/(..)/(\d*)',views.python_pos),
    #市场分析
    url('analysis/',views.analysis),
    #分析图表
    url('charts/',views.charts),
    #生活，健康
    url('heathy/',views.heathy),
    #生活，小段子
    url('smile/',views.smile),
    #垃圾站
    url('garbage/',views.garbage),

]

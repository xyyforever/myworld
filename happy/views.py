import hashlib
import logging
import random
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import MusicList,MovieList,FilmDown,PythonPos,PythonShanghai,Healthy,UserInfo
from django.http import JsonResponse, HttpResponse
import time
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create your views here.
#测试
def myindex(request):
    token = request.COOKIES.get('user_token')
    user = UserInfo.objects.filter(user_token=token)
    if user.exists():
        user = user.first()
        return render(request, 'happy/myindex.html', {'name': user.uname, 'user': user})
    return redirect('/jumplogin/')

#热门音乐
def hot_music(request,pagenum):
    token = request.COOKIES.get('user_token')
    user = UserInfo.objects.filter(user_token=token)
    if user.exists():
        if not pagenum:
            pagenum = 1
            # 分页
        infoall = MusicList.objects.all()
        paginator = Paginator(infoall, 20)
        page = paginator.page(pagenum)
        ouserall = page.object_list
        pagelist = paginator.page_range
        return render(request, 'happy/hot_music.html',{ 'hotlist': ouserall, 'pagelist': pagelist, 'page': page})
    return redirect('/jumplogin/')
#音乐下载页面
def load_music(request):
    token = request.COOKIES.get('user_token')
    user = UserInfo.objects.filter(user_token=token)
    if user.exists():
        return render(request,'happy/load_music.html')
    return redirect('/jumplogin/')


#下载的列表展示to_load
import urllib
import urllib.request
import urllib.parse
import re
import json
import time
url_info = 'http://tingapi.ting.baidu.com/v1/restserver/ting?method=baidu.ting.song.play&format=jsonp&callback=jQuery17202741599001012014_1513517333931&songid=%s&_=1513517334915'

url_songid = 'http://music.taihe.com/search?key=%s'

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Connection':'keep-alive',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',

}
#获取音乐id
def get_songid(siner):
    key = urllib.parse.quote(siner)
    url=url_songid%(key)
    request = urllib.request.Request(url=url,headers=headers)
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')
    pattern = r'sid&quot;:([\d]+)'
    p = re.compile(pattern,re.S)
    songids = p.findall(html)
    print(songids)
    return songids
#下载操作
def to_load(request):
    siner = request.GET.get('name')
    songids = get_songid(siner)
    olist=[]
    for songid in songids:
        url = url_info%(songid)
        request = urllib.request.Request(url=url,headers=headers)
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')
        pattern = r'\((.*)\)'
        p=re.compile(pattern)
        json_str=p.findall(content)[0]
        songinfo = json.loads(json_str,encoding='utf-8')
        title = songinfo['songinfo']['title']
        song_url = songinfo['bitrate']['file_link']
        olist.append((title,song_url))
    return JsonResponse({'result': '200', 'musiclist': olist})


#热门电影
def hot_movie(request,pagenum):
    if not pagenum:
        pagenum = 1
    # 分页
    infoall = MovieList.objects.all()
    paginator = Paginator(infoall, 20)
    page = paginator.page(pagenum)
    ouserall = page.object_list
    pagelist = paginator.page_range
    return render(request, 'happy/hot_movie.html',{ 'hotlist': ouserall, 'pagelist': pagelist, 'page': page})

#电影下载页面
def load_movielist(request,pagenum):
    if not pagenum:
        pagenum = 1
    # 分页
    infoall = FilmDown.objects.all()

    paginator = Paginator(infoall, 10)
    page = paginator.page(pagenum)
    ouserall = page.object_list
    pagelist = paginator.page_range
    return render(request,'happy/load_movielist.html',{ 'mdown_list': ouserall, 'pagelist': pagelist, 'page': page})

#python职位全国
def python_pos(request,addr,pagenum):
    if not pagenum:
        pagenum = 1
    # 分页
    if addr == '全国':
        infoall = PythonPos.objects.all()
    elif addr == '上海':
        infoall = PythonShanghai.objects.all()
    else:
        infoall = PythonPos.objects.all()
    paginator = Paginator(infoall, 20)
    page = paginator.page(pagenum)
    everypage = page.object_list
    pagelist = paginator.page_range
    return render(request,'happy/pythonList.html',{'python_list': everypage, 'type':addr, 'pagelist': pagelist, 'page': page})


#python 市场分析图表
def analysis(request):
    return render(request, 'happy/analysis.html')

def get_exp_chart(objs):
    # 工作经验
    exps_litter_one = len(objs.objects.filter(work_exp='应届生'))
    exps_no_limit = len(objs.objects.filter(work_exp='不限'))
    exps_inner_one = len(objs.objects.filter(work_exp='1年以内'))
    exps_one_three = len(objs.objects.filter(work_exp='1-3年'))
    exps_three_five = len(objs.objects.filter(work_exp='3-5年'))
    exps_five_ten = len(objs.objects.filter(work_exp='5-10年'))
    exps_up_ten = len(objs.objects.filter(work_exp='10年以上'))
    # {'value': exps_up_ten, 'name': '10年以上'}
    exps = [
        {'value': exps_litter_one, 'name': '应届生'},
        {'value': exps_no_limit, 'name': '不限'},
        {'value': exps_inner_one, 'name': '1年以内'},
        {'value': exps_one_three, 'name': '1-3年'},
        {'value': exps_three_five, 'name': '3-5年'},
        {'value': exps_five_ten, 'name': '5-10年'},
        {'value': exps_up_ten, 'name': '10年以上'}
    ]
    exps_arry = ['应届生', '不限', '1年以内', '1-3年', '3-5年', '5-10年', '10年以上']
    data = {"exps":exps,"exps_arry":exps_arry}
    return data;

def get_educate_chart(objs):
    educate_zhuan = len(objs.objects.filter(education='大专'))
    educate_ben = len(objs.objects.filter(education='本科'))
    educate_shuo = len(objs.objects.filter(education='硕士'))
    educate_bo = len(objs.objects.filter(education='博士'))
    educate_no_limit = len(objs.objects.filter(education='不限'))
    educates = [
        {'value': educate_zhuan, 'name': '大专'},
        {'value': educate_ben, 'name': '本科'},
        {'value': educate_shuo, 'name': '硕士'},
        {'value': educate_bo, 'name': '博士'},
        {'value': educate_no_limit, 'name': '不限'},
    ]
    arry_edu = ['大专', '本科', '硕士', '博士', '不限']
    data = {"arry_edu": arry_edu, "educates": educates}
    return data;

def get_salary_chart(objs):
    alldata = objs.objects.all()
    salary_8 = []
    salary_8_12 = []
    salary_12_15 = []
    salary_15_20 = []
    salary_20_30 = []
    salary_up_30 = []
    for saly in alldata:
        t = saly.salary
        s = t.replace('k', '').split('-')
        avg = (int(s[0]) + int(s[1])) / 2
        if int(s[1]) > 36:
            salary_up_30.append(saly.salary)
        else:
            if avg < 8:
                salary_8.append(saly.salary)
            elif (avg >= 8 and avg < 12):
                salary_8_12.append(saly.salary)
            elif (avg >= 12 and avg < 15):
                salary_12_15.append(saly.salary)
            elif (avg >= 15 and avg < 20):
                salary_15_20.append(saly.salary)
            elif (avg >= 20 and avg < 30):
                salary_20_30.append(saly.salary)
            else:
                salary_up_30.append(saly.salary)

    salarys = [
        {'value': len(salary_8), 'name': '8k以下'},
        {'value': len(salary_8_12), 'name': '8k-12k'},
        {'value': len(salary_12_15), 'name': '12k-15k'},
        {'value': len(salary_15_20), 'name': '15-20k'},
        {'value': len(salary_20_30), 'name': '20k-30k'},
        {'value': len(salary_up_30), 'name': '30k以上'},
    ]
    arry_salary = ['8k以下', '8k-12k', '12k-15k', '15-20k', '20k-30k', '30k以上']

    data = {"arry_salary": arry_salary, "salarys": salarys}
    return data;

#请求图表数据
def charts(request):
    # 工作经验
    exps = get_exp_chart(PythonPos)['exps']
    exps_arry = get_exp_chart(PythonPos)['exps_arry']
    #上海
    exps_sh = get_exp_chart(PythonShanghai)['exps']
    exps_arry_sh = get_exp_chart(PythonShanghai)['exps_arry']
    # 工作地点
    addr_beijing = len(PythonPos.objects.filter(work_city='北京'))
    addr_shanghai = len(PythonPos.objects.filter(work_city='上海'))
    addr_guangzhou = len(PythonPos.objects.filter(work_city='广州'))
    addr_shenzhen = len(PythonPos.objects.filter(work_city='深圳'))
    addr_hangzhou = len(PythonPos.objects.filter(work_city='杭州'))
    addr_nanjing = len(PythonPos.objects.filter(work_city='南京'))
    addr_wuhan = len(PythonPos.objects.filter(work_city='武汉'))
    addr_chengdou = len(PythonPos.objects.filter(work_city='成都'))
    addr_xian = len(PythonPos.objects.filter(work_city='西安'))
    addr_suzhou = len(PythonPos.objects.filter(work_city='苏州'))
    addr_other = 300 - (addr_beijing + addr_shanghai + addr_guangzhou + addr_shenzhen + addr_hangzhou + addr_nanjing + addr_wuhan + addr_chengdou + addr_xian + addr_suzhou)
    work_place = [
        {'value': addr_beijing, 'name': '北京'},
        {'value': addr_shanghai, 'name': '上海'},
        {'value': addr_guangzhou, 'name': '广州'},
        {'value': addr_shenzhen, 'name': '深圳'},
        {'value': addr_hangzhou, 'name': '杭州'},
        {'value': addr_nanjing, 'name': '南京'},
        {'value': addr_wuhan, 'name': '武汉'},
        {'value': addr_chengdou, 'name': '成都'},
        {'value': addr_xian, 'name': '西安'},
        {'value': addr_suzhou, 'name': '苏州'},
        {'value': addr_other, 'name': '其他'}
    ]
    arry_addr = ['北京', '上海', '广州', '深圳', '杭州', '南京', '武汉', '成都', '西安', '苏州', '其他']

    #学历要求
    arry_edu =get_educate_chart(PythonPos)['arry_edu']
    educates = get_educate_chart(PythonPos)['educates']
    #上海
    arry_edu_sh = get_educate_chart(PythonShanghai)['arry_edu']
    educates_sh = get_educate_chart(PythonShanghai)['educates']
    #薪资分布
    arry_salary = get_salary_chart(PythonPos)['arry_salary']
    salarys = get_salary_chart(PythonPos)['salarys']
    #上海
    arry_salary_sh = get_salary_chart(PythonShanghai)['arry_salary']
    salarys_sh = get_salary_chart(PythonShanghai)['salarys']
    data = {
        'exps_arry': exps_arry,
        'exps': exps,
        'exps_arry_sh': exps_arry_sh,
        'exps_sh': exps_sh,
        'workplace':work_place,
        'arry_addr':arry_addr,
        'educates':educates,
        'arry_edu':arry_edu,
        'salarys':salarys,
        'arry_salary':arry_salary,
        'educates_sh': educates_sh,
        'arry_edu_sh': arry_edu_sh,
        'salarys_sh': salarys_sh,
        'arry_salary_sh': arry_salary_sh,
    }

    return JsonResponse({'result':'200','data':data})



#生活。健康
def heathy(request):
    data = Healthy.objects.all()
    return render(request, 'happy/health.html',{'datalist':data})

#生活。小段子
def smile(request):
    return render(request, 'happy/smile.html')

#垃圾站
def garbage(request):
    return render(request, 'happy/garbage.html')
































#!/user/bin/env python
#!-*-coding:utf-8 -*-
#!@Author : gexianyu
import hashlib
import logging
import random
from django.shortcuts import render, redirect
from .models import UserInfo
from django.http import JsonResponse, HttpResponse
import time
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#登陆页面
def jumplogin(request):
    return render(request, 'happy/login.html')

#登陆
def login(request):
    if request.method == 'GET':
        return render(request, 'happy/login.html')

    name = request.POST.get('myname')
    password = request.POST.get('mypwd')

    user = UserInfo.objects.filter(uname=name)
    if user.exists():
        user = user.first()
        if user.upwd == pass_sec(password):
            user.user_token = creat_token()
            user.save()
            resp = JsonResponse({'result': '200', 'token': user.user_token, 'user_id': user.id, 'user_name': user.uname,
                                 'msg': '登录成功！'})
            resp.set_cookie('user_token', user.user_token)
            resp.set_cookie('user_id', user.id)
            return resp
        return JsonResponse({'result': '100', 'msg': '用户名或密码错误！'})
    return JsonResponse({'result': '100', 'msg': '用户名或密码错误！'})

#注册页面
def jumpregist(request):
    return render(request, 'happy/regist.html')

#注册
def regist(request):
    if request.method == 'GET':
        return render(request, 'happy/regist.html')
    name = request.POST.get('pwname')
    password = request.POST.get('pwpwd')
    surepwd = request.POST.get('surepwd')

    if password != surepwd:
        return JsonResponse({'result': '100', 'msg': '两次输入密码不相同！'})
    user = UserInfo()
    user.uname = name
    user.upwd = pass_sec(password)
    user.user_token = creat_token()
    user.save()
    htp = JsonResponse(
        {'result': '200', 'token': user.user_token, 'user_id': user.id, 'user_name': user.uname, 'msg': '注册成功！'})
    htp.set_cookie('user_token', user.user_token)
    htp.set_cookie('user_id', user.id)
    return htp

#退出登陆
def logout(request):
    token = request.COOKIES.get('user_token')
    if token:
        httpresponse = JsonResponse({'result': '200', 'msg': '已退出登录'})
        httpresponse.delete_cookie('user_token')
        httpresponse.delete_cookie('user_id')
        return httpresponse
    return JsonResponse({'result': '100', 'msg': '该用户不存在！'})

#生成MD5加密的token
def creat_token():
    secnum = str(time.time()) + str(random.random())
    md5 = hashlib.md5()
    md5.update(secnum.encode('utf-8'))
    istoken = md5.hexdigest()
    return istoken

#密码加密
def pass_sec(upass):
    md5 = hashlib.md5()
    md5.update(upass.encode('utf-8'))
    return md5.hexdigest()


#上传图片编辑信息

#编辑上传头像
def edit(request):
    token = request.COOKIES.get('user_token')
    user = UserInfo.objects.filter(user_token=token)
    if user.exists():
        user = user.first()
        return render(request,'happy/edit.html',{'name':user.uname,'user':user})
    return redirect('/jumplogin/')

# 上传头像
def uploadpic(request):
    if request.method == 'POST':
        filename = request.FILES.get('file')
        fileserver = BASE_DIR + '/static/uploads/' + filename.name
        import os
        ft = os.open(fileserver, os.O_CREAT | os.O_RDWR)
        for etc in filename.chunks():
            os.write(ft, etc)
        # os.close(ft)
        token = request.COOKIES.get('user_token')
        user = UserInfo.objects.filter(user_token=token)
        if user.exists():
            user = user.first()
            user.icon = filename.name
            user.save()
            return redirect('/edit/')
        return redirect('/jumplogin/')
    return HttpResponse('上传失败！')

































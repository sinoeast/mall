import logging
import re

from django import http
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

import logging

from apps.users.models import User

"""
断点的优势:
    1.可以查看我们的方法是否被调用了
    2.可以查看程序在运行过程中的数据
    3.查看程序的执行顺序是否和预期的一致

断点如何添加:
    0.不要在属性,类上加断点
    1.在函数(方法)的入口处
    2.在需要验证的地方添加
"""
#  注册日志
logging = logging.getLogger('django')

class Register(View):
    #
    def get(self, request: HttpRequest):
        return render(request, 'register.html')

    def post(self, request: HttpRequest):
        """
        1.接收前端提交的用户名,密码和手机号
        2.数据的验证(我们不相信前端提交的任何数据)
            2.1 验证比传(必须要让前端传递给后端)的数据是否有值
            2.2 判断用户名是否符合规则
            2.3 判断密码是否 符合规则
            2.4 判断确认密码和密码是否一致
            2.5 判断手机号是否符合规则
        3.验证数据没有问题才入库
        4.返回响应
        """
        # 1.接收前端提交的用户名,密码和手机号
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        allow = request.POST.get('allow')
        # 2.数据的验证(我们不相信前端提交的任何数据)
        #     2.1 验证必传(必须要让前端传递给后端)的数据是否有值
        # all([el,el,el]) el必须有值 只要有一个为None 则为False
        if not all([username,password,mobile,password2]):
            return http.HttpResponseBadRequest('有必填项缺失')
        #     2.2 判断用户名是否符合规则 判断 5-20位 数字 字母 _
        if not re.match(r'[0-9a-zA-Z_]{5,20}',username):
            return http.HttpResponseBadRequest('用户名不符合规则 判断 5-20位 数字 字母 _')
        #     2.3 判断密码是否 符合规则
        if not re.match(r"[0-9a-zA-Z_]{8,20}",password):
            return http.HttpResponseBadRequest('密码不符合规则 判断 8-20位 数字 字母 _')
        #     2.4 判断确认密码和密码是否一致
        if password != password2:
            return http.HttpResponseBadRequest('确认密码不一致')
        #     2.5 判断手机号是否符合规则
        if not re.match(r"",mobile):
            return http.HttpResponseBadRequest('手机号不符合规则')
        # 2.6 验证同意协议是否勾选
        if not allow:
            return http.HttpResponseBadRequest('请同意协议')
        # 3.验证数据没有问题才入库
        # 当我们在操作外界资源(mysql,redis,file)的时候,我们最好进行 try except的异常处理
        # User.objects.create  直接入库 理论是没问题的 但是 大家会发现 密码是明文
        try:
            # 利用继承的方法录入数据并且加密
            # User.objects.create_user(username=username,password=password,mobile=mobile)
            User.objects.create(username=username,password=password,mobile=mobile)
        except Exception :
            logging.error(Exception)
            return render(request, 'register.html', context={'error_message': '数据库异常'})
        # 系统也能自己去帮助我们实现 登陆状态的保持
        # from django.contrib.auth import login
        # login(request, user)
        request.session['username'] = username
        # 4.返回响应, 跳转到首页
        url = reverse("contents:index")
        return redirect(url)
        # 注册完成之后,默认认为用户已经登陆了
        # 保持登陆的状态
        # session
        # 自己实现request.session

        # 系统也能自己去帮助我们实现 登陆状态的保持
        # return http.HttpResponse('注册成功')

#验证重名 事务处理要全部处理，其他只做查询让前端处理
class UsernameCountView(View):
    def get(self,request,username):
        try:
            count = User.objects.filter(username=username).count()
        except:
            logging.error("数据库错误")
            return http.JsonResponse({"code":400,"contents":"数据库出错误"})
        return http.JsonResponse({"code":0,"count":count})


class MobileCountView(View):
    def get(self,request):
        mobile = request.GET.get('mobile')
        try:
            count = User.objects.filter(mobile__exact=mobile).count()
        except:
            logging.error("数据库错误")
            return http.JsonResponse({"code":400,"contents":"数据库错误"})
        return http.JsonResponse({"code":0,"count":count})

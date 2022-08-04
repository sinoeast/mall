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

from django.contrib.auth import authenticate, login

# 默认的认证后端是调用了
# from django.contrib.auth.backends import ModelBackend
# ModelBackend 中的认证方法
# def authenticate(self, request, username=None, password=None, **kwargs):

# 如果用户名和密码正确,则返回user
# 否则返回None
# user = authenticate(username=username,password=passwrod)

# is_authenticated 是否是认证用户
# 登陆用户返回 true
# 未登陆用户返回 false
# request.user.is_authenticated
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
from django.contrib.auth.mixins import LoginRequiredMixin

# 注册
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
        if not all([username, password, mobile, password2]):
            return http.HttpResponseBadRequest('有必填项缺失')
        #     2.2 判断用户名是否符合规则 判断 5-20位 数字 字母 _
        if not re.match(r'[0-9a-zA-Z_]{5,20}', username):
            return http.HttpResponseBadRequest('用户名不符合规则 判断 5-20位 数字 字母 _')
        #     2.3 判断密码是否 符合规则
        if not re.match(r"[0-9a-zA-Z_]{8,20}", password):
            return http.HttpResponseBadRequest('密码不符合规则 判断 8-20位 数字 字母 _')
        #     2.4 判断确认密码和密码是否一致
        if password != password2:
            return http.HttpResponseBadRequest('确认密码不一致')
        #     2.5 判断手机号是否符合规则
        if not re.match(r"", mobile):
            return http.HttpResponseBadRequest('手机号不符合规则')
        # 2.6 验证同意协议是否勾选
        if not allow:
            return http.HttpResponseBadRequest('请同意协议')
        # 3.验证数据没有问题才入库
        # 当我们在操作外界资源(mysql,redis,file)的时候,我们最好进行 try except的异常处理
        # User.objects.create  直接入库 理论是没问题的 但是 大家会发现 密码是明文
        try:
            # 利用继承的方法录入数据并且加密
            User.objects.create_user(username=username,password=password,mobile=mobile)
            # User.objects.create(username=username, password=password, mobile=mobile)
        except:
            logging.error(Exception)
            return render(request, 'register.html', context={'error_message': '数据库异常'})

        # 系统也能自己去帮助我们实现 登陆状态的保持
        # from django.contrib.auth import login
        # login(request, user)
        request.session['username'] = username

        # 4.返回响应, 跳转到首页
        url = reverse("contents:index")
        res = http.HttpResponseRedirect(url)
        res.set_cookie(key="username",value=username)

        # return redirect(url)
        return res
        # 注册完成之后,默认认为用户已经登陆了
        # 保持登陆的状态
        # session
        # 自己实现request.session

        # 系统也能自己去帮助我们实现 登陆状态的保持
        # return http.HttpResponse('注册成功')

# 验证重名 事务处理要全部处理，其他只做查询让前端处理
class UsernameCountView(View):
    def get(self, request, username):
        try:
            count = User.objects.filter(username=username).count()
        except:
            logging.error("数据库错误")
            return http.JsonResponse({"code": 400, "contents": "数据库出错误"})
        return http.JsonResponse({"code": 0, "count": count})

# 手机校验
class MobileCountView(View):
    def get(self, request):
        mobile = request.GET.get('mobile')
        try:
            count = User.objects.filter(mobile__exact=mobile).count()
        except:
            logging.error("数据库错误")
            return http.JsonResponse({"code": 400, "contents": "数据库错误"})
        return http.JsonResponse({"code": 0, "count": count})

# 登录
class LoginView(View):

    def get(self,request):

        return render(request,'login.html')



    def post(self,request):
        # 1.后端需要接收数据 (username,password)
        username=request.POST.get('username')
        passwrod=request.POST.get('password')
        remembered=request.POST.get('remembered')
        # 2.判断参数是否齐全
        if not all([username,passwrod]):
            return http.HttpResponseBadRequest('缺少必须的参数')
        # 3.判断用户名是否符合规则
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$',username):
            return http.HttpResponseBadRequest('用户名不符合规则')
        # 4.判断密码是否符合规则
        if not re.match(r'',passwrod):
            return http.HttpResponseBadRequest('密码不符合规则')
        # 5.验证用户名和密码re
        # 验证有2种方式
        # ① 使用django的认证后端
        # ② 我们可以自己查询数据库( 根据用户名/手机号查询对应的user用户,再比对密码)

        from apps.users import utils
        # 默认的认证后端是调用了 from django.contrib.auth.backends import ModelBackend
        # ModelBackend 中的认证方法
        # def authenticate(self, request, username=None, password=None, **kwargs):

        # 如果用户名和密码正确,则返回user
        # 否则返回None
        user = utils.UsernameMobileModelBackend().authenticate(request,username=username,password=passwrod)

        # is_authenticated 是否是认证用户
        # 登陆用户返回 true
        # 未登陆用户返回 false
        # request.user.is_authenticated

        if user is not None:
            # 6.如果验证成功则登陆,状态保持
            #登陆成功
            login(request,user)


            if remembered == 'on':
                #记住登陆
                # request.session.set_expiry(seconds)
                request.session.set_expiry(30*24*3600)
            else:
                # 不记住
                request.session.set_expiry(0)


            # 跳转到首页
            response = redirect(reverse('contents:index'))

            #设置cookie
            # response.set_cookie(key,value,max_age)
            response.set_cookie('username',user.username,max_age=14*24*3600)

            # 登录后跳转到之前访问的页面
            next = request.GET.get('next')
            if next:
                response = redirect(next)
            else:
                response = redirect(reverse('contents:index'))

            return response
        else:
            #登陆失败
            # 7.如果验证不成功则提示 用户名或密码错误
            return render(request,'login.html',context={'account_errmsg':'用户名或密码错误'})

# 登出
class LogoutView(View):

    def get(self,request):

        # request.session.flush()

        # 系统其他也给我们提供了退出的方法
        from django.contrib.auth import logout

        logout(request)

        # 退出之后,我们要跳转到指定页面
        # 还跳转到首页
        # 需要额外删除cookie中的name,因为我们首页的用户信息展示是通过username来判断

        response = redirect(reverse('contents:index'))

        response.delete_cookie('username')

        return response

from django.contrib.auth.mixins import LoginRequiredMixin
# 用户中心
class UserCenterInfoView(LoginRequiredMixin,View):

    def get(self,request):

        return render(request,'user_center_info.html')
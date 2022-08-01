import logging

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

import logging
#  注册日志
logging = logging.getLogger('django')

class Register(View):

    def get(self, request: HttpRequest):
        logging.info("成功")
        return render(request, 'register.html')

    def post(self, request: HttpRequest):
        """
        username : "",
        password : "",
        password2 : "",
        mobile : "",
        pic_code : "",
        sms_code : "",
        allow : "",
        :param request:
        :return:
        """
        username = request.POST.get('username')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        # if username == re


        pass

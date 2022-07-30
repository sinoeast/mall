import logging

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


class Register(View):

    def get(self, request: HttpRequest):
        logging.info("成功")
        return render(request, 'register.html')

    def post(self, request: HttpRequest):
        logging.info("成功")
        return render(request, 'register.html')

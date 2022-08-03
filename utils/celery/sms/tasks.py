#!/usr/bin/python3
# -*- coding:utf-8 -*-
""""
  @Author: 蓝天
  @Email: lantian27294@hundsun.com
  @Time: 2022/8/3 12:57
  @File: tasks.py
"""
from utils.celery.main import app


from libs.yuntongxun.sms import CCP


@app.task
def sms_sent_code(mobile,mobile_code,MOBILE_CODE_EXPIRE_TIME):
    CCP().send_template_sms(mobile, [mobile_code, MOBILE_CODE_EXPIRE_TIME], 1)
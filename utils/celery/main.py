#!/usr/bin/python3
# -*- coding:utf-8 -*-
""""
  @Author: 蓝天
  @Email: lantian27294@hundsun.com
  @Time: 2022/8/3 12:57
  @File: main.py
"""
import os

import utils

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mall.settings')

from celery import Celery

# 创建实例 设置中间人
app = Celery('tasks')

# 设置队列
# ③ celery 设置 broker (队列)
# config_from_object 参数: 就是 配置文件的路径
app.config_from_object("utils.celery.config")

# 设置生产者
# 让celery自动检测任务
#autodiscover_tasks 参数是 列表
# 列表的元素是: 任务的包路径
app.autodiscover_tasks(['utils.celery.sms'])

# 设置消费者
# pip install gevent
# celery -A utils.celery.main worker  -l info -P gevent
# 原因：celery不支持在windows下运行任务，需要借助gevent来完成……
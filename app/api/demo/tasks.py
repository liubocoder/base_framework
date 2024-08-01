# -*- coding: utf-8 -*-
# FileName       : tasks.py
# Create Time    : 2024/7/31 18:57:16
# Create By      : liubo
"""
tasks.py 使用说明:

调试的命令
/usr/local/bin/celery -A app worker -Q data_sync -B -l debug
1. 执行路径为项目根目录
2. /usr/local/bin/celery 为celery启动脚本
3. -A 参数 是celery应用初始化的包名，包含Celery('app')的文件包，本项目是app/celery.py中初始化的，因此是app

"""
import time

import celery
from celery import shared_task

from app.celery import app
from app.settings import logger


# 这里使用了bind=True，函数的第一个参数会传入celery.Task对象
# 其他参数包括：soft_time_limit、time_limit、max_retries等等，参考官方文档
# https://docs.celeryq.dev/en/stable/index.html
@shared_task(ignore_result=True, bind=True)
def demo_task(self: celery.Task):
    logger.debug(f"demo task begin: {self.name}")
    #do work
    time.sleep(1)
    logger.debug("demo task end")

@app.task
def demo_app_task(a, b):
    val = a+b
    logger.debug(f"app task: {a}+{b}={val}")
    return val
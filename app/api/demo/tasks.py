# -*- coding: utf-8 -*-
# FileName       : tasks.py
# Create Time    : 2024/7/31 18:57:16
# Create By      : liubo
"""
tasks.py 使用说明:

调试的命令
/usr/local/bin/celery -A app worker -Q data_sync -B -l debug
/usr/local/bin/celery 为celery启动脚本

"""
import time

from celery import shared_task

from app.settings import logger


@shared_task(ignore_result=True)
def demo_task():
    logger.debug("demo task begin")
    #do work
    time.sleep(1)
    logger.debug("demo task end")
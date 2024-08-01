# -*- coding: utf-8 -*-
# FileName       : celery.py
# Create Time    : 2024/7/31 19:04:51
# Create By      : liubo
"""
celery.py 使用说明:

"""

#作为兼容py2，这里不可不导入，整个项目已使用py3
#from  __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
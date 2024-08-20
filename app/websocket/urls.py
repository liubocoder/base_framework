# -*- coding: utf-8 -*-
# FileName       : urls.py
# Create Time    : 2024-08-19 15:29:58
# Created By     : liubo
"""
urls.py 使用说明:

"""
from django.urls import path

from app.websocket.ws import WsConsumer

ws_urlpatterns = [
    path("basefw/ws/v1/web/", WsConsumer.as_asgi())
]
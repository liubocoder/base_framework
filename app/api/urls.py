# -*- coding: utf-8 -*-
"""
urls.py 使用说明:
    api 路由定义
"""
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = []
urlpatterns += router.urls

from app.api.demo import urls as demo

urlpatterns += demo.urlpatterns


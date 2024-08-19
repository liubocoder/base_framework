# -*- coding: utf-8 -*-
# FileName       : urls.py
# Create Time    : 2024-08-19 10:32:28
# Created By     : liubo
"""
urls.py 使用说明:

"""
from django.urls import path, include, re_path
from rest_framework import routers

from app.api.myapp.views import MyAppViewSet

myapp_router = routers.DefaultRouter()
myapp_router.register("do-somethings", MyAppViewSet, basename="do_somethings")

urlpatterns = [
    path("myapp/", include(myapp_router.urls)),
]
